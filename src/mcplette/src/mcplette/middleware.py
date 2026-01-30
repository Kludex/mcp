"""Middleware system for MCPLette.

MCPLette uses a generator-based middleware pattern for clean request/response
handling. This pattern allows middleware to execute code before and after the
handler, with clear control flow via `yield`.

Middleware Pattern
==================

    class MyMiddleware(MCPMiddleware):
        async def dispatch(self, request: MCPRequest) -> AsyncGenerator[None, MCPResponse]:
            # Pre-processing (before handler)
            response = yield  # Handler executes here
            # Post-processing (after handler, can inspect/modify response)

Execution Flow
==============

    Request arrives
        ↓
    Middleware pre-yield (outer → inner)
        ↓
    Handler executes
        ↓
    Middleware post-yield (inner → outer)
        ↓
    Response sent

Short-circuiting
================

Middleware can short-circuit by raising an MCPError instead of yielding:

    class AuthMiddleware(MCPMiddleware):
        async def dispatch(self, request: MCPRequest) -> AsyncGenerator[None, MCPResponse]:
            if not request.context.get("authenticated"):
                raise MCPError(code=-32600, message="Unauthorized")
            response = yield

Function-based Middleware
=========================

For simple cases, use the @middleware decorator:

    @middleware
    async def logging_middleware(request: MCPRequest) -> AsyncGenerator[None, MCPResponse]:
        start = time.time()
        response = yield
        logger.info(f"{request.method} took {time.time() - start}s")

"""

from collections.abc import AsyncGenerator, Callable


class MCPRequest: ...


class MCPResponse: ...


class MCPMiddleware:
    async def dispatch(self, request: MCPRequest) -> AsyncGenerator[None, MCPResponse]:
        yield


MiddlewareFunc = Callable[[MCPRequest], AsyncGenerator[None, MCPResponse]]
