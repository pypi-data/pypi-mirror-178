from __future__ import annotations

from unittest.mock import patch

from . import httpx, requests
from .__version__ import __version__
from .constants import CONTENT_TYPE_DEFAULT, CONTENT_TYPE_JSON
from .mock import (
    AsyncMock,
    Mock,
    async_mock,
    async_mock_object,
    mock,
    mock_object,
    mock_return,
    patch_fastapi_dependencies,
)

__all__ = [
    "__version__",
    "mock",
    "Mock",
    "mock_object",
    "mock_return",
    "async_mock",
    "AsyncMock",
    "async_mock_object",
    "patch",
    "patch_fastapi_dependencies",
    "requests",
    "httpx",
    "CONTENT_TYPE_DEFAULT",
    "CONTENT_TYPE_JSON",
]
