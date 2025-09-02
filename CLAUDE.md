# mcplette Development Notes

## Type Annotations Standards

When working on this codebase, follow these type annotation conventions:

### Use Modern Union Syntax
- ✅ Use `str | None` instead of `Optional[str]`
- ✅ Use `dict[str, object]` instead of `Dict[str, Any]`
- ✅ Use `list[Tool]` instead of `List[Tool]`

### Avoid Generic Types
- ❌ Avoid `Any` type - use `object` for maximum generality
- ✅ Use `object` instead of `Any` for better type safety
- ✅ Use specific types when possible (e.g., `str`, `int`, `bool`)

### Import Strategy
- ✅ Import only what you need from `typing`
- ✅ Use built-in types (`dict`, `list`) instead of typing module equivalents
- ✅ Keep imports minimal - only import `Callable` from typing when needed

## Code Quality

### Type Checking
Always run `uv run pyright src/mcplette/` before committing changes to ensure:
- Zero type errors
- Zero type warnings  
- Proper type coverage

### Example Type Patterns

```python
# ✅ Good - Modern syntax, specific types
def process_data(
    items: list[dict[str, object]] | None = None,
    callback: Callable[[str], str] | None = None,
) -> dict[str, object]:
    pass

# ❌ Bad - Old syntax, Any usage
def process_data(
    items: Optional[List[Dict[str, Any]]] = None,
    callback: Optional[Callable[[str], Any]] = None,
) -> Dict[str, Any]:
    pass
```

## mcplette Architecture

The mcplette package implements a Starlette-inspired pattern for MCP servers:

- **Tool**: Encapsulates callable functions with schema validation
- **Resource**: Represents URI-based resources with content handlers  
- **Prompt**: Template-based prompt generation with parameters
- **Server**: Container that manages collections of tools, resources, and prompts

All classes support both synchronous and asynchronous handlers automatically.