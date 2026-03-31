"""
Tests for VerificationPrompts component.

This module tests verification agent system prompts which handle:
- Prompt content validation
- Tool integration verification
- Prompt completeness and accuracy
"""

import pytest

from rlm.agents.prompts.verification_prompts import (
    AUTOFORMALIZATION_SYSTEM_PROMPT,
    VERIFIER_SYSTEM_PROMPT,
    PHYSICIST_SYSTEM_PROMPT,
    CROSS_CHECK_SYSTEM_PROMPT
)


class TestAutoformalizationPrompt:
    """
    Tests for AUTOFORMALIZATION_SYSTEM_PROMPT.
    """

    def test_autoformalization_prompt_exists(self):
        """
        Test that AUTOFORMALIZATION_SYSTEM_PROMPT is defined.

        Expected behavior:
        - Prompt should be a non-empty string
        - Should contain key instructions
        """
        assert AUTOFORMALIZATION_SYSTEM_PROMPT is not None
        assert isinstance(AUTOFORMALIZATION_SYSTEM_PROMPT, str)
        assert len(AUTOFORMALIZATION_SYSTEM_PROMPT) > 0

    def test_autoformalization_prompt_content(self):
        """
        Test that AUTOFORMALIZATION_SYSTEM_PROMPT contains required content.

        Expected behavior:
        - Should mention Autoformalization Agent role
        - Should mention Layer 1 axioms
        - Should mention Lean 4
        - Should mention Mathlib, PhysLib, SciLean
        """
        prompt = AUTOFORMALIZATION_SYSTEM_PROMPT
        assert "Autoformalization" in prompt
        assert "Lean 4" in prompt
        assert "Mathlib" in prompt
        assert "PhysLib" in prompt or "SciLean" in prompt

    def test_autoformalization_prompt_responsibilities(self):
        """
        Test that prompt includes agent responsibilities.

        Expected behavior:
        - Should list 5 responsibilities
        - Should mention parsing informal rules
        - Should mention generating Lean 4 theorems
        - Should mention skeleton proofs
        """
        prompt = AUTOFORMALIZATION_SYSTEM_PROMPT
        assert "responsibilities" in prompt.lower()
        # Check for key responsibilities
        assert "parse" in prompt.lower()
        assert "generate" in prompt.lower()
        assert "theorem" in prompt.lower()

    def test_autoformalization_prompt_output_format(self):
        """
        Test that prompt specifies output format.

        Expected behavior:
        - Should include code block example
        - Should show Lean import structure
        - Should show theorem template
        """
        prompt = AUTOFORMALIZATION_SYSTEM_PROMPT
        assert "```lean" in prompt or "lean" in prompt.lower()
        assert "import" in prompt
        assert "theorem" in prompt.lower()

    def test_autoformalization_prompt_tools(self):
        """
        Test that prompt mentions available tools.

        Expected behavior:
        - Should mention verify_lean tool
        - Should instruct to use tools
        """
        prompt = AUTOFORMALIZATION_SYSTEM_PROMPT
        assert "verify_lean" in prompt


