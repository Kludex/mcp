import functools
import inspect
from dataclasses import dataclass
from typing import Callable, Sequence


def is_async_callable(obj: object) -> bool:
    """
    Correctly determines if an object is a coroutine function,
    including those wrapped in functools.partial objects.
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj) or (
        callable(obj) and inspect.iscoroutinefunction(obj.__call__)
    )


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
        self.name = name or uri.split('/')[-1]
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


@dataclass(slots=True)
class Server:
    tools: list[Tool]
    resources: list[Resource] 
    prompts: list[Prompt]
    
    def __init__(
        self,
        tools: Sequence[Tool] | None = None,
        resources: Sequence[Resource] | None = None,
        prompts: Sequence[Prompt] | None = None,
    ):
        self.tools = list(tools or [])
        self.resources = list(resources or [])
        self.prompts = list(prompts or [])
    
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
