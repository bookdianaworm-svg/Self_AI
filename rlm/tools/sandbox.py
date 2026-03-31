# Tool Sandbox for safe execution
import sys
import threading
from contextlib import contextmanager
from typing import Any, Dict, Optional
import io


class ToolSandbox:
    """
    Sandboxed environment for executing dynamically created tools.
    """

    def __init__(self, timeout: float = 30.0, memory_limit_mb: int = 512):
        self.timeout = timeout
        self.memory_limit_mb = memory_limit_mb
        self._local = {}

    @contextmanager
    def execution_context(self, tool_function: callable, **globals):
        """Execute a tool in a restricted context."""
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()

            result = None
            error = None

            def run():
                nonlocal result, error
                try:
                    result = tool_function(**globals)
                except Exception as e:
                    error = e

            thread = threading.Thread(target=run)
            thread.daemon = True
            thread.start()
            thread.join(timeout=self.timeout)

            if thread.is_alive():
                raise TimeoutError(f"Tool execution timed out after {self.timeout}s")

            if error:
                raise error

            yield result

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def execute(self, tool_function: callable, **kwargs) -> Any:
        """Execute a tool safely."""
        with self.execution_context(tool_function, **kwargs) as result:
            return result
