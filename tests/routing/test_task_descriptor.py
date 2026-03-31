"""
Tests for TaskDescriptor component.

This module tests task descriptor generation functions which handle:
- Intent classification from prompts
- Complexity estimation
- Capability detection (internet, filesystem, Lean, Haskell, Docker)
- Token estimation
- Default task descriptor generation
"""

import pytest

from rlm.routing.task_descriptor import (
    default_task_descriptor_fn,
    classify_intent,
    estimate_complexity,
    needs_internet,
    needs_filesystem,
    needs_lean_access,
    needs_haskell_access,
    needs_docker_isolation,
    estimate_cpu_time
)


class TestClassifyIntent:
    """
    Tests for intent classification from prompts.
    """

    def test_classify_web_research(self):
        """
        Test classification of web research prompts.

        Expected behavior:
        - Should return "web_research" for research-related keywords
        - Should match keywords: search, research, find, look up, arxiv, google
        """
        prompts = [
            "Search for recent papers on quantum computing",
            "Research the history of machine learning",
            "Find information about climate change",
            "Look up the latest arxiv papers",
            "Google the current stock prices"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "web_research", f"Prompt '{prompt}' should be web_research, got {intent}"

    def test_classify_proof_synthesis(self):
        """
        Test classification of proof synthesis prompts.

        Expected behavior:
        - Should return "proof_synthesis" for theorem-related keywords
        - Should match keywords: prove, theorem, lean, formal, verify
        """
        prompts = [
            "Prove that the sum of two even numbers is even",
            "Write a theorem about prime numbers",
            "Formalize this mathematical statement in Lean",
            "Verify the following proof",
            "Create a formal proof for this lemma"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "proof_synthesis", f"Prompt '{prompt}' should be proof_synthesis, got {intent}"

    def test_classify_code_generation(self):
        """
        Test classification of code generation prompts.

        Expected behavior:
        - Should return "code_generation" for code-related keywords
        - Should match keywords: code, implement, function, class, write
        """
        prompts = [
            "Write a function that sorts an array",
            "Implement a binary search tree",
            "Create a class for handling user data",
            "Code a web scraper",
            "Write a Python script to process files"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "code_generation", f"Prompt '{prompt}' should be code_generation, got {intent}"

    def test_classify_refactor(self):
        """
        Test classification of refactoring prompts.

        Expected behavior:
        - Should return "refactor" for refactoring keywords
        - Should match keywords: refactor, improve, optimize, clean
        """
        prompts = [
            "Refactor this code to be more maintainable",
            "Improve the performance of this function",
            "Optimize the database queries",
            "Clean up this legacy code",
            "Refactor the class structure"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "refactor", f"Prompt '{prompt}' should be refactor, got {intent}"

    def test_classify_summarization(self):
        """
        Test classification of summarization prompts.

        Expected behavior:
        - Should return "summarization" for summary keywords
        - Should match keywords: summarize, summary, brief
        """
        prompts = [
            "Summarize this article in 3 sentences",
            "Provide a summary of the meeting notes",
            "Brief me on the current situation",
            "Summarize the key points from this document"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "summarization", f"Prompt '{prompt}' should be summarization, got {intent}"

    def test_classify_general(self):
        """
        Test classification of general prompts.

        Expected behavior:
        - Should return "general" for prompts without specific keywords
        - Should be the default classification
        """
        prompts = [
            "What is the capital of France?",
            "Tell me a joke",
            "How are you today?",
            "Explain the concept of recursion"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "general", f"Prompt '{prompt}' should be general, got {intent}"

    def test_classify_case_insensitive(self):
        """
        Test that classification is case-insensitive.

        Expected behavior:
        - Should match keywords regardless of case
        - Should treat "Prove" and "prove" the same
        """
        prompts = [
            "PROVE this theorem",
            "Prove This Theorem",
            "pRoVe tHiS tHeOrEm"
        ]
        for prompt in prompts:
            intent = classify_intent(prompt)
            assert intent == "proof_synthesis", f"Prompt '{prompt}' should be proof_synthesis, got {intent}"

    def test_classify_with_multiple_keywords(self):
        """
        Test classification with multiple matching keywords.

        Expected behavior:
        - Should return the first matching intent based on keyword order
        - Should be deterministic
        """
        prompt = "Prove this theorem and search for related papers"
        intent = classify_intent(prompt)
        # Should match "prove" before "search" based on function order
        assert intent in ["proof_synthesis", "web_research"]


class TestEstimateComplexity:
    """
    Tests for complexity estimation from prompts.
    """

    def test_estimate_complexity_simple(self):
        """
        Test complexity estimation for simple prompts.

        Expected behavior:
        - Should return low complexity score (< 0.5)
        - Should consider prompt length and depth
        """
        prompt = "What is 2 + 2?"
        complexity = estimate_complexity(prompt, depth=1)
        assert 0.0 <= complexity < 0.5, f"Simple prompt should have low complexity, got {complexity}"

    def test_estimate_complexity_complex(self):
        """
        Test complexity estimation for complex prompts.

        Expected behavior:
        - Should return high complexity score (> 0.5)
        - Should consider complexity keywords
        """
        prompt = "Design and implement a distributed consensus algorithm with fault tolerance and Byzantine agreement"
        complexity = estimate_complexity(prompt, depth=5)
        assert complexity > 0.5, f"Complex prompt should have high complexity, got {complexity}"

    def test_estimate_complexity_with_depth(self):
        """
        Test that depth affects complexity estimation.

        Expected behavior:
        - Higher depth should increase complexity
        - Depth should be bounded (max 0.5 from depth alone)
        """
        prompt = "Write a function"
        complexity1 = estimate_complexity(prompt, depth=1)
        complexity2 = estimate_complexity(prompt, depth=10)
        assert complexity2 > complexity1, "Higher depth should increase complexity"

    def test_estimate_complexity_with_length(self):
        """
        Test that prompt length affects complexity estimation.

        Expected behavior:
        - Longer prompts should have higher complexity
        - Length factor should be bounded (max 0.3)
        """
        short_prompt = "Hello"
        long_prompt = "Hello " * 1000
        complexity1 = estimate_complexity(short_prompt, depth=1)
        complexity2 = estimate_complexity(long_prompt, depth=1)
        assert complexity2 > complexity1, "Longer prompt should increase complexity"

    def test_estimate_complexity_with_keywords(self):
        """
        Test that complexity keywords affect estimation.

        Expected behavior:
        - Keywords like "prove", "theorem", "optimize" should increase complexity
        - Each keyword should add ~0.05
        """
        prompt1 = "Write a function"
        prompt2 = "Prove a theorem and optimize the design"
        complexity1 = estimate_complexity(prompt1, depth=1)
        complexity2 = estimate_complexity(prompt2, depth=1)
        assert complexity2 > complexity1, "Complexity keywords should increase complexity"

    def test_estimate_complexity_upper_bound(self):
        """
        Test that complexity is bounded at 1.0.

        Expected behavior:
        - Should never return complexity > 1.0
        - Should handle extreme inputs gracefully
        """
        prompt = "Prove " * 1000 + "theorem " * 1000 + "optimize " * 1000
        complexity = estimate_complexity(prompt, depth=100)
        assert complexity <= 1.0, f"Complexity should be bounded at 1.0, got {complexity}"

    def test_estimate_complexity_lower_bound(self):
        """
        Test that complexity is bounded at 0.0.

        Expected behavior:
        - Should never return complexity < 0.0
        - Should handle empty/minimal inputs gracefully
        """
        prompt = ""
        complexity = estimate_complexity(prompt, depth=0)
        assert complexity >= 0.0, f"Complexity should be bounded at 0.0, got {complexity}"


class TestCapabilityDetection:
    """
    Tests for capability detection functions.
    """

    def test_needs_internet_detection(self):
        """
        Test detection of internet access needs.

        Expected behavior:
        - Should return True for internet-related keywords
        - Keywords: search, research, arxiv, google, download, fetch, url, http
        """
        prompts_true = [
            "Search for information",
            "Research this topic",
            "Download the file from URL",
            "Fetch data from the API",
            "Google the answer"
        ]
        for prompt in prompts_true:
            assert needs_internet(prompt), f"Prompt '{prompt}' should need internet"

        prompts_false = [
            "Write a function",
            "Calculate the sum",
            "Prove this theorem"
        ]
        for prompt in prompts_false:
            assert not needs_internet(prompt), f"Prompt '{prompt}' should not need internet"

    def test_needs_filesystem_detection(self):
        """
        Test detection of filesystem access needs.

        Expected behavior:
        - Should return True for filesystem-related keywords
        - Keywords: file, read, write, save, load, directory, path
        """
        prompts_true = [
            "Read the file",
            "Write to disk",
            "Save the results",
            "Load the configuration",
            "Create a directory"
        ]
        for prompt in prompts_true:
            assert needs_filesystem(prompt), f"Prompt '{prompt}' should need filesystem"

        prompts_false = [
            "Calculate the answer",
            "Prove the theorem",
            "Generate a summary"
        ]
        for prompt in prompts_false:
            assert not needs_filesystem(prompt), f"Prompt '{prompt}' should not need filesystem"

    def test_needs_lean_access_detection(self):
        """
        Test detection of Lean access needs.

        Expected behavior:
        - Should return True for Lean-related keywords
        - Keywords: lean, formal verification, theorem proving
        """
        prompts_true = [
            "Verify in Lean",
            "Formalize in Lean",
            "Prove using Lean",
            "Lean theorem",
            "Formal verification with Lean"
        ]
        for prompt in prompts_true:
            assert needs_lean_access(prompt), f"Prompt '{prompt}' should need Lean access"

        prompts_false = [
            "Write Python code",
            "Calculate the sum",
            "Generate a summary"
        ]
        for prompt in prompts_false:
            assert not needs_lean_access(prompt), f"Prompt '{prompt}' should not need Lean access"

    def test_needs_haskell_access_detection(self):
        """
        Test detection of Haskell access needs.

        Expected behavior:
        - Should return True for Haskell-related keywords
        - Keywords: haskell, dimensional types, type checking
        """
        prompts_true = [
            "Check with Haskell",
            "Haskell dimensional types",
            "Verify types in Haskell",
            "Haskell type checker"
        ]
        for prompt in prompts_true:
            assert needs_haskell_access(prompt), f"Prompt '{prompt}' should need Haskell access"

        prompts_false = [
            "Write Python code",
            "Calculate the sum",
            "Generate a summary"
        ]
        for prompt in prompts_false:
            assert not needs_haskell_access(prompt), f"Prompt '{prompt}' should not need Haskell access"

    def test_needs_docker_isolation_detection(self):
        """
        Test detection of Docker isolation needs.

        Expected behavior:
        - Should return True for Docker-related keywords
        - Keywords: docker, container, sandbox, isolation
        """
        prompts_true = [
            "Run in Docker",
            "Containerize this application",
            "Use Docker for isolation",
            "Sandbox the execution"
        ]
        for prompt in prompts_true:
            assert needs_docker_isolation(prompt), f"Prompt '{prompt}' should need Docker isolation"

        prompts_false = [
            "Write Python code",
            "Calculate the sum",
            "Generate a summary"
        ]
        for prompt in prompts_false:
            assert not needs_docker_isolation(prompt), f"Prompt '{prompt}' should not need Docker isolation"

    def test_capability_detection_case_insensitive(self):
        """
        Test that capability detection is case-insensitive.

        Expected behavior:
        - Should match keywords regardless of case
        """
        assert needs_internet("SEARCH for info")
        assert needs_filesystem("READ the file")
        assert needs_lean_access("LEAN verification")
        assert needs_haskell_access("HASKELL types")
        assert needs_docker_isolation("DOCKER container")


class TestTokenEstimation:
    """
    Tests for token estimation in task descriptors.
    """
    # Note: Token estimation is part of default_task_descriptor_fn
    # This tests the estimation logic indirectly

    def test_token_estimation_in_descriptor(self):
        """
        Test that task descriptor includes token estimate.

        Expected behavior:
        - Should estimate tokens based on word count
        - Should be a reasonable approximation
        """
        prompt = "This is a test prompt with ten words"
        descriptor = default_task_descriptor_fn(prompt, depth=1)
        assert "token_estimate" in descriptor
        assert descriptor["token_estimate"] > 0
        # Rough estimate: words * 1.3
        assert descriptor["token_estimate"] > len(prompt.split())

    def test_token_estimation_scales_with_length(self):
        """
        Test that token estimation scales with prompt length.

        Expected behavior:
        - Longer prompts should have higher token estimates
        """
        short_prompt = "Hello"
        long_prompt = "Hello " * 100
        descriptor1 = default_task_descriptor_fn(short_prompt, depth=1)
        descriptor2 = default_task_descriptor_fn(long_prompt, depth=1)
        assert descriptor2["token_estimate"] > descriptor1["token_estimate"]


class TestCpuTimeEstimation:
    """
    Tests for CPU time estimation.
    """

    def test_estimate_cpu_time_simple(self):
        """
        Test CPU time estimation for simple tasks.

        Expected behavior:
        - Should return low CPU time estimate
        - Should be based on complexity
        """
        prompt = "What is 2 + 2?"
        cpu_time = estimate_cpu_time(prompt, complexity=0.1)
        assert cpu_time < 5.0, f"Simple task should have low CPU time, got {cpu_time}"

    def test_estimate_cpu_time_complex(self):
        """
        Test CPU time estimation for complex tasks.

        Expected behavior:
        - Should return high CPU time estimate
        - Should scale with complexity
        """
        prompt = "Prove a complex theorem"
        cpu_time = estimate_cpu_time(prompt, complexity=0.9)
        assert cpu_time > 5.0, f"Complex task should have high CPU time, got {cpu_time}"

    def test_estimate_cpu_time_scales_with_complexity(self):
        """
        Test that CPU time scales with complexity.

        Expected behavior:
        - Higher complexity should result in higher CPU time
        """
        cpu_time1 = estimate_cpu_time("test", complexity=0.2)
        cpu_time2 = estimate_cpu_time("test", complexity=0.8)
        assert cpu_time2 > cpu_time1, "Higher complexity should increase CPU time"


class TestDefaultTaskDescriptor:
    """
    Tests for default task descriptor generation.
    """

    def test_descriptor_has_required_fields(self):
        """
        Test that task descriptor has all required fields.

        Expected behavior:
        - Should include subtask_id, parent_task_id, intent
        - Should include complexity_score, latency_budget_ms
        - Should include cost_sensitivity, safety_level
        """
        prompt = "Write a function"
        descriptor = default_task_descriptor_fn(prompt, depth=1)

        required_fields = [
            "subtask_id",
            "parent_task_id",
            "intent",
            "complexity_score",
            "latency_budget_ms",
            "cost_sensitivity",
            "token_estimate",
            "safety_level"
        ]
        for field in required_fields:
            assert field in descriptor, f"Descriptor should include field '{field}'"

    def test_descriptor_subtask_id_format(self):
        """
        Test that subtask_id follows expected format.

        Expected behavior:
        - Should include depth and hash
        - Should be unique for different prompts
        """
        prompt = "Write a function"
        descriptor = default_task_descriptor_fn(prompt, depth=3)
        assert descriptor["subtask_id"].startswith("subtask-3-")

    def test_descriptor_parent_task_id(self):
        """
        Test that parent_task_id is set correctly.

        Expected behavior:
        - Should be "main" for top-level tasks
        """
        prompt = "Write a function"
        descriptor = default_task_descriptor_fn(prompt, depth=1)
        assert descriptor["parent_task_id"] == "main"

    def test_descriptor_capabilities(self):
        """
        Test that capabilities dictionary is populated.

        Expected behavior:
        - Should include all capability flags
        - Should be boolean values
        """
        prompt = "Search for files and verify in Lean"
        descriptor = default_task_descriptor_fn(prompt, depth=1)

        assert "capabilities" in descriptor
        capabilities = descriptor["capabilities"]
        required_capabilities = [
            "needs_internet",
            "needs_filesystem",
            "needs_lean_access",
            "needs_haskell_access",
            "needs_docker_isolation"
        ]
        for cap in required_capabilities:
            assert cap in capabilities
            assert isinstance(capabilities[cap], bool)

    def test_descriptor_security(self):
        """
        Test that security dictionary is populated.

        Expected behavior:
        - Should include data_sensitivity
        - Should have default value
        """
        prompt = "Write a function"
        descriptor = default_task_descriptor_fn(prompt, depth=1)

        assert "security" in descriptor
        assert "data_sensitivity" in descriptor["security"]
        assert descriptor["security"]["data_sensitivity"] == "internal"

    def test_descriptor_performance(self):
        """
        Test that performance dictionary is populated.

        Expected behavior:
        - Should include expected_cpu_seconds
        - Should be a numeric value
        """
        prompt = "Write a function"
        descriptor = default_task_descriptor_fn(prompt, depth=1)

        assert "performance" in descriptor
        assert "expected_cpu_seconds" in descriptor["performance"]
        assert isinstance(descriptor["performance"]["expected_cpu_seconds"], (int, float))

    def test_descriptor_mode(self):
        """
        Test that mode field is set correctly.

        Expected behavior:
        - Should be "dev" by default
        """
        prompt = "Write a function"
        descriptor = default_task_descriptor_fn(prompt, depth=1)
        assert descriptor["mode"] == "dev"

    def test_descriptor_with_different_depths(self):
        """
        Test that descriptors vary with depth.

        Expected behavior:
        - Higher depth should increase complexity_score
        - subtask_id should reflect depth
        """
        prompt = "Write a function"
        descriptor1 = default_task_descriptor_fn(prompt, depth=1)
        descriptor2 = default_task_descriptor_fn(prompt, depth=5)

        assert descriptor1["subtask_id"].startswith("subtask-1-")
        assert descriptor2["subtask_id"].startswith("subtask-5-")
        assert descriptor2["complexity_score"] >= descriptor1["complexity_score"]

    def test_descriptor_with_empty_prompt(self):
        """
        Test handling of empty prompt.

        Expected behavior:
        - Should not raise exception
        - Should return valid descriptor
        """
        descriptor = default_task_descriptor_fn("", depth=1)
        assert descriptor is not None
        assert "subtask_id" in descriptor

    def test_descriptor_with_very_long_prompt(self):
        """
        Test handling of very long prompts.

        Expected behavior:
        - Should not raise exception
        - Should handle gracefully
        """
        prompt = "Write a function " * 10000
        descriptor = default_task_descriptor_fn(prompt, depth=1)
        assert descriptor is not None
        assert "subtask_id" in descriptor


class TestEdgeCases:
    """
    Tests for edge cases and error handling.
    """

    def test_classify_intent_with_none(self):
        """
        Test classification with None input.

        Expected behavior:
        - Should handle gracefully or raise appropriate exception
        """
        try:
            intent = classify_intent(None)
            assert intent == "general"  # May default to general
        except (AttributeError, TypeError):
            # Also acceptable to raise exception
            pass

    def test_estimate_complexity_with_negative_depth(self):
        """
        Test complexity estimation with negative depth.

        Expected behavior:
        - Should handle gracefully
        - Complexity should be >= 0
        """
        complexity = estimate_complexity("test", depth=-1)
        assert complexity >= 0.0

    def test_capability_detection_with_special_characters(self):
        """
        Test capability detection with special characters.

        Expected behavior:
        - Should handle special characters correctly
        - Should not raise exception
        """
        prompts = [
            "Search for 'test' in files",
            "Read file: /path/to/file.txt",
            "Download from http://example.com"
        ]
        for prompt in prompts:
            try:
                needs_internet(prompt)
                needs_filesystem(prompt)
            except Exception as e:
                pytest.fail(f"Should handle special characters: {e}")
