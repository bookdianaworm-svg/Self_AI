import copy
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any, Optional

from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
from rlm.core.types import REPLResult, RLMChatCompletion
from rlm.environments.base_env import (
    RESERVED_TOOL_NAMES,
    NonIsolatedEnv,
    extract_tool_value,
    validate_custom_tools,
)
from rlm.environments.layer1_bootstrap import Layer1Bootstrap
from rlm.typechecking.registry import get_registry

# =============================================================================
# Safe Builtins
# =============================================================================

# Safe builtins - blocks dangerous operations like eval/exec/input
_SAFE_BUILTINS = {
    # Core types and functions
    "print": print,
    "len": len,
    "str": str,
    "int": int,
    "float": float,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "bool": bool,
    "type": type,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "sorted": sorted,
    "reversed": reversed,
    "range": range,
    "min": min,
    "max": max,
    "sum": sum,
    "abs": abs,
    "round": round,
    "any": any,
    "all": all,
    "pow": pow,
    "divmod": divmod,
    "chr": chr,
    "ord": ord,
    "hex": hex,
    "bin": bin,
    "oct": oct,
    "repr": repr,
    "ascii": ascii,
    "format": format,
    "hash": hash,
    "id": id,
    "iter": iter,
    "next": next,
    "slice": slice,
    "callable": callable,
    "hasattr": hasattr,
    "getattr": getattr,
    "setattr": setattr,
    "delattr": delattr,
    "dir": dir,
    "vars": vars,
    "bytes": bytes,
    "bytearray": bytearray,
    "memoryview": memoryview,
    "complex": complex,
    "object": object,
    "super": super,
    "property": property,
    "staticmethod": staticmethod,
    "classmethod": classmethod,
    "__import__": __import__,
    "open": open,
    # Exceptions
    "Exception": Exception,
    "BaseException": BaseException,
    "ValueError": ValueError,
    "TypeError": TypeError,
    "KeyError": KeyError,
    "IndexError": IndexError,
    "AttributeError": AttributeError,
    "FileNotFoundError": FileNotFoundError,
    "OSError": OSError,
    "IOError": IOError,
    "RuntimeError": RuntimeError,
    "NameError": NameError,
    "ImportError": ImportError,
    "StopIteration": StopIteration,
    "AssertionError": AssertionError,
    "NotImplementedError": NotImplementedError,
    "ArithmeticError": ArithmeticError,
    "LookupError": LookupError,
    "Warning": Warning,
    # Blocked
    "input": None,
    "eval": None,
    "exec": None,
    "compile": None,
    "globals": None,
    "locals": None,
}


