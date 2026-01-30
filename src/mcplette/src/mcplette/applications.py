from collections.abc import Sequence
from dataclasses import dataclass, field

from asgi_types import ASGIReceiveCallable, ASGISendCallable, Scope

from mcplette.middleware import MCPMiddleware
from mcplette.routing import MCPRoute


@dataclass(kw_only=True)
class MCPLette:
    name: str
    description: str
    version: str
    routes: Sequence[MCPRoute]
    middleware: Sequence[MCPMiddleware] = field(default_factory=list[MCPMiddleware])

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None: ...