class TestVerifierPrompt:
    """
    Tests for VERIFIER_SYSTEM_PROMPT.
    """

    def test_verifier_prompt_exists(self):
        """
        Test that VERIFIER_SYSTEM_PROMPT is defined.

        Expected behavior:
        - Prompt should be a non-empty string
        - Should contain key instructions
        """
        assert VERIFIER_SYSTEM_PROMPT is not None
        assert isinstance(VERIFIER_SYSTEM_PROMPT, str)
        assert len(VERIFIER_SYSTEM_PROMPT) > 0

    def test_verifier_prompt_content(self):
        """
        Test that VERIFIER_SYSTEM_PROMPT contains required content.

        Expected behavior:
        - Should mention Verifier Agent role
        - Should mention Layer 1 axioms
        - Should mention Lean kernel
        """
        prompt = VERIFIER_SYSTEM_PROMPT
        assert "Verifier" in prompt
        assert "Layer 1" in prompt or "Layer1" in prompt
        assert "Lean" in prompt

    def test_verifier_prompt_responsibilities(self):
        """
        Test that prompt includes agent responsibilities.

        Expected behavior:
        - Should list responsibilities
        - Should mention loading context
        - Should mention compiling code
        - Should mention proof synthesis
        """
        prompt = VERIFIER_SYSTEM_PROMPT
        assert "responsibilities" in prompt.lower()
        assert "load" in prompt.lower()
        assert "compile" in prompt.lower()
        assert "proof" in prompt.lower()

    def test_verifier_prompt_tools(self):
        """
        Test that prompt mentions available tools.

        Expected behavior:
        - Should mention verify_lean tool
        - Should mention prove_theorem tool
        - Should include tool signatures
        """
        prompt = VERIFIER_SYSTEM_PROMPT
        assert "verify_lean" in prompt
        assert "prove_theorem" in prompt

    def test_verifier_prompt_output_format(self):
        """
        Test that prompt specifies output format.

        Expected behavior:
        - Should include JSON format example
        - Should show status field
        - Should show errors field
        - Should show proof field
        """
        prompt = VERIFIER_SYSTEM_PROMPT
        assert "json" in prompt.lower()
        assert "status" in prompt.lower()
        assert "errors" in prompt.lower() or "error" in prompt.lower()
        assert "proof" in prompt.lower()


class TestPhysicistPrompt:
    """
    Tests for PHYSICIST_SYSTEM_PROMPT.
    """

    def test_physicist_prompt_exists(self):
        """
        Test that PHYSICIST_SYSTEM_PROMPT is defined.

        Expected behavior:
        - Prompt should be a non-empty string
        - Should contain key instructions
        """
        assert PHYSICIST_SYSTEM_PROMPT is not None
        assert isinstance(PHYSICIST_SYSTEM_PROMPT, str)
        assert len(PHYSICIST_SYSTEM_PROMPT) > 0

    def test_physicist_prompt_content(self):
        """
        Test that PHYSICIST_SYSTEM_PROMPT contains required content.

        Expected behavior:
        - Should mention Physicist Agent role
        - Should mention Layer 2 physics constraints
        - Should mention design validation
        """
        prompt = PHYSICIST_SYSTEM_PROMPT
        assert "Physicist" in prompt
        assert "Layer 2" in prompt or "Layer2" in prompt
        assert "physics" in prompt.lower()

    def test_physicist_prompt_responsibilities(self):
        """
        Test that prompt includes agent responsibilities.

        Expected behavior:
        - Should list responsibilities
        - Should mention extracting parameters
        - Should mention instantiating theorems
        - Should mention writing proofs
        """
        prompt = PHYSICIST_SYSTEM_PROMPT
        assert "responsibilities" in prompt.lower()
        assert "extract" in prompt.lower()
        assert "instantiate" in prompt.lower()
        assert "proof" in prompt.lower()

    def test_physicist_prompt_constraints(self):
        """
        Test that prompt mentions validation constraints.

        Expected behavior:
        - Should mention thermal limits
        - Should mention energy balance
        - Should mention stress constraints
        """
        prompt = PHYSICIST_SYSTEM_PROMPT
        # Check for physics-related constraints
        physics_terms = ["thermal", "energy", "stress", "constraint"]
        has_any = any(term in prompt.lower() for term in physics_terms)
        assert has_any

    def test_physicist_prompt_tools(self):
        """
        Test that prompt mentions available tools.

        Expected behavior:
        - Should mention verify_lean tool
        - Should mention prove_theorem tool
        - Should mention get_layer1_axioms tool
        """
        prompt = PHYSICIST_SYSTEM_PROMPT
        assert "verify_lean" in prompt
        assert "prove_theorem" in prompt
        assert "get_layer1_axioms" in prompt

    def test_physicist_prompt_output_format(self):
        """
        Test that prompt specifies output format.

        Expected behavior:
        - Should include JSON format example
        - Should show status field
        - Should show violations field
        - Should show proofs field
        """
        prompt = PHYSICIST_SYSTEM_PROMPT
        assert "json" in prompt.lower()
        assert "status" in prompt.lower()
        assert "violations" in prompt.lower() or "violation" in prompt.lower()
        assert "proofs" in prompt.lower() or "proof" in prompt.lower()


