from collections.abc import Sequence

from mcplette.middleware import MCPMiddleware

# TODO(Marcelo): Is this really the best I can do?


class MCPRoute:
    middleware: Sequence[MCPMiddleware]


class Tool(MCPRoute): ...


class Resource(MCPRoute): ...


class Prompt(MCPRoute): ...


class MCPRouter(MCPRoute):
    routes: Sequence[MCPRoute]


class ResourceRouter(MCPRoute):
    scheme: str
    routes: Sequence[MCPRoute]
