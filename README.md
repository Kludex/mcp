This is an opinionated implementation of the MCP specification.

The `mcplette` structure works as follows:

1. You need to instantiate a `MCP` object, that will hold the `tools`, `prompts` and `resources`
2. You'll need to expose that into one of the `Router` classes, e.g. `WebSocketRouter`, so you'll have:
    ```py
    from mcplette.applications import MCP
    from starlette.applications import Starlette

    mcp = MCP(tools=..., resources=...)
    ```
