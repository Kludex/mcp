from inline_snapshot import snapshot
from starlette.testclient import TestClient

from mcplette.applications import MCP


def test_mcp_init():
    mcp = MCP()

    @mcp.tool()
    async def sum(a: int, b: int) -> int:
        return a + b

    client = TestClient(mcp)
    response = client.put("/tools/sum/calls/1")
    assert response.status_code == 200
    assert response.json() == {"result": 3}
