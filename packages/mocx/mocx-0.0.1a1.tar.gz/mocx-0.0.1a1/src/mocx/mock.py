from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Sequence
from unittest import mock as _mock

__all__ = [
    "mock",
    "Mock",
    "mock_object",
    "mock_return",
    "async_mock",
    "AsyncMock",
    "async_mock_object",
    "patch_fastapi_dependencies",
]


class _AsyncMock(_mock.Mock):
    # pylint: disable=invalid-overridden-method, useless-parent-delegation
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return super().__call__(*args, **kwargs)


@dataclass
class MockReturn:
    value: Any | None = None
    once: Any | None = None
    each: Sequence[Any] | None = None
    call: Callable[..., Any] | None = None
    exception: Exception | None = None
    side_effect: Any | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        if (bool(self.value) + bool(self.once) + bool(self.each) + bool(self.call)) > 1:
            raise Exception("...")

        if self.value:
            self.side_effect = lambda *args, **kwargs: self.value
        elif self.once:
            self.side_effect = [self.once]
        elif self.each:
            self.side_effect = self.each
        elif self.call:
            self.side_effect = self.call
        elif self.exception:
            self.side_effect = self.exception


def mock_return(
    value: Any | None = None,
    once: Any | None = None,
    each: Sequence[Any] | None = None,
    call: Callable[..., Any] | None = None,
    exception: Exception | None = None,
) -> Any:
    return MockReturn(
        value=value, once=once, each=each, call=call, exception=exception
    ).side_effect


def mock(
    return_value: Any | None = None,
    return_once: Any | None = None,
    return_each: Sequence[Any] | None = None,
    return_call: Callable[..., Any] | None = None,
    return_exception: Exception | None = None,
    **kwargs: Any,
) -> _mock.Mock:
    side_effect: Any = mock_return(
        value=return_value,
        once=return_once,
        each=return_each,
        call=return_call,
        exception=return_exception,
    )
    return _mock.Mock(side_effect=side_effect, **kwargs)


@wraps(mock)
def Mock(
    *args: Any,
    **kwargs: Any,
) -> _mock.Mock:
    return mock(*args, **kwargs)


def mock_object(
    obj_type: type[Any],
    **kwargs: Any,
) -> _mock.Mock:

    mock_obj: _mock.Mock = mock(spec_set=obj_type, **kwargs)

    for member_name, member_returns in kwargs.items():
        mock_member: _mock.Mock = mock()
        mock_member.side_effect = member_returns
        setattr(mock_obj, member_name, mock_member)

    return mock_obj


def async_mock(
    return_value: Any | None = None,
    return_once: Any | None = None,
    return_each: Sequence[Any] | None = None,
    return_call: Callable[..., Any] | None = None,
    return_exception: Exception | None = None,
    **kwargs: Any,
) -> _AsyncMock:
    side_effect: Any = mock_return(
        value=return_value,
        once=return_once,
        each=return_each,
        call=return_call,
        exception=return_exception,
    )
    return _AsyncMock(side_effect=side_effect, **kwargs)


@wraps(async_mock)
def AsyncMock(
    *args: Any,
    **kwargs: Any,
) -> _AsyncMock:
    return async_mock(*args, **kwargs)


def async_mock_object(
    obj_type: type[Any],
    **kwargs: Any,
) -> _AsyncMock:

    mock_obj: _mock.Mock = async_mock(spec_set=obj_type, **kwargs)

    for member_name, member_returns in kwargs.items():
        mock_member: _mock.Mock = mock()
        mock_member.side_effect = member_returns
        setattr(mock_obj, member_name, mock_member)

    return mock_obj


def patch_fastapi_dependencies(
    *args: Any,
    overrides: dict[Callable[..., Any], Callable[..., Any]] | None,
    remove: bool | None = False,
) -> None:
    from fastapi import FastAPI
    from starlette.routing import Mount

    for x in args:
        if not isinstance(x, FastAPI):
            raise TypeError(f"Expected type 'FastAPI'; given: {type(x)}")

        if overrides is None:
            x.dependency_overrides.clear()
        elif remove:
            for k in overrides:
                del x.dependency_overrides[k]
        else:
            x.dependency_overrides.update(overrides)

        patch_fastapi_dependencies(
            *[
                y.app
                for y in x.routes
                if isinstance(y, Mount) and isinstance(y.app, FastAPI)
            ],
            overrides=overrides,
        )
