"""Shared exceptions."""

from __future__ import annotations


class VitalGraphsError(Exception):
    """Base error for Vital Graphs."""


class ValidationError(VitalGraphsError):
    """Raised when YAML or graph validation fails."""

    def __init__(self, message: str, *, path: str | None = None) -> None:
        self.path = path
        if path:
            super().__init__(f"{path}: {message}")
        else:
            super().__init__(message)


class GraphIntegrityError(ValidationError):
    """Raised when SystemGraph invariants are violated."""
