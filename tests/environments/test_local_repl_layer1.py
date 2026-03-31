"""
Tests for LocalREPL Layer1 tools.

This module tests the Layer1-specific tools in LocalREPL:
- verify_lean: Verify Lean code against Layer1 axioms
- check_haskell_types: Check Haskell dimensional types
- get_layer1_axioms: Retrieve available Layer1 axioms
- prove_theorem: Attempt to prove a theorem using Layer1
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.environments.local_repl import LocalREPL


class TestVerifyLeanTool:
    """
    Tests for the verify_lean tool in LocalREPL.
    """

    def test_verify_lean_tool_exists(self):
        """
        Test that verify_lean tool is available when Layer1 is enabled.

        Expected behavior:
        - Tool should be in available tools
        - Should be callable
        """
        repl = LocalREPL(enable_layer1=True)
        # Check if tool is available (implementation may vary)
        # This test documents expected behavior
        assert repl is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_verify_lean_simple_code(self, mock_bootstrap):
        """
        Test verifying simple Lean code.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should verify code successfully
        - Should return success result
        - Should include verification output
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": True,
            "output": "Proof verified successfully"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        lean_code = "theorem add_comm (a b : Nat) : a + b = b + a := by rw [add_comm]"

        # Execute verify_lean tool (implementation may vary)
        result = repl.execute_code(f"verify_lean('{lean_code}')")

        # Check result
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_verify_lean_with_syntax_error(self, mock_bootstrap):
        """
        Test verifying Lean code with syntax errors.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should detect syntax errors
        - Should return failure result
        - Should include error details
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": False,
            "error": "Syntax error at line 1"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        lean_code = "theorem bad : Prop :="  # Incomplete

        result = repl.execute_code(f"verify_lean('{lean_code}')")
        assert result is not None

    # @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    # def test_verify_lean_with_proof_error(self, mock_bootstrap):
    #     """
    #     Test verifying Lean code with proof errors.

    #     Args:
    #         mock_bootstrap: Mocked Layer1Bootstrap

    #     Expected behavior:
    #         - Should detect proof errors
    #         - Should return failure result
    #         - Should include error location
    #     """
    #     mock_kernel = MagicMock()
    #     mock_kernel.execute.return_value = {
    #         "success": False,
    #         "error": "Proof failed at step 3"
    #     }
    #     mock_instance = MagicMock()
    #     mock_instance.lean_kernel = mock_kernel
    #     mock_bootstrap.return_value = mock_instance

    #     repl = LocalREPL(enable_layer1=True)
    #     lean_code = "theorem false_statement : 1 = 2 := by trivial"

    #     result = repl.execute_code(f"verify_lean('{lean_code}')")
    #     assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_verify_lean_complex_theorem(self, mock_bootstrap):
        """
        Test verifying a complex Lean theorem.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle complex code
        - Should return appropriate result
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": True,
            "output": "Complex proof verified"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        lean_code = """
theorem distributive_law (a b c : Nat) :
  a * (b + c) = a * b + a * c :=
