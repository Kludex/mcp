from inline_snapshot import snapshot
from mcp_client import MCPClient

from mcplette.applications import MCP


def test_mcp_init():
    mcp = MCP()

    @mcp.tool()
    async def sum(a: int, b: int) -> int:
        return a + b

    client = MCPClient(mcp)
    response = client.call_tool("sum", {"a": 1, "b": 2})  # type: ignore
    assert response == snapshot({"content": [{"text": "3", "type": "text"}]})
