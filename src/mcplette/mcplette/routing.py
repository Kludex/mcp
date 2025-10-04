from __future__ import annotations as _annotations

import functools
import inspect
from dataclasses import KW_ONLY, dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from uvicorn._types import ASGIReceiveCallable, ASGISendCallable, Scope


@dataclass(slots=True)
class Tool:
    name: str
    # TODO(Marcelo): This handler should be a generator, given that we can use
    # elicitation and sampling.
    handler: Callable[..., object]

    _ = KW_ONLY

    description: str | None = None
    input_schema: dict[str, object] | None = field(default={"type": "object", "properties": {}})


@dataclass(slots=True)
class Resource:
    uri: str
    handler: Callable[..., object]

    _ = KW_ONLY

    name: str | None = None
    description: str | None = None
    mime_type: str | None = None

    def __post_init__(self):
        self.name = self.name or self.uri.split("/")[-1]


@dataclass(slots=True)
class Prompt:
    name: str
    handler: Callable[..., object]

    _ = KW_ONLY

    description: str | None = None
    arguments: list[dict[str, object]] | None = field(default_factory=list)


@dataclass(slots=True)
class StreamableHTTPRouter:
    tools: list[Tool]
    resources: list[Resource]
    prompts: list[Prompt]

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        if scope["type"] != "http":
            return


@dataclass(slots=True)
class WebSocketRouter:
    tools: list[Tool]
    resources: list[Resource]
    prompts: list[Prompt]

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        if scope["type"] != "websocket":
            return


def is_async_callable(obj: object) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj) or (callable(obj) and inspect.iscoroutinefunction(obj.__call__))