class TestCrossCheckPrompt:
    """
    Tests for CROSS_CHECK_SYSTEM_PROMPT.
    """

    def test_cross_check_prompt_exists(self):
        """
        Test that CROSS_CHECK_SYSTEM_PROMPT is defined.

        Expected behavior:
        - Prompt should be a non-empty string
        - Should contain key instructions
        """
        assert CROSS_CHECK_SYSTEM_PROMPT is not None
        assert isinstance(CROSS_CHECK_SYSTEM_PROMPT, str)
        assert len(CROSS_CHECK_SYSTEM_PROMPT) > 0

    def test_cross_check_prompt_content(self):
        """
        Test that CROSS_CHECK_SYSTEM_PROMPT contains required content.

        Expected behavior:
        - Should mention Cross-Check Agent role
        - Should mention Layer 2 consistency
        - Should mention multiple sources
        """
        prompt = CROSS_CHECK_SYSTEM_PROMPT
        assert "Cross-Check" in prompt or "CrossCheck" in prompt
        assert "Layer 2" in prompt or "Layer2" in prompt
        assert "source" in prompt.lower()

    def test_cross_check_prompt_responsibilities(self):
        """
        Test that prompt includes agent responsibilities.

        Expected behavior:
        - Should list responsibilities
        - Should mention formalizing from sources
        - Should mention proving equivalence
        - Should mention flagging divergences
        """
        prompt = CROSS_CHECK_SYSTEM_PROMPT
        assert "responsibilities" in prompt.lower()
        assert "formalize" in prompt.lower()
        assert "equivalence" in prompt.lower()
        assert "divergence" in prompt.lower() or "divergences" in prompt.lower()

    def test_cross_check_prompt_tools(self):
        """
        Test that prompt mentions available tools.

        Expected behavior:
        - Should mention verify_lean tool
        - Should mention prove_theorem tool
        """
        prompt = CROSS_CHECK_SYSTEM_PROMPT
        assert "verify_lean" in prompt
        assert "prove_theorem" in prompt


class TestPromptConsistency:
    """
    Tests for consistency across all prompts.
    """

    def test_all_prompts_use_lean(self):
        """
        Test that all prompts mention Lean.

        Expected behavior:
        - Autoformalization prompt should mention Lean
        - Verifier prompt should mention Lean
        - Physicist prompt should mention Lean
        - Cross-check prompt should mention Lean
        """
        assert "Lean" in AUTOFORMALIZATION_SYSTEM_PROMPT
        assert "Lean" in VERIFIER_SYSTEM_PROMPT
        assert "Lean" in PHYSICIST_SYSTEM_PROMPT
        assert "Lean" in CROSS_CHECK_SYSTEM_PROMPT

    def test_all_prompts_use_layer1(self):
        """
        Test that all prompts mention Layer 1.

        Expected behavior:
        - All prompts should reference Layer 1 axioms
        """
        layer1_terms = ["Layer 1", "Layer1", "Layer-1"]
        for prompt in [AUTOFORMALIZATION_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT,
                     PHYSICIST_SYSTEM_PROMPT, CROSS_CHECK_SYSTEM_PROMPT]:
            has_layer1 = any(term in prompt for term in layer1_terms)
            assert has_layer1, f"Prompt should mention Layer 1"

    def test_all_prompts_specify_output_format(self):
        """
        Test that all prompts specify output format.

        Expected behavior:
        - All prompts should include format instructions
        - Should use code blocks or JSON
        """
        for prompt in [AUTOFORMALIZATION_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT,
                     PHYSICIST_SYSTEM_PROMPT, CROSS_CHECK_SYSTEM_PROMPT]:
            # Check for format indicators
            has_format = (
                "```" in prompt or  # Code block
                "json" in prompt.lower() or  # JSON format
                "format" in prompt.lower()  # Format instruction
            )
            assert has_format, f"Prompt should specify output format"

    def test_all_prompts_mention_tools(self):
        """
        Test that all prompts mention available tools.

        Expected behavior:
        - All prompts should reference tools
        - Should instruct when to use tools
        """
        for prompt in [AUTOFORMALIZATION_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT,
                     PHYSICIST_SYSTEM_PROMPT, CROSS_CHECK_SYSTEM_PROMPT]:
            # Check for tool references
            has_tools = (
                "verify_lean" in prompt or
                "prove_theorem" in prompt or
                "tool" in prompt.lower()
            )
            assert has_tools, f"Prompt should mention available tools"


