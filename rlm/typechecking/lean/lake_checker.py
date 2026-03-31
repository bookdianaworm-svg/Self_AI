"""
Lake-based Lean 4 verification implementation.

This module provides a verifier that uses Lake (the Lean 4 build tool)
via subprocess to verify Lean code.
"""

import re
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from rlm.typechecking.base import CheckerStatus, TypeCheckerHealth
from rlm.typechecking.exceptions import (
    TypeCheckerNotAvailableError,
    TypeCheckTimeoutError,
    TypeCheckExecutionError,
)
from rlm.typechecking.lean.lean_checker import LeanChecker
from rlm.typechecking.lean.result import LeanErrorInfo, LeanVerificationResult
from rlm.typechecking.result import TypeErrorInfo


class LakeChecker(LeanChecker):
    """
    Lean 4 verifier using Lake.

    This verifier invokes Lake as a subprocess to verify Lean code.

    Error Codes:
        LN001: Lean checker not available
        LN002: Lean type error / verification failure
        LN003: Lean timeout
    """

    ERROR_CODE_NOT_AVAILABLE = "LN001"
    ERROR_CODE_VERIFICATION_FAILED = "LN002"
    ERROR_CODE_TIMEOUT = "LN003"

    def __init__(
        self,
        timeout_seconds: float = 60.0,
        lake_path: str = "lake",
        lean_path: str = "lean",
        lean_options: Optional[list[str]] = None,
    ):
        """
        Initialize the Lake checker.

        Args:
            timeout_seconds: Default timeout for verification.
            lake_path: Path to Lake executable.
            lean_path: Path to Lean executable.
            lean_options: Additional options to pass to Lake/Lean.

        Raises:
            TypeCheckerNotAvailableError: If Lake/Lean is not available.
        """
        super().__init__(timeout_seconds, lake_path)
        self.lean_path = lean_path
        self.lean_options = lean_options or []
        self._version: Optional[str] = None
        self._check_lake_availability()

    @property
    def name(self) -> str:
        return "Lake Lean 4 Verifier"

    def _check_lake_availability(self) -> None:
        """Check if Lake is available and get its version."""
        try:
            lean_cmd: str = self.lean_path if self.lean_path is not None else "lean"
            result = subprocess.run(
                [lean_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0:
                self._version = result.stdout.strip().split("\n")[0]

                self._health = TypeCheckerHealth(
                    status=CheckerStatus.AVAILABLE,
                    version=self._version,
                    last_check=datetime.now(),
                )
            else:
                self._health = TypeCheckerHealth(
                    status=CheckerStatus.UNAVAILABLE,
                    error=f"Lean returned code {result.returncode}",
                    last_check=datetime.now(),
                )
                raise TypeCheckerNotAvailableError(
                    "lean", f"Lean not available: {result.stderr}"
                )
        except FileNotFoundError:
            self._health = TypeCheckerHealth(
                status=CheckerStatus.UNAVAILABLE,
                error=f"Lean executable not found at: {self.lean_path}",
                last_check=datetime.now(),
            )
            raise TypeCheckerNotAvailableError(
                "lean", f"Lean executable not found at: {self.lean_path}"
            )
        except subprocess.TimeoutExpired:
            self._health = TypeCheckerHealth(
                status=CheckerStatus.ERROR,
                error="Timeout while checking Lean availability",
                last_check=datetime.now(),
            )
            raise TypeCheckerNotAvailableError(
                "lean", "Timeout while checking Lean availability"
            )

    def health_check(self) -> TypeCheckerHealth:
        """
        Perform a health check on Lake/Lean.

        Returns:
            TypeCheckerHealth with current status.
        """
        try:
            lean_cmd: str = self.lean_path if self.lean_path is not None else "lean"
            result = subprocess.run(
                [lean_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0:
                version = result.stdout.strip().split("\n")[0]

                self._health = TypeCheckerHealth(
                    status=CheckerStatus.AVAILABLE,
                    version=version,
                    last_check=datetime.now(),
                )
            else:
                self._health.status = CheckerStatus.UNAVAILABLE
                self._health.error = f"Lean returned code {result.returncode}"
        except FileNotFoundError:
            self._health.status = CheckerStatus.UNAVAILABLE
            self._health.error = f"Lean not found at: {self.lean_path}"
        except subprocess.TimeoutExpired:
            self._health.status = CheckerStatus.ERROR
            self._health.error = "Timeout while checking Lean"
        except Exception as e:
            self._health.status = CheckerStatus.ERROR
            self._health.error = str(e)

        self._health.last_check = datetime.now()
        return self._health

    def verify(
        self,
        code: str,
        timeout_seconds: Optional[float] = None,
    ) -> LeanVerificationResult:
        """
        Verify Lean code using Lake.

        Args:
            code: Lean code to verify.
            timeout_seconds: Optional timeout override.

        Returns:
            LeanVerificationResult with verification results.
        """
        timeout = timeout_seconds or self.timeout_seconds
        start_time = time.perf_counter()

        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".lean",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Build Lake/Lean command
            # Use lake to verify, or fall back to lean directly
            cmd = [
                self.lean_path,
                *self.lean_options,
                temp_file,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            execution_time_ms = (time.perf_counter() - start_time) * 1000

            # Parse errors from stderr/stdout
            errors = self._parse_lean_errors(result.stderr, result.stdout)

            success = result.returncode == 0 and len(errors) == 0

            return LeanVerificationResult(
                success=success,
                code=code,
                errors=errors,
                checked_at=datetime.now(),
                execution_time_ms=execution_time_ms,
                stdout=result.stdout,
                stderr=result.stderr,
                metadata={
                    "return_code": result.returncode,
                    "lean_version": self._version,
                    "temp_file": temp_file,
                },
            )

        except subprocess.TimeoutExpired:
            execution_time_ms = (time.perf_counter() - start_time) * 1000
            raise TypeCheckTimeoutError(
                timeout_seconds=timeout,
                code=code,
                message=f"Lean verification timed out after {timeout} seconds",
            )
        except FileNotFoundError:
            raise TypeCheckerNotAvailableError(
                "lean", f"Lean not found at: {self.lean_path}"
            )
        except Exception as e:
            execution_time_ms = (time.perf_counter() - start_time) * 1000
            raise TypeCheckExecutionError(
                checker="lean",
                message=str(e),
                stderr="",
            )
        finally:
            # Clean up temp file
            try:
                Path(temp_file).unlink(missing_ok=True)
            except Exception:
                pass

    def _parse_lean_errors(self, stderr: str, stdout: str = "") -> list[LeanErrorInfo]:
        """
        Parse Lean error output into LeanErrorInfo objects.

        Lean outputs errors in various formats, including:
        - "file.lean: line: col: error: message"
        - Tactic state dumps

        Args:
            stderr: Standard error from Lean.
            stdout: Standard output from Lean (may contain additional info).

        Returns:
            List of LeanErrorInfo objects.
        """
        errors = []
        combined_output = stderr + "\n" + stdout

        # Pattern for Lean error messages
        # Example: "test.lean:3:10: error: ... "
        pattern = re.compile(
            r"(?P<file>[^:]+):"
            r"(?P<line>\d+):"
            r"(?P<col>\d+):"
            r"(?:\s+(?P<severity>warning|error))?"
            r"\s+(?P<message>.+)"
        )

        for match in pattern.finditer(combined_output):
            line = int(match.group("line"))
            col = int(match.group("col"))
            severity = match.group("severity") or "error"
            message = match.group("message").strip()

            error_code = "LN002"  # Generic verification failure

            error_info = LeanErrorInfo(
                line=line,
                column=col,
                message=message,
                severity=severity,
                code=error_code,
                lean_code=self._get_lean_error_code(message),
            )

            errors.append(error_info)

        return errors

    def _get_lean_error_code(self, message: str) -> Optional[str]:
        """Extract Lean error code from error message."""
        if "type mismatch" in message.lower():
            return "type mismatch"
        elif "unknown identifier" in message.lower():
            return "unknown identifier"
        elif "expected" in message.lower() and "got" in message.lower():
            return "expected got"
        elif "invalid" in message.lower():
            return "invalid"
        return None

    def check(self, code: str, timeout_seconds: Optional[float] = None):
        """
        Verify Lean code.

        This method implements the TypeChecker interface.

        Args:
            code: Lean code to verify.
            timeout_seconds: Optional timeout override.

        Returns:
            TypeCheckerResult with verification results.
        """
        return self.verify(code, timeout_seconds)
