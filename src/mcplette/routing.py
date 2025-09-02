from __future__ import annotations as _annotations

import functools
import inspect
from typing import Callable


class Tool:
    def __init__(
        self,
        name: str,
        handler: Callable[..., object],
        *,
        description: str | None = None,
        input_schema: dict[str, object] | None = None,
    ):
        self.name = name
        self.handler = handler
        self.description = description
        self.input_schema = input_schema or {"type": "object", "properties": {}}


class Resource:
    def __init__(
        self,
        uri: str,
        handler: Callable[..., object],
        *,
        name: str | None = None,
        description: str | None = None,
        mime_type: str | None = None,
    ):
        self.uri = uri
        self.handler = handler
        self.name = name or uri.split("/")[-1]
        self.description = description
        self.mime_type = mime_type


class Prompt:
    def __init__(
        self,
        name: str,
        handler: Callable[..., object],
        *,
        description: str | None = None,
        arguments: list[dict[str, object]] | None = None,
    ):
        self.name = name
        self.handler = handler
        self.description = description
        self.arguments = arguments or []


def is_async_callable(obj: object) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj) or (callable(obj) and inspect.iscoroutinefunction(obj.__call__))
