import asyncio
from typing import Callable


class Tool:
    def __init__(
        self,
        name: str,
        handler: Callable[..., object],
        description: str | None = None,
        input_schema: dict[str, object] | None = None,
    ):
        self.name = name
        self.handler = handler
        self.description = description
        self.input_schema = input_schema or {"type": "object", "properties": {}}
        
    async def call(self, **kwargs: object) -> object:
        if asyncio.iscoroutinefunction(self.handler):
            return await self.handler(**kwargs)
        return self.handler(**kwargs)


class Resource:
    def __init__(
        self,
        uri: str,
        handler: Callable[..., object],
        name: str | None = None,
        description: str | None = None,
        mime_type: str | None = None,
    ):
        self.uri = uri
        self.handler = handler
        self.name = name or uri.split('/')[-1]
        self.description = description
        self.mime_type = mime_type
        
    async def read(self, **kwargs: object) -> object:
        if asyncio.iscoroutinefunction(self.handler):
            return await self.handler(**kwargs)
        return self.handler(**kwargs)


class Prompt:
    def __init__(
        self,
        name: str,
        handler: Callable[..., object],
        description: str | None = None,
        arguments: list[dict[str, object]] | None = None,
    ):
        self.name = name
        self.handler = handler
        self.description = description
        self.arguments = arguments or []
        
    async def get(self, **kwargs: object) -> object:
        if asyncio.iscoroutinefunction(self.handler):
            return await self.handler(**kwargs)
        return self.handler(**kwargs)


class Server:
    def __init__(
        self,
        tools: list[Tool] | None = None,
        resources: list[Resource] | None = None,
        prompts: list[Prompt] | None = None,
    ):
        self.tools = tools or []
        self.resources = resources or []
        self.prompts = prompts or []
    
    def add_tool(self, tool: Tool) -> None:
        self.tools.append(tool)
    
    def add_resource(self, resource: Resource) -> None:
        self.resources.append(resource)
    
    def add_prompt(self, prompt: Prompt) -> None:
        self.prompts.append(prompt)