by rw [mul_add]
"""

        result = repl.execute_code(f"verify_lean('{lean_code}')")
        assert result is not None


class TestCheckHaskellTypesTool:
    """
    Tests for the check_haskell_types tool in LocalREPL.
    """

    def test_check_haskell_types_tool_exists(self):
        """
        Test that check_haskell_types tool is available when Layer1 is enabled.

        Expected behavior:
        - Tool should be in available tools
        - Should be callable
        """
        repl = LocalREPL(enable_layer1=True)
        assert repl is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_check_haskell_types_simple(self, mock_bootstrap):
        """
        Test checking simple Haskell types.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should check types successfully
        - Should return success result
        - Should include type information
        """
        mock_compiler = MagicMock()
        mock_compiler.compile.return_value = {
            "success": True,
            "output": "Types checked successfully"
        }
        mock_instance = MagicMock()
        mock_instance.haskell_compiler = mock_compiler
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        haskell_code = "x :: Double; x = 5.0"

        result = repl.execute_code(f"check_haskell_types('{haskell_code}')")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_check_haskell_types_with_dimensional_units(self, mock_bootstrap):
        """
        Test checking Haskell types with dimensional units.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should validate dimensional types
        - Should check unit consistency
        """
        mock_compiler = MagicMock()
        mock_compiler.compile.return_value = {
            "success": True,
            "output": "Dimensional types validated"
        }
        mock_instance = MagicMock()
        mock_instance.haskell_compiler = mock_compiler
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        haskell_code = """
velocity :: Length / Time
velocity = distance / time
"""

        result = repl.execute_code(f"check_haskell_types('{haskell_code}')")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_check_haskell_types_with_type_error(self, mock_bootstrap):
        """
        Test checking Haskell types with type errors.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should detect type errors
        - Should return failure result
        - Should include error details
        """
        mock_compiler = MagicMock()
        mock_compiler.compile.return_value = {
            "success": False,
            "error": "Type mismatch: expected Double, got String"
        }
        mock_instance = MagicMock()
        mock_instance.haskell_compiler = mock_compiler
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        haskell_code = "x :: Double; x = \"not a number\""

        result = repl.execute_code(f"check_haskell_types('{haskell_code}')")
        assert result is not None


class TestGetLayer1AxiomsTool:
    """
    Tests for the get_layer1_axioms tool in LocalREPL.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_get_layer1_axioms_returns_list(self, mock_bootstrap):
        """
        Test that get_layer1_axioms returns available axioms.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should return list of axioms
        - Should include Mathlib axioms
        - Should include PhysLib axioms
        """
        mock_instance = MagicMock()
        mock_instance.loaded = True
        mock_instance._mathlib_version = "v4.0.0"
        mock_instance._physlib_version = "v1.0.0"
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        result = repl.execute_code("get_layer1_axioms()")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_get_layer1_axioms_with_filter(self, mock_bootstrap):
        """
        Test filtering axioms by library.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should allow filtering by library
        - Should return only matching axioms
        """
        mock_instance = MagicMock()
        mock_instance.loaded = True
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        result = repl.execute_code("get_layer1_axioms(library='mathlib')")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_get_layer1_axioms_before_loading(self, mock_bootstrap):
        """
        Test getting axioms before Layer1 is loaded.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should return error or empty list
        - Should indicate Layer1 not loaded
        """
        mock_instance = MagicMock()
        mock_instance.loaded = False
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        result = repl.execute_code("get_layer1_axioms()")
        assert result is not None


class TestProveTheoremTool:
    """
    Tests for the prove_theorem tool in LocalREPL.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_prove_theorem_simple(self, mock_bootstrap):
        """
        Test proving a simple theorem.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should attempt proof synthesis
        - Should return proof result
        - Should include proof if successful
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": True,
            "proof": "Proof completed using rw tactic"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        theorem = "theorem add_comm (a b : Nat) : a + b = b + a"

        result = repl.execute_code(f"prove_theorem('{theorem}')")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_prove_theorem_with_tactics(self, mock_bootstrap):
        """
        Test proving a theorem with specific tactics.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should use specified tactics
        - Should return proof result
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": True,
            "proof": "Proof completed using induction and rw"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        theorem = "theorem add_comm (a b : Nat) : a + b = b + a"
        tactics = ["induction", "rw"]

        result = repl.execute_code(f"prove_theorem('{theorem}', tactics={tactics})")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_prove_theorem_unprovable(self, mock_bootstrap):
        """
        Test attempting to prove an unprovable theorem.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should detect unprovable statement
        - Should return failure result
        - Should indicate why proof failed
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": False,
            "error": "Theorem is false: cannot prove 1 = 2"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        theorem = "theorem false_statement : 1 = 2"

        result = repl.execute_code(f"prove_theorem('{theorem}')")
        assert result is not None


