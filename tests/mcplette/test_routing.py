import pytest
from inline_snapshot import snapshot

from mcplette._context import RunContext
from mcplette.routing import Tool

pytestmark = pytest.mark.anyio


async def test_tool():
    async def sum(a: int, b: int) -> int:
        return a + b

    tool = Tool(function=sum)
    assert tool.function_schema.json_schema == snapshot(
        {
            "additionalProperties": False,
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
            "type": "object",
        }
    )
    assert await tool.function_schema.call({"a": 1, "b": 2}, RunContext()) == 3


async def test_tool_with_context():
    async def sum(ctx: RunContext[int], a: int, b: int) -> int:
        return a + b

    tool = Tool(function=sum)
    assert tool.function_schema.json_schema == snapshot(
        {
            "additionalProperties": False,
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
            "type": "object",
        }
    )
    assert await tool.function_schema.call({"a": 1, "b": 2}, RunContext()) == 3


async def test_tool_with_context_as_second_argument():
    async def sum(a: int, ctx: RunContext[int], b: int) -> int:
        return a + b

    tool = Tool(function=sum)
    assert tool.function_schema.json_schema == snapshot(
        {
            "additionalProperties": False,
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
            "type": "object",
        }
    )
    assert await tool.function_schema.call({"a": 1, "b": 2}, RunContext()) == 3
