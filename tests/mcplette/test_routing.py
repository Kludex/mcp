from inline_snapshot import snapshot

from mcplette._context import RunContext
from mcplette.routing import Tool


def test_tool():
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
    assert tool.function_schema.takes_ctx == snapshot(False)


def test_tool_with_context():
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
    assert tool.function_schema.takes_ctx == snapshot(True)


def test_tool_with_context_as_second_argument():
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
