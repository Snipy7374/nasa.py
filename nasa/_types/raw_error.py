from __future__ import annotations
from typing import TypedDict

__all__: tuple[str, ...] = (
    "RawAPIError",
)


class ErrorMetadata(TypedDict):
    code: str
    message: str


class RawAPIError(TypedDict):
    error: ErrorMetadata