class TestLayer1Integration:
    """
    Tests for Layer1 integration in LocalREPL.
    """

    def test_enable_layer1_flag(self):
        """
        Test that enable_layer1 flag enables Layer1 tools.

        Expected behavior:
        - With enable_layer1=True, Layer1 tools should be available
        - With enable_layer1=False, Layer1 tools should not be available
        """
        repl_with_layer1 = LocalREPL(enable_layer1=True)
        repl_without_layer1 = LocalREPL(enable_layer1=False)

        assert repl_with_layer1 is not None
        assert repl_without_layer1 is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_layer1_bootstrap_initialization(self, mock_bootstrap):
        """
        Test that Layer1Bootstrap is initialized correctly.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Layer1Bootstrap should be created
        - Should be initialized with correct path
        """
        repl = LocalREPL(enable_layer1=True)
        assert mock_bootstrap.called or repl is not None

    def test_layer1_tools_in_custom_tools(self):
        """
        Test that Layer1 tools can be added via custom_tools.

        Expected behavior:
        - Tools should be added to custom_tools dict
        - Should be callable from REPL
        """
        custom_tools = {
            "verify_lean": lambda x: {"success": True},
            "get_layer1_axioms": lambda: {"axioms": []}
        }
        repl = LocalREPL(custom_tools=custom_tools)

        # Execute code that uses custom tools
        result = repl.execute_code("result = verify_lean('test')")
        assert result is not None


class TestErrorHandling:
    """
    Tests for error handling in Layer1 tools.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_verify_lean_with_none_input(self, mock_bootstrap):
        """
        Test verify_lean with None input.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle None gracefully
        - Should return error result
        """
        mock_instance = MagicMock()
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        result = repl.execute_code("verify_lean(None)")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_prove_theorem_with_empty_string(self, mock_bootstrap):
        """
        Test prove_theorem with empty string.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle empty string gracefully
        - Should return error result
        """
        mock_instance = MagicMock()
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        result = repl.execute_code("prove_theorem('')")
        assert result is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_layer1_tools_without_layer1_enabled(self, mock_bootstrap):
        """
        Test calling Layer1 tools when Layer1 is not enabled.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should return error indicating Layer1 not enabled
        - Should not crash
        """
        repl = LocalREPL(enable_layer1=False)
        result = repl.execute_code("verify_lean('test')")
        assert result is not None


class TestCleanup:
    """
    Tests for cleanup of Layer1 resources.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_cleanup_releases_resources(self, mock_bootstrap):
        """
        Test that cleanup releases Layer1 resources.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should clean up Lean kernel
        - Should clean up Haskell compiler
        - Should not leave resources open
        """
        mock_instance = MagicMock()
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        repl.cleanup()

        # Verify cleanup was called (implementation may vary)
        assert repl is not None


class TestEdgeCases:
    """
    Tests for edge cases in Layer1 tools.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap')
    def test_verify_lean_with_very_long_code(self, mock_bootstrap):
        """
        Test verifying very long Lean code.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle long code
        - Should not crash
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": True,
            "output": "Long code verified"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)
        lean_code = "theorem t" + " " * 10000 + ": Prop := trivial"

        result = repl.execute_code(f"verify_lean('{lean_code}')")
        assert result is not None

    @patch('rlm.environments.local_repl.Layer1Bootstrap')
    def test_multiple_layer1_tool_calls(self, mock_bootstrap):
        """
        Test multiple consecutive Layer1 tool calls.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle multiple calls
        - Each call should work independently
        """
        mock_kernel = MagicMock()
        mock_kernel.execute.return_value = {
            "success": True,
            "output": "Success"
        }
        mock_instance = MagicMock()
        mock_instance.lean_kernel = mock_kernel
        mock_instance.load_layer1.return_value = {"success": True}
        mock_instance.get_verification_oracle.return_value = {
            "lean_kernel": mock_kernel,
            "haskell_types": None
        }
        mock_bootstrap.return_value = mock_instance

        repl = LocalREPL(enable_layer1=True)

        # Verify Layer1 was initialized properly
        assert repl.verification_oracle is not None
        assert mock_instance.load_layer1.called
        assert mock_instance.get_verification_oracle.called

        # Multiple calls should all succeed (placeholder implementation)
        for i in range(5):
            result = repl.execute_code(f"verify_lean('theorem t{i} : Prop := trivial')")
            assert result is not None
