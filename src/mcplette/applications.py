from dataclasses import dataclass, field
from typing import Callable

from .routing import Prompt, Resource, Tool


@dataclass(slots=True)
class Server:
    tools: list[Tool] = field(default_factory=list)
    resources: list[Resource] = field(default_factory=list)
    prompts: list[Prompt] = field(default_factory=list)

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
