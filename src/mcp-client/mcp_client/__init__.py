from __future__ import annotations as _annotations

import uuid

from mcp_types import Arguments, CallToolResult
from pydantic import TypeAdapter
from starlette.testclient import TestClient

ta_call_tool_result = TypeAdapter(CallToolResult)


class MCPClient(TestClient):
    def call_tool(
        self,
        tool_name: str,
        arguments: Arguments,
        *,
        tool_call_id: str | None = None,
    ) -> CallToolResult:
        tool_call_id = tool_call_id or str(uuid.uuid4())
        response = self.put(
            f"/tools/{tool_name}/calls/{tool_call_id}",
            json={"arguments": arguments, "name": tool_name},
        )
        breakpoint()
        return ta_call_tool_result.validate_json(response.content)