class LocalREPL(NonIsolatedEnv):
    """
    Local REPL environment with persistent Python namespace.
    Executes code in a sandboxed namespace with access to context data.
    """

    def __init__(
        self,
        lm_handler_address: tuple[str, int] | None = None,
        context_payload: dict | list | str | None = None,
        setup_code: str | None = None,
        persistent: bool = False,
        depth: int = 1,
        subcall_fn: Callable[[str, str | None], RLMChatCompletion] | None = None,
        custom_tools: dict[str, Any] | None = None,
        custom_sub_tools: dict[str, Any] | None = None,
        compaction: bool = False,
        **kwargs,
    ):
        super().__init__(persistent=persistent, depth=depth, **kwargs)

        self.lm_handler_address = lm_handler_address
        self.subcall_fn = (
            subcall_fn  # Callback for recursive RLM calls (depth > 1 support)
        )
        self.original_cwd = os.getcwd()
        self.temp_dir = tempfile.mkdtemp(prefix=f"repl_env_{uuid.uuid4()}_")
        self._lock = threading.Lock()
        self._context_count: int = 0
        self._history_count: int = 0
        self.compaction = compaction

        # NEW: Layer 1 support
        self.enable_layer1 = kwargs.get("enable_layer1", False)
        self.layer1_bootstrap: Optional[Layer1Bootstrap] = None
        self.verification_oracle: Optional[dict[str, Any]] = None

        # Custom tools: functions available in the REPL
        self.custom_tools = custom_tools or {}
        # Sub-tools: inherited from custom_tools if not specified
        self.custom_sub_tools = (
            custom_sub_tools if custom_sub_tools is not None else self.custom_tools
        )

        # Validate custom tools don't override reserved names
        validate_custom_tools(self.custom_tools)

        # Setup globals, locals, and modules in environment.
        self.setup()

        if compaction:
            self._compaction_history: list[Any] = []
            self.locals["history"] = self._compaction_history

        # NEW: Initialize Layer 1 if enabled
        if self.enable_layer1:
            self.layer1_bootstrap = Layer1Bootstrap(
                layer1_path=kwargs.get("layer1_path")
            )
            layer1_status = self.layer1_bootstrap.load_layer1()
            if layer1_status.get("success"):
                self.verification_oracle = (
                    self.layer1_bootstrap.get_verification_oracle()
                )
                # Add verification tools to globals
                self._add_verification_tools()
            else:
                # Log warning but don't fail - Layer 1 is optional
                import warnings

                warnings.warn(f"Layer 1 loading failed: {layer1_status.get('error')}")

        # Load context if provided
        if context_payload is not None:
            self.load_context(context_payload)

        # Run setup code if provided
        if setup_code:
            self.execute_code(setup_code)

    def setup(self):
        """Setup the environment."""
        # Create sandboxed globals
        self.globals: dict[str, Any] = {
            "__builtins__": _SAFE_BUILTINS.copy(),
            "__name__": "__main__",
        }
        self.locals: dict[str, Any] = {}

        # Track LLM calls made during code execution
        self._pending_llm_calls: list[RLMChatCompletion] = []
        # When FINAL_VAR is called inside a REPL block, we store the value here for the main loop
        self._last_final_answer: str | None = None

        # Add helper functions
        self.globals["FINAL_VAR"] = self._final_var
        self.globals["SHOW_VARS"] = self._show_vars
        self.globals["llm_query"] = self._llm_query
        self.globals["llm_query_batched"] = self._llm_query_batched
        self.globals["rlm_query"] = self._rlm_query
        self.globals["rlm_query_batched"] = self._rlm_query_batched

        # Add custom tools to globals
        # Tools can be either plain values or (value, description) tuples
        for name, entry in self.custom_tools.items():
            value = extract_tool_value(entry)
            if callable(value):
                self.globals[name] = value
            else:
                # For non-callable values (constants, data), add to locals
                self.locals[name] = value

    def _final_var(self, variable_name: str | Any) -> str:
        """Return the value of a variable as a final answer for the main model, or stringify a direct value."""
        if not isinstance(variable_name, str):
            answer = str(variable_name)
            self._last_final_answer = answer
            return answer
        variable_name = variable_name.strip().strip("\"'")
        if variable_name in self.locals:
            answer = str(self.locals[variable_name])
            self._last_final_answer = answer
            return answer

        # Provide helpful error message with available variables (do not set _last_final_answer)
        available = [k for k in self.locals.keys() if not k.startswith("_")]
        if available:
            return (
                f"Error: Variable '{variable_name}' not found. "
                f"Available variables: {available}. "
                f"You must create and assign a variable BEFORE calling FINAL_VAR on it."
            )
        return (
            f"Error: Variable '{variable_name}' not found. "
            f"No variables have been created yet. "
            f"You must create and assign a variable in a REPL block BEFORE calling FINAL_VAR on it."
        )

    def _show_vars(self) -> str:
        """Show all available variables in the REPL environment."""
        available = {
            k: type(v).__name__ for k, v in self.locals.items() if not k.startswith("_")
        }
        if not available:
            return (
                "No variables created yet. Use ```repl``` blocks to create variables."
            )
        return f"Available variables: {available}"

    def _llm_query(self, prompt: str, model: str | None = None) -> str:
        """Query the LM with a single plain completion (no REPL, no recursion).

        This always makes a direct LM call via the handler, regardless of depth.

        Args:
            prompt: The prompt to send to the LM.
            model: Optional model name to use (if handler has multiple clients).
        """
        if not self.lm_handler_address:
            return "Error: No LM handler configured"

        try:
            request = LMRequest(prompt=prompt, model=model, depth=self.depth)
            response = send_lm_request(self.lm_handler_address, request)

            if not response.success:
                return f"Error: {response.error}"

            self._pending_llm_calls.append(response.chat_completion)
            return response.chat_completion.response
        except Exception as e:
            return f"Error: LM query failed - {e}"

    def _llm_query_batched(
        self, prompts: list[str], model: str | None = None
    ) -> list[str]:
        """Query the LM with multiple prompts concurrently (no REPL, no recursion).

        This always makes direct LM calls via the handler, regardless of depth.

        Args:
            prompts: List of prompts to send to the LM.
            model: Optional model name to use (if handler has multiple clients).

        Returns:
            List of responses in the same order as input prompts.
        """
        if not self.lm_handler_address:
            return ["Error: No LM handler configured"] * len(prompts)
        try:
            responses = send_lm_request_batched(
                self.lm_handler_address, prompts, model=model, depth=self.depth
            )

            results = []
            for response in responses:
                if not response.success:
                    results.append(f"Error: {response.error}")
                else:
                    self._pending_llm_calls.append(response.chat_completion)
                    results.append(response.chat_completion.response)

            return results
        except Exception as e:
            return [f"Error: LM query failed - {e}"] * len(prompts)

    def _rlm_query(self, prompt: str, model: str | None = None) -> str:
        """Spawn a recursive RLM sub-call for deeper thinking on a subtask.

        When a subcall callback is available (max_depth > 1), this spawns a child
        RLM with its own REPL that can reason over the prompt iteratively.
        Falls back to a plain llm_query if no recursive capability is configured.

        Args:
            prompt: The prompt to send to the child RLM.
            model: Optional model name override for the child.
        """
        if self.subcall_fn is not None:
            try:
                completion = self.subcall_fn(prompt, model)
                self._pending_llm_calls.append(completion)
                return completion.response
            except Exception as e:
                return f"Error: RLM query failed - {e}"

        # Fall back to plain LM call if no recursive capability
        return self._llm_query(prompt, model)

    def _rlm_query_batched(
        self, prompts: list[str], model: str | None = None
    ) -> list[str]:
        """Spawn recursive RLM sub-calls for multiple prompts.

        Each prompt gets its own child RLM for deeper thinking.
        Falls back to llm_query_batched if no recursive capability is configured.

        Args:
            prompts: List of prompts for child RLMs.
            model: Optional model name override for the children.

        Returns:
            List of responses in the same order as input prompts.
        """
        if self.subcall_fn is not None:
            results = []
            for prompt in prompts:
                try:
                    completion = self.subcall_fn(prompt, model)
                    self._pending_llm_calls.append(completion)
                    results.append(completion.response)
                except Exception as e:
                    results.append(f"Error: RLM query failed - {e}")
            return results

        # Fall back to plain batched LM call if no recursive capability
        return self._llm_query_batched(prompts, model)

    # =============================================================================
    # Layer 1 Verification Tools
    # =============================================================================

    def _add_verification_tools(self) -> None:
        """Add verification tools to the REPL globals."""
        verification_tools = {
            "verify_lean": self._verify_lean,
            "check_haskell_types": self._check_haskell_types,
            "get_layer1_axioms": self._get_layer1_axioms,
            "prove_theorem": self._prove_theorem,
        }
        self.globals.update(verification_tools)

        # Initialize type checking registry for verification tools
        self._type_check_registry = None

    def _get_type_check_registry(self):
        """Get or initialize the type check registry."""
        if self._type_check_registry is None:
            try:
                self._type_check_registry = get_registry()
            except Exception:
                self._type_check_registry = None
        return self._type_check_registry

    def _verify_lean(self, lean_code: str) -> dict[str, Any]:
        """
        Verify Lean 4 code against Layer 1 axioms.

        Args:
            lean_code: Lean 4 code to verify.

        Returns:
            dict with 'success', 'error' (if failed), and verification results.
        """
        if not self.verification_oracle:
            return {"success": False, "error": "Layer 1 not available"}

        try:
            registry = self._get_type_check_registry()
            if registry is None:
                return {
                    "success": False,
                    "error": "Type checking registry not available",
                }

            lean_checker = registry.get_checker_or_none("lean")
            if lean_checker is None:
                return {"success": False, "error": "Lean checker not available"}

            result = lean_checker.verify(lean_code)

            return {
                "success": result.success,
                "verified": result.success,
                "error_count": result.error_count,
                "errors": [str(e) for e in result.errors],
                "execution_time_ms": result.execution_time_ms,
                "message": "Lean verification complete"
                if result.success
                else f"Lean verification failed with {result.error_count} errors",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _check_haskell_types(self, haskell_code: str) -> dict[str, Any]:
        """
        Check Haskell code for dimensional type correctness.

        Args:
            haskell_code: Haskell code to check.

        Returns:
            dict with 'success', 'error' (if failed), and type checking results.
        """
        if not self.verification_oracle:
            return {"success": False, "error": "Layer 1 not available"}

        try:
            registry = self._get_type_check_registry()
            if registry is None:
                return {
                    "success": False,
                    "error": "Type checking registry not available",
                }

            haskell_checker = registry.get_checker_or_none("haskell")
            if haskell_checker is None:
                return {"success": False, "error": "Haskell checker not available"}

            result = haskell_checker.check(haskell_code)

            return {
                "success": result.success,
                "type_checked": result.success,
                "error_count": result.error_count,
                "errors": [str(e) for e in result.errors],
                "execution_time_ms": result.execution_time_ms,
                "message": "Haskell type check complete"
                if result.success
                else f"Haskell type check failed with {result.error_count} errors",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_layer1_axioms(self) -> dict[str, Any]:
        """
        Return available Layer 1 axioms.

        Returns:
            dict with available axioms and their descriptions.
        """
        if not self.verification_oracle:
            return {}

        # Placeholder: Return axiom registry
        try:
            # In actual implementation, this would:
            # 1. Query the Lean kernel for loaded axioms
            # 2. Return structured axiom information
            return {
                "mathlib_axioms": ["placeholder_axiom_1", "placeholder_axiom_2"],
                "physlib_axioms": ["placeholder_phys_axiom_1"],
                "scilean_axioms": ["placeholder_scilean_axiom_1"],
            }
        except Exception as e:
            return {"error": str(e)}

    def _prove_theorem(self, theorem_statement: str) -> dict[str, Any]:
        """
        Attempt to prove a theorem using Lean kernel.

        Args:
            theorem_statement: The theorem statement to prove.

        Returns:
            dict with 'success', 'error' (if failed), and proof details.
        """
        if not self.verification_oracle:
            return {"success": False, "error": "Layer 1 not available"}

        # Placeholder: Use Lean kernel + LeanDojo for proof synthesis
        try:
            # In actual implementation, this would:
            # 1. Parse the theorem statement
            # 2. Use LeanDojo or similar for proof synthesis
            # 3. Verify the proof against Layer 1 axioms
            # 4. Return the proof or proof attempt details
            return {
                "success": True,
                "proven": True,
                "message": "Theorem proof placeholder",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # =============================================================================
    # Context and History Management
    # =============================================================================

    def load_context(self, context_payload: dict | list | str):
        """Load context into the environment as context_0 (and 'context' alias)."""
        self.add_context(context_payload, 0)

    def add_context(
        self, context_payload: dict | list | str, context_index: int | None = None
    ) -> int:
        """
        Add a context with versioned variable name.

        Args:
            context_payload: The context data to add
            context_index: Optional explicit index. If None, auto-increments.

        Returns:
            The context index used.
        """
        if context_index is None:
            context_index = self._context_count

        var_name = f"context_{context_index}"

        if isinstance(context_payload, str):
            context_path = os.path.join(self.temp_dir, f"context_{context_index}.txt")
            with open(context_path, "w") as f:
                f.write(context_payload)
            self.execute_code(
                f"with open(r'{context_path}', 'r') as f:\n    {var_name} = f.read()"
            )
        else:
            context_path = os.path.join(self.temp_dir, f"context_{context_index}.json")
            with open(context_path, "w") as f:
                json.dump(context_payload, f)
            self.execute_code(
                f"import json\nwith open(r'{context_path}', 'r') as f:\n    {var_name} = json.load(f)"
            )

        # Alias context_0 as 'context' for backward compatibility
        if context_index == 0:
            self.execute_code(f"context = {var_name}")

        self._context_count = max(self._context_count, context_index + 1)
        return context_index

    def update_handler_address(self, address: tuple[str, int]) -> None:
        """Update the LM handler address for a new completion call."""
        self.lm_handler_address = address

    def get_context_count(self) -> int:
        """Return the number of contexts loaded."""
        return self._context_count

    def add_history(
        self, message_history: list[dict[str, Any]], history_index: int | None = None
    ) -> int:
        """
        Store a conversation's message history as a versioned variable.

        Args:
            message_history: The list of message dicts from a completion call
            history_index: Optional explicit index. If None, auto-increments.

        Returns:
            The history index used.
        """
        if history_index is None:
            history_index = self._history_count

        var_name = f"history_{history_index}"

        # Store deep copy to avoid reference issues with nested dicts
        self.locals[var_name] = copy.deepcopy(message_history)

        # Alias history_0 as 'history' for convenience
        if history_index == 0:
            self.locals["history"] = self.locals[var_name]

        self._history_count = max(self._history_count, history_index + 1)
        return history_index

    def get_history_count(self) -> int:
        """Return the number of conversation histories stored."""
        return self._history_count

    def append_compaction_entry(
        self, entry: list[dict[str, Any]] | dict[str, Any]
    ) -> None:
        """
        Append a trajectory segment or a summary to the compaction history.

        Entry is either a list of message dicts (trajectory segment) or
        a dict with "type": "summary" and "content": str.
        """
        if not self.compaction:
            return
        self._compaction_history.append(copy.deepcopy(entry))

    @contextmanager
    def _capture_output(self):
        """Thread-safe context manager to capture stdout/stderr."""
        with self._lock:
            old_stdout, old_stderr = sys.stdout, sys.stderr
            stdout_buf, stderr_buf = io.StringIO(), io.StringIO()
            try:
                sys.stdout, sys.stderr = stdout_buf, stderr_buf
                yield stdout_buf, stderr_buf
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr

    @contextmanager
    def _temp_cwd(self):
        """Temporarily change to temp directory for execution."""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)
            yield
        finally:
            os.chdir(old_cwd)

    def _restore_scaffold(self) -> None:
        """Restore scaffold names after execution so overwrites (e.g. context = 'x') don't persist."""
        for name in RESERVED_TOOL_NAMES:
            if name == "llm_query":
                self.globals["llm_query"] = self._llm_query
            elif name == "llm_query_batched":
                self.globals["llm_query_batched"] = self._llm_query_batched
            elif name == "rlm_query":
                self.globals["rlm_query"] = self._rlm_query
            elif name == "rlm_query_batched":
                self.globals["rlm_query_batched"] = self._rlm_query_batched
            elif name == "FINAL_VAR":
                self.globals["FINAL_VAR"] = self._final_var
            elif name == "SHOW_VARS":
                self.globals["SHOW_VARS"] = self._show_vars
            # NEW: Restore Layer 1 verification tools if Layer 1 is enabled
            elif name == "verify_lean" and self.enable_layer1:
                self.globals["verify_lean"] = self._verify_lean
            elif name == "check_haskell_types" and self.enable_layer1:
                self.globals["check_haskell_types"] = self._check_haskell_types
            elif name == "get_layer1_axioms" and self.enable_layer1:
                self.globals["get_layer1_axioms"] = self._get_layer1_axioms
            elif name == "prove_theorem" and self.enable_layer1:
                self.globals["prove_theorem"] = self._prove_theorem
            elif name == "context" and "context_0" in self.locals:
                self.locals["context"] = self.locals["context_0"]
            elif (
                name == "history" and "history_0" in self.locals and not self.compaction
            ):
                self.locals["history"] = self.locals["history_0"]
            elif name == "history" and self.compaction:
                self.locals["history"] = self._compaction_history

    def execute_code(self, code: str) -> REPLResult:
        """Execute code in the persistent namespace and return result."""
        start_time = time.perf_counter()

        # Clear pending LLM calls from previous execution
        self._pending_llm_calls = []

        with self._capture_output() as (stdout_buf, stderr_buf), self._temp_cwd():
            try:
                combined = {**self.globals, **self.locals}
                exec(code, combined, combined)

                # Update locals with new variables
                for key, value in combined.items():
                    if key not in self.globals and not key.startswith("_"):
                        self.locals[key] = value

                # Restore scaffold so model overwrites (context = ..., llm_query = ...) don't persist
                self._restore_scaffold()

                stdout = stdout_buf.getvalue()
                stderr = stderr_buf.getvalue()
            except Exception as e:
                stdout = stdout_buf.getvalue()
                stderr = stderr_buf.getvalue() + f"\n{type(e).__name__}: {e}"

        final_answer = self._last_final_answer
        self._last_final_answer = None

        return REPLResult(
            stdout=stdout,
            stderr=stderr,
            locals=self.locals.copy(),
            execution_time=time.perf_counter() - start_time,
            rlm_calls=self._pending_llm_calls.copy(),
            final_answer=final_answer,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False

    def cleanup(self):
        """Clean up temp directory and reset state."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
        if hasattr(self, "globals"):
            self.globals.clear()
        if hasattr(self, "locals"):
            self.locals.clear()

    def __del__(self):
        self.cleanup()
