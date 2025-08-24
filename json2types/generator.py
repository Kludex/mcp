"""Core generator for converting JSON Schema to Python TypedDict."""

from __future__ import annotations as _annotations

import ast
import json
import re
from enum import Enum
from typing import Any

from pydantic.alias_generators import to_pascal


class JsonSchemaVersion(Enum):
    """Supported JSON Schema versions."""

    DRAFT_7 = "draft7"
    DRAFT_2020_12 = "2020-12"

    @classmethod
    def detect_version(cls, schema: dict[str, Any]) -> JsonSchemaVersion:
        """Detect JSON Schema version from $schema field."""
        schema_uri = schema.get("$schema", "")

        if "2020-12" in schema_uri:
            return cls.DRAFT_2020_12
        elif "draft-07" in schema_uri or "draft/07" in schema_uri:
            return cls.DRAFT_7
        else:
            # Default to 2020-12 if no $schema specified
            return cls.DRAFT_2020_12


def generate_types(json_schema: str) -> str:
    """Generate Python TypedDict types from JSON Schema.

    Args:
        json_schema: JSON Schema as string
        output_path: The python module that has the types.
    """
    schema_dict = json.loads(json_schema)
    generator = TypeGenerator(schema_dict)
    return generator.generate()


class TypeGenerator:
    """Generates Python TypedDict classes from JSON Schema using AST."""

    def __init__(self, schema: dict[str, Any]):
        self.schema = schema
        self.version = JsonSchemaVersion.detect_version(schema)
        self.imports: set[str] = set()
        self.class_nodes: list[ast.stmt] = []
        # Cache for definitions to avoid duplicates
        self.definitions: dict[str, dict[str, Any]] = {}
        self.processed_refs: dict[str, str] = {}  # ref_uri -> class_name

        if self.version == JsonSchemaVersion.DRAFT_2020_12:
            # JSON Schema 2020-12 uses $defs
            self.definitions = self.schema.get("$defs", {})
        else:
            # JSON Schema Draft 7 uses definitions
            self.definitions = self.schema.get("definitions", {})

    def generate(self) -> str:
        """Generate the complete Python module."""
        self._process_schema(self.schema)
        return self._build_module()

    def _resolve_ref(self, ref_uri: str) -> dict[str, Any]:
        """Resolve a $ref URI to the actual schema."""
        # Handle internal references
        if ref_uri.startswith("#/"):
            # Remove "#/" prefix and split path
            path_parts = ref_uri[2:].split("/")

            if len(path_parts) >= 2:
                expected_root = "$defs" if self.version == JsonSchemaVersion.DRAFT_2020_12 else "definitions"

                if path_parts[0] == expected_root:
                    def_name = path_parts[1]
                    if def_name in self.definitions:
                        return self.definitions[def_name]

        # If reference not found, return empty object (will become Any)
        return {}

    def _process_schema(self, schema: dict[str, Any], context_name: str = "") -> ast.expr:
        """Process a schema object and return the type AST node."""
        # TODO(Marcelo): This is completely wrong. Ask the LLM to fix it.
        if "definitions" in schema:
            for name, definition in schema["definitions"].items():
                result = self._process_schema(definition, name)
        elif "$ref" in schema:
            ref_uri = schema["$ref"]

            # Check if we've already processed this reference
            if ref_uri in self.processed_refs:
                class_name = self.processed_refs[ref_uri]
                return ast.Name(id=class_name, ctx=ast.Load())

            resolved_schema = self._resolve_ref(ref_uri)
            if resolved_schema:
                # Generate class name from the reference path
                if ref_uri.startswith("#/"):
                    path_parts: list[str] = ref_uri[2:].split("/")
                    ref_class_name: str = path_parts[-1] if path_parts else context_name or "GeneratedType"
                else:
                    ref_class_name = context_name or "GeneratedType"

                result = self._process_schema(resolved_schema, ref_class_name)

                # Cache the result if it's a class reference
                if isinstance(result, ast.Name):
                    self.processed_refs[ref_uri] = result.id
                return result
        if schema.get("type") == "object":
            return self._process_object(schema, context_name)
        elif schema.get("type") == "array":
            return self._process_array(schema)
        else:
            return self._process_primitive(schema)

    def _process_object(self, schema: dict[str, Any], context_name: str = "") -> ast.Name:
        """Process an object schema and generate TypedDict class."""
        title = schema.get("title")
        if not title and context_name:
            # Generate name from context (e.g., "preferences" -> "Preferences")
            title = to_pascal(context_name)
        elif not title:
            title = "GeneratedType"

        properties = schema.get("properties", {})
        required = set(schema.get("required", []))

        # Create class body (annotations)
        annotations: list[ast.stmt] = []

        for prop_name, prop_schema in properties.items():
            field_name = self._to_field_name(prop_name)
            field_type = self._process_schema(prop_schema, prop_name)

            # Handle optional fields with NotRequired
            if prop_name not in required:
                self.imports.add("typing_extensions")
                field_type = self._create_subscript("NotRequired", [field_type])

            # Add Field annotation for alias
            if field_name != prop_name:
                self.imports.add("typing_extensions")
                self.imports.add("pydantic")

                field_call = self._create_field_call(prop_name)
                field_type = self._create_subscript("Annotated", [field_type, field_call])

            # Create annotation node
            annotation = ast.AnnAssign(
                target=ast.Name(id=field_name, ctx=ast.Store()), annotation=field_type, value=None, simple=1
            )
            annotations.append(annotation)

        # Create TypedDict base
        self.imports.add("typing_extensions")
        bases: list[ast.expr] = [ast.Name(id="TypedDict", ctx=ast.Load())]

        # Create class node
        body_nodes: list[ast.stmt] = annotations if annotations else [ast.Pass()]
        class_node = ast.ClassDef(name=title, bases=bases, keywords=[], decorator_list=[], body=body_nodes)

        self.class_nodes.append(class_node)
        return ast.Name(id=title, ctx=ast.Load())

    def _process_array(self, schema: dict[str, Any]) -> ast.Subscript:
        """Process an array schema."""
        items_schema = schema.get("items", {})
        item_type = self._process_schema(items_schema)
        return self._create_subscript("list", [item_type])

    def _process_primitive(self, schema: dict[str, Any]) -> ast.expr:
        """Process primitive types."""
        type_mapping = {"string": "str", "number": "float", "integer": "int", "boolean": "bool", "null": "None"}

        schema_type: Any = schema.get("type")
        if isinstance(schema_type, str) and schema_type in type_mapping:
            return ast.Name(id=type_mapping[schema_type], ctx=ast.Load())

        # Handle union types (multiple types)
        if isinstance(schema_type, list):
            types: list[ast.expr] = []
            for t_any in schema_type:  # type: ignore[reportUnknownVariableType]
                if isinstance(t_any, str) and t_any in type_mapping:
                    types.append(ast.Name(id=type_mapping[t_any], ctx=ast.Load()))
                else:
                    types.append(ast.Name(id="Any", ctx=ast.Load()))
            if len(types) > 1:
                return self._create_union(types)
            return types[0]

        return ast.Name(id="Any", ctx=ast.Load())

    def _create_subscript(self, value: str, slices: list[ast.expr]) -> ast.Subscript:
        """Create a subscript node like list[int] or Annotated[str, Field()]."""
        if len(slices) == 1:
            slice_node = slices[0]
        else:
            slice_node = ast.Tuple(elts=slices, ctx=ast.Load())

        return ast.Subscript(value=ast.Name(id=value, ctx=ast.Load()), slice=slice_node, ctx=ast.Load())

    def _create_union(self, types: list[ast.expr]) -> ast.expr:
        """Create union type using | operator."""
        result: ast.expr = types[0]
        for type_node in types[1:]:
            result = ast.BinOp(left=result, op=ast.BitOr(), right=type_node)
        return result

    def _create_field_call(self, alias: str) -> ast.Call:
        """Create Field(alias="...") call."""
        return ast.Call(
            func=ast.Name(id="Field", ctx=ast.Load()),
            args=[],
            keywords=[ast.keyword(arg="alias", value=ast.Constant(value=alias))],
        )

    def _to_field_name(self, name: str) -> str:
        """Convert to snake_case field name."""
        s1 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        return s1.lower()

    def _build_module(self) -> str:
        """Build the final Python module from AST."""
        # Create import statements
        import_nodes: list[ast.stmt] = []
        for module in sorted(self.imports):
            if module == "typing_extensions":
                names: list[ast.alias] = []
                # Check if we need specific imports by examining class nodes
                temp_module = ast.Module(body=self.class_nodes, type_ignores=[])
                code_str = ast.unparse(temp_module)
                if "TypedDict" in code_str:
                    names.append(ast.alias(name="TypedDict"))
                if "NotRequired" in code_str:
                    names.append(ast.alias(name="NotRequired"))
                if "Annotated" in code_str:
                    names.append(ast.alias(name="Annotated"))

                if names:
                    import_nodes.append(ast.ImportFrom(module="typing_extensions", names=names, level=0))
            elif module == "pydantic":
                import_nodes.append(ast.ImportFrom(module="pydantic", names=[ast.alias(name="Field")], level=0))

        # Create complete module
        all_nodes: list[ast.stmt] = import_nodes + self.class_nodes
        module = ast.Module(body=all_nodes, type_ignores=[])

        return ast.unparse(module)
