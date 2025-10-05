from __future__ import annotations as _annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any, overload

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
from starlette.types import ExceptionHandler, Lifespan

from .routing import Func, MCPRouter, Prompt, Resource, Tool, ToolParams


class MCP(Starlette):
    def __init__(
        self,
        tools: Sequence[Tool] = (),
        resources: Sequence[Resource] = (),
        prompts: Sequence[Prompt] = (),
        *,
        debug: bool = False,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan[MCP] | None = None,
    ) -> None:
        super().__init__(debug, routes, middleware, exception_handlers, on_startup, on_shutdown, lifespan)

        self.mcp_router = MCPRouter(tools=tools, resources=resources, prompts=prompts)

        self.router.add_route(
            "/tools/{tool_name}/calls/{tool_call_id}",
            self.mcp_router.handle_tools_call,
            methods=["PUT"],
        )

    @overload
    def tool(self, func: Func[ToolParams], /) -> Func[ToolParams]: ...

    @overload
    def tool(
        self,
        /,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> Callable[[Func[ToolParams]], Func[ToolParams]]: ...

    def tool(
        self,
        func: Func[ToolParams] | None = None,
        /,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> Any:
        def tool_decorator(func_: Func[ToolParams]) -> Func[ToolParams]:
            self.mcp_router.add_tool(func_, name=name, description=description)
            return func_

        return tool_decorator if func is None else tool_decorator(func)

    def resource(
        self, uri: str, name: str | None = None, description: str | None = None, mime_type: str | None = None
    ) -> ...:
        def decorator(handler: Callable[..., object]) -> None:
            self.mcp_router.add_resource(uri, handler, name=name, description=description, mime_type=mime_type)

        return decorator

    def prompt(
        self, name: str, description: str | None = None, arguments: list[dict[str, object]] | None = None
    ) -> ...:
        def decorator(handler: Callable[..., object]) -> None:
            self.mcp_router.add_prompt(name, handler, description=description, arguments=arguments)

        return decorator