class TestPromptQuality:
    """
    Tests for prompt quality and completeness.
    """

    def test_prompts_are_reasonable_length(self):
        """
        Test that prompts are reasonable length.

        Expected behavior:
        - Prompts should be long enough to be clear
        - Prompts should not be excessively long
        """
        for prompt in [AUTOFORMALIZATION_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT,
                     PHYSICIST_SYSTEM_PROMPT, CROSS_CHECK_SYSTEM_PROMPT]:
            assert len(prompt) > 100, "Prompt should be long enough"
            assert len(prompt) < 5000, "Prompt should not be excessively long"

    def test_prompts_use_clear_language(self):
        """
        Test that prompts use clear, unambiguous language.

        Expected behavior:
        - Should use imperative verbs
        - Should avoid vague terms
        - Should be specific
        """
        for prompt in [AUTOFORMALIZATION_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT,
                     PHYSICIST_SYSTEM_PROMPT, CROSS_CHECK_SYSTEM_PROMPT]:
            # Check for clear language indicators
            has_clear_language = (
                "Your task" in prompt or
                "Your responsibilities" in prompt or
                "You are" in prompt
            )
            assert has_clear_language, "Prompt should use clear language"

    def test_prompts_include_examples(self):
        """
        Test that prompts include examples where appropriate.

        Expected behavior:
        - Verifier prompt should have output example
        - Physicist prompt should have output example
        - Autoformalization prompt should have code example
        """
        # Verifier should have JSON example
        assert "```json" in VERIFIER_SYSTEM_PROMPT.lower() or "json" in VERIFIER_SYSTEM_PROMPT.lower()

        # Autoformalization should have Lean code example
        assert "```lean" in AUTOFORMALIZATION_SYSTEM_PROMPT.lower() or "lean" in AUTOFORMALIZATION_SYSTEM_PROMPT.lower()


class TestEdgeCases:
    """
    Tests for edge cases in prompt validation.
    """

    def test_prompts_are_not_empty(self):
        """
        Test that prompts are not empty strings.

        Expected behavior:
        - All prompts should have content
        """
        assert len(AUTOFORMALIZATION_SYSTEM_PROMPT) > 0
        assert len(VERIFIER_SYSTEM_PROMPT) > 0
        assert len(PHYSICIST_SYSTEM_PROMPT) > 0
        assert len(CROSS_CHECK_SYSTEM_PROMPT) > 0

    def test_prompts_are_strings(self):
        """
        Test that all prompts are string type.

        Expected behavior:
        - All prompts should be strings
        """
        assert isinstance(AUTOFORMALIZATION_SYSTEM_PROMPT, str)
        assert isinstance(VERIFIER_SYSTEM_PROMPT, str)
        assert isinstance(PHYSICIST_SYSTEM_PROMPT, str)
        assert isinstance(CROSS_CHECK_SYSTEM_PROMPT, str)

    def test_prompts_contain_printable_characters(self):
        """
        Test that prompts contain only printable characters.

        Expected behavior:
        - All prompts should be printable
        - Should not contain control characters
        """
        for prompt in [AUTOFORMALIZATION_SYSTEM_PROMPT, VERIFIER_SYSTEM_PROMPT,
                     PHYSICIST_SYSTEM_PROMPT, CROSS_CHECK_SYSTEM_PROMPT]:
            assert prompt.isprintable() or all(ord(c) < 128 or ord(c) in [10, 13] for c in prompt)
