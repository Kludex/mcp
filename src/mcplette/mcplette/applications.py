from __future__ import annotations as _annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

from .routing import Prompt, Resource, Tool

if TYPE_CHECKING:
    from uvicorn._types import ASGIReceiveCallable, ASGISendCallable, Scope


@dataclass(slots=True, kw_only=True)
class MCP:
    tools: list[Tool] = field(default_factory=list)
    resources: list[Resource] = field(default_factory=list)
    prompts: list[Prompt] = field(default_factory=list)

    _router: ... = field(init=False)

    def add_tool(
        self,
        name: str,
        handler: Callable[..., object],
        *,
        description: str | None = None,
        input_schema: dict[str, object] | None = None,
    ) -> None:
        tool = Tool(name, handler, description=description, input_schema=input_schema)
        self.tools.append(tool)

    def add_resource(
        self,
        uri: str,
        handler: Callable[..., object],
        *,
        name: str | None = None,
        description: str | None = None,
        mime_type: str | None = None,
    ) -> None:
        resource = Resource(uri, handler, name=name, description=description, mime_type=mime_type)
        self.resources.append(resource)

    def add_prompt(
        self,
        name: str,
        handler: Callable[..., object],
        *,
        description: str | None = None,
        arguments: list[dict[str, object]] | None = None,
    ) -> None:
        prompt = Prompt(name, handler, description=description, arguments=arguments)
        self.prompts.append(prompt)

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        return await self._router(scope, receive, send)
