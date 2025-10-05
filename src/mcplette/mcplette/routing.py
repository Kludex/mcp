from __future__ import annotations as _annotations

from collections.abc import Callable, Sequence
from dataclasses import KW_ONLY, dataclass, field
from typing import Any, ParamSpec, TypeAlias, overload

from mcp_types import CallToolResult
from mcp_types import Params as CallToolParams
from pydantic import TypeAdapter
from pydantic.json_schema import GenerateJsonSchema
from starlette.requests import Request
from starlette.responses import Response

from ._function_schema import DocstringFormat, FunctionSchema, function_schema
from ._function_schema._json_schema import GenerateToolJsonSchema

ta_call_tool_params = TypeAdapter(CallToolParams)
ta_call_tool_result = TypeAdapter(CallToolResult)

ToolParams = ParamSpec("ToolParams", default=...)

Func: TypeAlias = Callable[ToolParams, Any]


class MCPRouter:
    def __init__(
        self,
        *,
        tools: Sequence[Tool] = (),
        resources: Sequence[Resource] = (),
        prompts: Sequence[Prompt] = (),
    ) -> None:
        self.tools = list(tools)
        self.resources = list(resources)
        self.prompts = list(prompts)

    def add_tool(self, name: str, handler: Callable[..., object], *, description: str | None = None) -> None:
        tool = Tool(name, handler, description=description)
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

    # Decorators

    @overload
    def tool(self) -> Callable[[Func[ToolParams]], Func[ToolParams]]: ...

    @overload
    def tool(self, func: Func[ToolParams]) -> Func[ToolParams]: ...

    def tool(self, func: Func[ToolParams] | None = None, *, name: str | None = None) -> Any:
        def tool_decorator(func_: Func[ToolParams]) -> Func[ToolParams]:
            self.tools.append(Tool(name=name, function=func_))
            return func_

        return tool_decorator if func is None else tool_decorator(func)

    def resource(
        self, uri: str, name: str | None = None, description: str | None = None, mime_type: str | None = None
    ) -> ...: ...

    def prompt(
        self, name: str, description: str | None = None, arguments: list[dict[str, object]] | None = None
    ) -> ...: ...

    # Endpoints

    async def handle_tools_call(self, request: Request) -> Response:
        tool_name = request.path_params["tool_name"]
        _ = request.path_params["tool_call_id"]

        params = ta_call_tool_params.validate_json(await request.body())

        # TODO(Marcelo): Create a smarter routing.
        for tool in self.tools:
            if tool.name == tool_name:
                result = await tool(params)
                return Response(content=result, status_code=200)

        return Response(status_code=404)


@dataclass(init=False, slots=True)
class Tool:
    name: str

    # TODO(Marcelo): This handler should be a generator, given that we can use
    # elicitation and sampling.
    function: Func
    description: str | None = None
    function_schema: FunctionSchema

    def __init__(
        self,
        function: Func,
        *,
        name: str | None = None,
        description: str | None = None,
        docstring_format: DocstringFormat = "auto",
        schema_generator: type[GenerateJsonSchema] = GenerateToolJsonSchema,
    ) -> None:
        self.function = function
        self.function_schema = function_schema(function, schema_generator=schema_generator)
        self.name = name or self.function.__name__
        self.description = description or self.function_schema.description

    async def __call__(self, request: CallToolParams) -> CallToolResult: ...


@dataclass(slots=True)
class Resource:
    uri: str
    function: Callable[..., Any]

    _ = KW_ONLY

    name: str | None = None
    description: str | None = None
    mime_type: str | None = None

    def __post_init__(self):
        self.name = self.name or self.uri.split("/")[-1]


@dataclass(slots=True)
class Prompt:
    name: str
    function: Callable[..., Any]

    _ = KW_ONLY

    description: str | None = None
    arguments: list[dict[str, object]] | None = field(default_factory=list)
