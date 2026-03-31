"""
Agent loop callback handler middleware.

Bridges RLM callbacks to Redux store and SQLite storage.
"""

import time
import uuid
from typing import Any, Callable, Dict, List, Optional

from rlm.redux.slices.agent_loop_slice import (
    AgentLoopActions,
    AgentLoopSlice,
    AgentLoopStatus,
    generate_call_id,
    generate_chain_thought_id,
    generate_execution_id,
    generate_iteration_id,
)
from rlm.storage.agent_loop_storage import AgentLoopStorage
from rlm.utils.chain_of_thought import (
    extract_chain_of_thought,
    extract_reasoning_context,
    identify_action_from_response,
)


class AgentLoopCallbacks:
    """Callback handler that bridges RLM callbacks to Redux and SQLite."""

    def __init__(
        self,
        store: Any,
        agent_id: str,
        agent_name: str,
        depth: int = 0,
        task: str = "",
        parent_id: Optional[str] = None,
        storage: Optional[AgentLoopStorage] = None,
    ):
        self.store = store
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.depth = depth
        self.parent_id = parent_id
        self.storage = storage or AgentLoopStorage(enabled=True)

        self.parent_call_id: Optional[str] = None
        self.current_iteration: Optional[int] = None
        self.current_iteration_id: Optional[str] = None
        self.current_call_id: Optional[str] = None
        self.iteration_start_time: float = 0.0
        self.call_start_time: float = 0.0

        self._register_agent(task)

    def _register_agent(self, task: str):
        """Register this agent with the Redux store."""
        self.store.dispatch(
            AgentLoopActions.register_agent(
                agent_id=self.agent_id,
                agent_name=self.agent_name,
                depth=self.depth,
                task=task,
                parent_id=self.parent_id,
            )
        )

    def _get_slice_state(self) -> AgentLoopSlice:
        """Get the agent loop slice from store."""
        return self.store.get_state().agent_loop

    def on_iteration_start(self, iteration_number: int, prompt: str) -> str:
        """Called when an iteration starts.

        Returns:
            The iteration ID for this iteration.
        """
        self.current_iteration = iteration_number
        self.iteration_start_time = time.time()

        slice_state = self._get_slice_state()
        iteration_id = generate_iteration_id(slice_state)

        self.store.dispatch(
            AgentLoopActions.iteration_started(
                agent_id=self.agent_id,
                iteration_id=iteration_id,
                iteration_number=iteration_number,
                depth=self.depth,
                prompt=prompt,
            )
        )

        self.storage.save_iteration(
            {
                "iteration_id": iteration_id,
                "agent_id": self.agent_id,
                "iteration_number": iteration_number,
                "depth": self.depth,
                "prompt": prompt,
                "response": "",
                "code_blocks": [],
                "final_answer": None,
                "execution_time": 0.0,
                "timestamp": self.iteration_start_time,
            }
        )

        return iteration_id

    def on_iteration_complete(
        self,
        iteration_id: str,
        response: str,
        code_blocks: List[Dict[str, Any]],
        final_answer: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Called when an iteration completes.

        Returns:
            List of extracted chain-of-thought steps.
        """
        execution_time = time.time() - self.iteration_start_time

        self.store.dispatch(
            AgentLoopActions.iteration_completed(
                agent_id=self.agent_id,
                iteration_id=iteration_id,
                response=response,
                code_blocks=code_blocks,
                final_answer=final_answer,
                execution_time=execution_time,
            )
        )

        self.storage.save_iteration(
            {
                "iteration_id": iteration_id,
                "agent_id": self.agent_id,
                "iteration_number": self.current_iteration or 0,
                "depth": self.depth,
                "prompt": "",
                "response": response,
                "code_blocks": code_blocks,
                "final_answer": final_answer,
                "execution_time": execution_time,
                "timestamp": time.time(),
            }
        )

        chain_thought_steps = self._extract_and_save_chain_thought(
            response, code_blocks, iteration_id
        )

        return chain_thought_steps

    def _extract_and_save_chain_thought(
        self, response: str, code_blocks: List[Dict[str, Any]], iteration_id: str
    ) -> List[Dict[str, Any]]:
        """Extract and save chain-of-thought steps."""
        steps = []
        thoughts = extract_chain_of_thought(response)
        action = identify_action_from_response(response)
        context = extract_reasoning_context(
            response, [b.get("code", "") for b in code_blocks]
        )

        slice_state = self._get_slice_state()

        for thought in thoughts:
            step_id = generate_chain_thought_id(slice_state)
            self.store.dispatch(
                AgentLoopActions.chain_thought_added(
                    agent_id=self.agent_id,
                    step_id=step_id,
                    iteration=self.current_iteration or 0,
                    thought=thought,
                    action=action,
                    context=context,
                )
            )

            self.storage.save_chain_thought(
                {
                    "step_id": step_id,
                    "agent_id": self.agent_id,
                    "iteration": self.current_iteration or 0,
                    "thought": thought,
                    "action": action,
                    "context": context,
                    "timestamp": time.time(),
                }
            )

            steps.append(
                {
                    "step_id": step_id,
                    "thought": thought,
                    "action": action,
                    "context": context,
                }
            )

        return steps

    def on_llm_call_start(
        self, model: str, prompt: str, call_type: str = "completion"
    ) -> str:
        """Called when an LLM call starts.

        Returns:
            The call ID for this LLM call.
        """
        self.call_start_time = time.time()

        slice_state = self._get_slice_state()
        call_id = generate_call_id(slice_state)
        self.current_call_id = call_id

        self.store.dispatch(
            AgentLoopActions.llm_call_started(
                agent_id=self.agent_id,
                call_id=call_id,
                parent_call_id=self.parent_call_id,
                depth=self.depth,
                model=model,
                prompt=prompt,
                call_type=call_type,
            )
        )

        return call_id

    def on_llm_call_complete(
        self,
        call_id: str,
        response: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: Optional[float] = None,
        success: bool = True,
        error: Optional[str] = None,
    ):
        """Called when an LLM call completes."""
        execution_time = time.time() - self.call_start_time

        self.store.dispatch(
            AgentLoopActions.llm_call_completed(
                agent_id=self.agent_id,
                call_id=call_id,
                response=response,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                execution_time=execution_time,
                success=success,
                error=error,
            )
        )

        self.storage.save_llm_call(
            {
                "call_id": call_id,
                "agent_id": self.agent_id,
                "parent_call_id": self.parent_call_id,
                "depth": self.depth,
                "model": "",  # Will be filled from the started event
                "prompt": "",  # Will be filled from the started event
                "response": response,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "execution_time": execution_time,
                "call_type": "",  # Will be filled from the started event
                "success": success,
                "error": error,
                "timestamp": time.time(),
            }
        )

    def on_repl_execution_start(
        self, code: str, parent_call_id: Optional[str] = None
    ) -> str:
        """Called when a REPL execution starts.

        Returns:
            The execution ID for this REPL execution.
        """
        slice_state = self._get_slice_state()
        execution_id = generate_execution_id(slice_state)

        self.store.dispatch(
            AgentLoopActions.repl_execution_started(
                agent_id=self.agent_id,
                execution_id=execution_id,
                parent_call_id=parent_call_id or self.current_call_id,
                code=code,
            )
        )

        return execution_id

    def on_repl_execution_complete(
        self,
        execution_id: str,
        stdout: str,
        stderr: str,
        execution_time: float,
        success: bool,
        error: Optional[str] = None,
        return_value_preview: Optional[str] = None,
        llm_calls_made: Optional[List[str]] = None,
    ):
        """Called when a REPL execution completes."""
        self.store.dispatch(
            AgentLoopActions.repl_execution_completed(
                agent_id=self.agent_id,
                execution_id=execution_id,
                stdout=stdout,
                stderr=stderr,
                execution_time=execution_time,
                success=success,
                error=error,
                return_value_preview=return_value_preview,
                llm_calls_made=llm_calls_made or [],
            )
        )

        self.storage.save_repl_execution(
            {
                "execution_id": execution_id,
                "agent_id": self.agent_id,
                "parent_call_id": self.current_call_id,
                "code": "",  # Will be filled from the started event
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": execution_time,
                "success": success,
                "error": error,
                "return_value_preview": return_value_preview,
                "llm_calls_made": llm_calls_made or [],
                "timestamp": time.time(),
            }
        )

    def on_subcall_start(self, depth: int, model: str, prompt_preview: str) -> str:
        """Called when a subcall (child RLM) starts.

        Returns:
            The call ID for tracking this subcall.
        """
        self.call_start_time = time.time()

        slice_state = self._get_slice_state()
        call_id = generate_call_id(slice_state)
        self.current_call_id = call_id

        self.store.dispatch(
            AgentLoopActions.llm_call_started(
                agent_id=self.agent_id,
                call_id=call_id,
                parent_call_id=self.parent_call_id,
                depth=depth,
                model=model,
                prompt=prompt_preview,
                call_type="subcall",
            )
        )

        return call_id

    def on_subcall_complete(
        self, depth: int, model: str, duration: float, error: Optional[str]
    ):
        """Called when a subcall (child RLM) completes."""
        self.store.dispatch(
            AgentLoopActions.llm_call_completed(
                agent_id=self.agent_id,
                call_id=self.current_call_id or "",
                response="",
                input_tokens=0,
                output_tokens=0,
                cost=None,
                execution_time=duration,
                success=error is None,
                error=error,
            )
        )

    def on_agent_spawned(self, child_agent_id: str, child_task: str, reason: str):
        """Called when this agent spawns a child agent."""
        extracted_reason = extract_reasoning_context(
            f"Spawning agent for: {child_task}", []
        )

        self.store.dispatch(
            AgentLoopActions.agent_spawned(
                parent_agent_id=self.agent_id,
                child_agent_id=child_agent_id,
                child_task=child_task,
                reason=reason or "Task delegation",
            )
        )

        self.storage.save_spawning_event(
            {
                "event_id": str(uuid.uuid4()),
                "parent_agent_id": self.agent_id,
                "child_agent_id": child_agent_id,
                "child_task": child_task,
                "reason": reason or "Task delegation",
                "timestamp": time.time(),
            }
        )

    def on_status_change(self, status: AgentLoopStatus):
        """Update agent status in the store."""
        self.store.dispatch(
            AgentLoopActions.update_agent_status(agent_id=self.agent_id, status=status)
        )


def create_loop_handler(
    store: Any,
    agent_id: str,
    agent_name: str,
    depth: int = 0,
    task: str = "",
    parent_id: Optional[str] = None,
    storage: Optional[AgentLoopStorage] = None,
) -> AgentLoopCallbacks:
    """Factory function to create an agent loop callback handler.

    Args:
        store: The Redux store instance.
        agent_id: Unique identifier for this agent.
        agent_name: Human-readable name for this agent.
        depth: Current recursion depth.
        task: The task this agent is working on.
        parent_id: ID of the parent agent (if any).
        storage: Optional SQLite storage instance.

    Returns:
        AgentLoopCallbacks instance with all callback methods.
    """
    return AgentLoopCallbacks(
        store=store,
        agent_id=agent_id,
        agent_name=agent_name,
        depth=depth,
        task=task,
        parent_id=parent_id,
        storage=storage,
    )
