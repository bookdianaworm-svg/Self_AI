"""
GHC-based Haskell type checker implementation.

This module provides a type checker that uses the Glasgow Haskell Compiler (GHC)
via subprocess to check Haskell code for type errors.
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
from rlm.typechecking.haskell.haskell_checker import HaskellChecker
from rlm.typechecking.haskell.result import HaskellErrorInfo, HaskellTypeResult
from rlm.typechecking.result import TypeErrorInfo


class GHCChecker(HaskellChecker):
    """
    Haskell type checker using GHC.

    This checker invokes GHC as a subprocess to type-check Haskell code.

    Error Codes:
        HC001: Haskell checker not available
        HC002: Haskell type error
        HC003: Haskell timeout
    """

    ERROR_CODE_NOT_AVAILABLE = "HC001"
    ERROR_CODE_TYPE_ERROR = "HC002"
    ERROR_CODE_TIMEOUT = "HC003"

    def __init__(
        self,
        timeout_seconds: float = 30.0,
        ghc_path: str = "ghc",
        ghc_options: Optional[list[str]] = None,
    ):
        """
        Initialize the GHC checker.

        Args:
            timeout_seconds: Default timeout for type checking.
            ghc_path: Path to GHC executable.
            ghc_options: Additional options to pass to GHC.

        Raises:
            TypeCheckerNotAvailableError: If GHC is not available.
        """
        super().__init__(timeout_seconds, ghc_path, ghc_options or [])
        self._version: Optional[str] = None
        self._check_ghc_availability()

    @property
    def name(self) -> str:
        return "GHC Haskell Type Checker"

    def _check_ghc_availability(self) -> None:
        """Check if GHC is available and get its version."""
        try:
            ghc_cmd: str = self.ghc_path if self.ghc_path is not None else "ghc"
            result = subprocess.run(
                [ghc_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0:
                # Parse version from output like "The Glorious Glasgow Haskell Compilation System, version 9.4.8"
                match = re.search(r"version\s+(\d+\.\d+\.\d+)", result.stdout)
                if match:
                    self._version = match.group(1)
                else:
                    self._version = result.stdout.strip().split("\n")[0]

                self._health = TypeCheckerHealth(
                    status=CheckerStatus.AVAILABLE,
                    version=self._version,
                    last_check=datetime.now(),
                )
            else:
                self._health = TypeCheckerHealth(
                    status=CheckerStatus.UNAVAILABLE,
                    error=f"GHC returned code {result.returncode}",
                    last_check=datetime.now(),
                )
                raise TypeCheckerNotAvailableError(
                    "haskell", f"GHC not available: {result.stderr}"
                )
        except FileNotFoundError:
            self._health = TypeCheckerHealth(
                status=CheckerStatus.UNAVAILABLE,
                error=f"GHC executable not found at: {self.ghc_path}",
                last_check=datetime.now(),
            )
            raise TypeCheckerNotAvailableError(
                "haskell", f"GHC executable not found at: {self.ghc_path}"
            )
        except subprocess.TimeoutExpired:
            self._health = TypeCheckerHealth(
                status=CheckerStatus.ERROR,
                error="Timeout while checking GHC availability",
                last_check=datetime.now(),
            )
            raise TypeCheckerNotAvailableError(
                "haskell", "Timeout while checking GHC availability"
            )

    def health_check(self) -> TypeCheckerHealth:
        """
        Perform a health check on GHC.

        Returns:
            TypeCheckerHealth with current status.
        """
        try:
            ghc_cmd: str = self.ghc_path if self.ghc_path is not None else "ghc"
            result = subprocess.run(
                [ghc_cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0:
                match = re.search(r"version\s+(\d+\.\d+\.\d+)", result.stdout)
                version = match.group(1) if match else "unknown"

                self._health = TypeCheckerHealth(
                    status=CheckerStatus.AVAILABLE,
                    version=version,
                    last_check=datetime.now(),
                )
            else:
                self._health.status = CheckerStatus.UNAVAILABLE
                self._health.error = f"GHC returned code {result.returncode}"
        except FileNotFoundError:
            self._health.status = CheckerStatus.UNAVAILABLE
            self._health.error = f"GHC not found at: {self.ghc_path}"
        except subprocess.TimeoutExpired:
            self._health.status = CheckerStatus.ERROR
            self._health.error = "Timeout while checking GHC"
        except Exception as e:
            self._health.status = CheckerStatus.ERROR
            self._health.error = str(e)

        self._health.last_check = datetime.now()
        return self._health

    def check_types(
        self,
        code: str,
        timeout_seconds: Optional[float] = None,
    ) -> HaskellTypeResult:
        """
        Check Haskell code for type errors using GHC.

        Args:
            code: Haskell code to type check.
            timeout_seconds: Optional timeout override.

        Returns:
            HaskellTypeResult with type checking results.
        """
        timeout = timeout_seconds or self.timeout_seconds
        start_time = time.perf_counter()

        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".hs",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Build GHC command
            cmd = [
                self.ghc_path,
                "-fno-code",  # Type-check only, don't generate code
                "-ferror-spans",  # Include error spans in output
                *self.ghc_options,
                temp_file,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            execution_time_ms = (time.perf_counter() - start_time) * 1000

            # Parse errors from stderr
            errors = self._parse_ghc_errors(result.stderr, result.stdout)

            success = result.returncode == 0 and len(errors) == 0

            return HaskellTypeResult(
                success=success,
                code=code,
                errors=errors,
                checked_at=datetime.now(),
                execution_time_ms=execution_time_ms,
                stdout=result.stdout,
                stderr=result.stderr,
                metadata={
                    "return_code": result.returncode,
                    "ghc_version": self._version,
                    "temp_file": temp_file,
                },
            )

        except subprocess.TimeoutExpired:
            execution_time_ms = (time.perf_counter() - start_time) * 1000
            raise TypeCheckTimeoutError(
                timeout_seconds=timeout,
                code=code,
                message=f"Haskell type checking timed out after {timeout} seconds",
            )
        except FileNotFoundError:
            raise TypeCheckerNotAvailableError(
                "haskell", f"GHC not found at: {self.ghc_path}"
            )
        except Exception as e:
            execution_time_ms = (time.perf_counter() - start_time) * 1000
            raise TypeCheckExecutionError(
                checker="haskell",
                message=str(e),
                stderr="",
            )
        finally:
            # Clean up temp file
            try:
                Path(temp_file).unlink(missing_ok=True)
            except Exception:
                pass

    def _parse_ghc_errors(
        self, stderr: str, stdout: str = ""
    ) -> list[HaskellErrorInfo]:
        """
        Parse GHC error output into HaskellErrorInfo objects.

        GHC outputs errors in the format:
        filename:line:column: [error code] message

        Args:
            stderr: Standard error from GHC.
            stdout: Standard output from GHC (may contain additional info).

        Returns:
            List of HaskellErrorInfo objects.
        """
        errors = []
        combined_output = stderr + "\n" + stdout

        # Pattern for GHC error messages
        # Example: "test.hs:3:10: error: Couldn't match expected type ..."
        pattern = re.compile(
            r"(?P<file>[^:]+):"
            r"(?P<line>\d+):"
            r"(?P<col>\d+):"
            r"(?:\s+(?P<severity>warning|error))?"
            r"(?:\s+\[(?P<code>[^\]]+)\])?"
            r"\s+(?P<message>.+)"
        )

        for match in pattern.finditer(combined_output):
            line = int(match.group("line"))
            col = int(match.group("col"))
            severity = match.group("severity") or "error"
            ghc_code = match.group("code")
            message = match.group("message").strip()

            # Determine our error code
            if ghc_code and "Couldn't match" in message:
                error_code = "HC002"  # Type mismatch
            elif ghc_code and "Occurs check" in message:
                error_code = "HC002"  # Occurs check failure
            elif ghc_code and "Not in scope" in message:
                error_code = "HC002"  # Not in scope
            else:
                error_code = "HC002"  # Generic type error

            error_info = HaskellErrorInfo(
                line=line,
                column=col,
                message=message,
                severity=severity,
                code=error_code,
                ghc_code=ghc_code,
            )

            errors.append(error_info)

        return errors

    def check(self, code: str, timeout_seconds: Optional[float] = None):
        """
        Check Haskell code for type errors.

        This method implements the TypeChecker interface.

        Args:
            code: Haskell code to type check.
            timeout_seconds: Optional timeout override.

        Returns:
            TypeCheckerResult with type checking results.
        """
        return self.check_types(code, timeout_seconds)
