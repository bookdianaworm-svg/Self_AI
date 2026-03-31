"""
Mock Language Model for testing without real LLM calls.

This module provides a simple mock implementation of BaseLM that can be
used in tests to avoid making actual API calls to LLM providers.
"""

from rlm.clients.base_lm import BaseLM
from rlm.core.types import ModelUsageSummary, UsageSummary


class MockLM(BaseLM):
    """
    Simple mock LM that echoes prompts for testing purposes.

    This mock implementation returns deterministic responses based on the
    input prompt, allowing tests to verify behavior without making actual
    LLM API calls.
    """

    def __init__(self, model_name: str = "mock-model"):
        """
        Initialize MockLM with a model name.

        Args:
            model_name: Name to use for this mock model
        """
        super().__init__(model_name=model_name)
        self.call_count = 0

    def completion(self, prompt: str) -> str:
        """
        Return a mock response to the given prompt.

        Args:
            prompt: The input prompt

        Returns:
            A deterministic response based on the prompt
        """
        self.call_count += 1
        # Truncate prompt for cleaner output
        prompt_preview = prompt[:50] if len(prompt) > 50 else prompt
        return f"Mock response to: {prompt_preview}"

    async def acompletion(self, prompt: str) -> str:
        """
        Async version of completion.

        Args:
            prompt: The input prompt

        Returns:
            A deterministic response based on the prompt
        """
        return self.completion(prompt)

    def get_usage_summary(self) -> UsageSummary:
        """
        Return a mock usage summary.

        Returns:
            UsageSummary with mock data
        """
        return UsageSummary(
            model_usage_summaries={
                self.model_name: ModelUsageSummary(
                    total_calls=self.call_count,
                    total_input_tokens=self.call_count * 10,
                    total_output_tokens=self.call_count * 10
                )
            }
        )

    def get_last_usage(self) -> UsageSummary:
        """
        Return usage summary for the last call.

        Returns:
            UsageSummary with mock data
        """
        return self.get_usage_summary()


class MockLMWithResponse(BaseLM):
    """
    Mock LM that returns predefined responses for testing.

    This allows tests to specify exact responses for different prompts.
    """

    def __init__(self, responses: dict[str, str], model_name: str = "mock-with-response"):
        """
        Initialize MockLMWithResponse with predefined responses.

        Args:
            responses: Dictionary mapping prompts to responses
            model_name: Name to use for this mock model
        """
        super().__init__(model_name=model_name)
        self.responses = responses
        self.call_count = 0
        self.call_history = []

    def completion(self, prompt: str) -> str:
        """
        Return the predefined response for the given prompt.

        Args:
            prompt: The input prompt

        Returns:
            The predefined response or a default if not found
        """
        self.call_count += 1
        self.call_history.append(prompt)
        return self.responses.get(prompt, f"Mock response to: {prompt[:50]}")

    async def acompletion(self, prompt: str) -> str:
        """
        Async version of completion.

        Args:
            prompt: The input prompt

        Returns:
            The predefined response or a default if not found
        """
        return self.completion(prompt)

    def get_usage_summary(self) -> UsageSummary:
        """
        Return a mock usage summary.

        Returns:
            UsageSummary with mock data
        """
        return UsageSummary(
            model_usage_summaries={
                self.model_name: ModelUsageSummary(
                    total_calls=self.call_count,
                    total_input_tokens=self.call_count * 10,
                    total_output_tokens=self.call_count * 10
                )
            }
        )

    def get_last_usage(self) -> UsageSummary:
        """
        Return usage summary for the last call.

        Returns:
            UsageSummary with mock data
        """
        return self.get_usage_summary()
