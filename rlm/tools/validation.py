# Tool validation utilities
import ast
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    valid: bool
    errors: List[str]
    warnings: List[str]


class ToolValidator:
    """
    Validates tool implementations for safety and quality.
    """

    DANGEROUS_PATTERNS = [
        r"__import__",
        r"eval\s*\(",
        r"exec\s*\(",
        r"compile\s*\(",
        r"open\s*\(",
        r"input\s*\(",
        r"raw_input\s*\(",
        r"subprocess\s*\.\s*(run|call|popen|system)",
        r"os\s*\.\s*(system|popen|remove|rmdir)",
        r"shutil\s*\.\s*(rmtree|make_archive)",
    ]

    @classmethod
    def validate(cls, implementation: str) -> ValidationResult:
        """Validate tool implementation."""
        errors = []
        warnings = []

        try:
            ast.parse(implementation)
        except SyntaxError as e:
            errors.append(f"Syntax error: {e}")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, implementation):
                errors.append(f"Dangerous pattern detected: {pattern}")

        tree = ast.parse(implementation)
        has_docstring = any(
            isinstance(node, (ast.FunctionDef, ast.Module)) and ast.get_docstring(node)
            for node in ast.walk(tree)
        )
        if not has_docstring:
            warnings.append("Tool implementation lacks docstrings")

        return ValidationResult(
            valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @classmethod
    def extract_parameters(
        cls, implementation: str, function_name: str
    ) -> List[Tuple[str, str, bool]]:
        """
        Extract parameters from a function definition.
        Returns list of (name, type_hint, is_required).
        """
        try:
            tree = ast.parse(implementation)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    params = []
                    for arg in node.args.args:
                        name = arg.arg
                        type_hint = "Any"
                        if arg.annotation:
                            type_hint = getattr(
                                arg.annotation, "id", str(arg.annotation)
                            )

                        arg_index = node.args.args.index(arg)
                        defaults_offset = len(node.args.args) - len(node.args.defaults)
                        has_default = arg_index >= defaults_offset

                        params.append((name, type_hint, not has_default))
                    return params
            return []
        except Exception:
            return []
