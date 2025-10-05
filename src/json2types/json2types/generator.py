"""Core generator for converting JSON Schema to Python TypedDict."""

from __future__ import annotations as _annotations

import ast
import json
import re
from enum import Enum
from typing import Any


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
        # Track generated class names to avoid duplicates
        self.class_names: set[str] = set()
        # Context stack for creating unique nested class names
        self.context_stack: list[str] = []

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

    def _to_class_name(self, name: str) -> str:
        """Convert name to proper PascalCase class name, preserving existing casing."""
        if not name:
            return "GeneratedType"

        # If already in PascalCase (starts with uppercase), keep it
        if name[0].isupper() and "_" not in name.lower():
            return name

        # Handle special underscore prefix like '_meta' -> 'Meta'
        if name.startswith("_"):
            return name[1:].capitalize()

        # Convert to PascalCase, handling compound words better than to_pascal
        # First, split on common word boundaries and capitalize each part
        import re

        # Handle camelCase input by inserting spaces before uppercase letters
        spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)

        # Split on spaces, underscores, and hyphens, then capitalize each word
        words = re.split(r"[\s_-]+", spaced)
        pascal_name = "".join(word.capitalize() for word in words if word)

        return pascal_name

    def _generate_unique_class_name(self, base_name: str, context_name: str = "", is_ref: bool = False) -> str:
        """Generate a unique class name, avoiding duplicates."""
        clean_name = self._to_class_name(base_name)

        # For $ref references, use the exact name from the reference without context prefixing
        if is_ref:
            unique_name = clean_name
        elif context_name and clean_name in self.class_names:
            # Create context-specific name like 'ElicitRequestParams'
            context_pascal = self._to_class_name(context_name)
            unique_name = f"{context_pascal}{clean_name}"
        else:
            unique_name = clean_name

        self.class_names.add(unique_name)
        return unique_name

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
        # Add context to stack for nested processing
        if context_name:
            self.context_stack.append(context_name)
        # Handle definitions - these should be processed to generate classes
        if "definitions" in schema:
            for name, definition in schema["definitions"].items():
                # Process each definition to generate the class
                self._process_schema(definition, name)
            # After processing definitions, continue with the main schema
            # Remove definitions to avoid infinite recursion
            schema = {k: v for k, v in schema.items() if k != "definitions"}

        # Handle $defs for JSON Schema 2020-12
        if "$defs" in schema:
            for name, definition in schema["$defs"].items():
                # Process each definition to generate the class
                self._process_schema(definition, name)
            # After processing $defs, continue with the main schema
            # Remove $defs to avoid infinite recursion
            schema = {k: v for k, v in schema.items() if k != "$defs"}

        # Handle anyOf for union types
        if "anyOf" in schema:
            any_of_schemas = schema["anyOf"]
            if any_of_schemas:
                types: list[ast.expr] = []
                for sub_schema in any_of_schemas:
                    types.append(self._process_schema(sub_schema, context_name))
                if len(types) == 1:
                    return types[0]
                return self._create_union(types)

        # Handle $ref references
        if "$ref" in schema:
            ref_uri = schema["$ref"]

            # Check if we've already processed this reference
            if ref_uri in self.processed_refs:
                class_name = self.processed_refs[ref_uri]
                return ast.Name(id=class_name, ctx=ast.Load())

            resolved_schema = self._resolve_ref(ref_uri)
            if resolved_schema:
                # Generate class name from the reference path, not context
                if ref_uri.startswith("#/"):
                    path_parts: list[str] = ref_uri[2:].split("/")
                    ref_class_name: str = path_parts[-1] if path_parts else "GeneratedType"
                else:
                    ref_class_name = "GeneratedType"

                # Process the schema with the ref class name (not context), marking it as a ref
                if resolved_schema.get("type") == "object":
                    result = self._process_object(resolved_schema, ref_class_name, is_ref=True)
                else:
                    result = self._process_schema(resolved_schema, ref_class_name)

                # Cache the result if it's a class reference
                if isinstance(result, ast.Name):
                    self.processed_refs[ref_uri] = result.id
                return result
            else:
                # If reference cannot be resolved, return Any
                return ast.Name(id="Any", ctx=ast.Load())

        try:
            # Handle different schema types
            if schema.get("type") == "object":
                return self._process_object(schema, context_name)
            elif schema.get("type") == "array":
                return self._process_array(schema)
            else:
                return self._process_primitive(schema)
        finally:
            # Remove context from stack when done
            if context_name and self.context_stack and self.context_stack[-1] == context_name:
                self.context_stack.pop()

    def _process_object(self, schema: dict[str, Any], context_name: str = "", is_ref: bool = False) -> ast.Name:
        """Process an object schema and generate TypedDict class."""
        title = schema.get("title")
        if not title and context_name:
            # Generate name from context (e.g., "preferences" -> "Preferences")
            title = context_name
        elif not title:
            title = "GeneratedType"

        # Get parent context for unique naming of nested classes
        parent_context = ""
        if not is_ref:
            if len(self.context_stack) >= 2:
                parent_context = self.context_stack[-2]
            elif len(self.context_stack) == 1:
                parent_context = self.context_stack[-1]

        # Generate unique class name
        unique_title = self._generate_unique_class_name(title, parent_context, is_ref)

        # If this class already exists, just return a reference to it
        if any(node.name == unique_title for node in self.class_nodes if isinstance(node, ast.ClassDef)):
            return ast.Name(id=unique_title, ctx=ast.Load())

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
                self.imports.add("typing")
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

        # Check if additionalProperties is true or an object schema
        additional_properties = schema.get("additionalProperties")
        decorator_list: list[ast.expr] = []
        if additional_properties is True or isinstance(additional_properties, dict):
            self.imports.add("pydantic")
            # Create @with_config(extra="allow") decorator
            decorator_list.append(
                ast.Call(
                    func=ast.Name(id="with_config", ctx=ast.Load()),
                    args=[],
                    keywords=[ast.keyword(arg="extra", value=ast.Constant(value="allow"))],
                )
            )

        # Create class node
        body_nodes: list[ast.stmt] = annotations if annotations else [ast.Pass()]
        class_node = ast.ClassDef(
            name=unique_title, bases=bases, keywords=[], decorator_list=decorator_list, body=body_nodes
        )

        self.class_nodes.append(class_node)
        return ast.Name(id=unique_title, ctx=ast.Load())

    def _process_array(self, schema: dict[str, Any]) -> ast.Subscript:
        """Process an array schema."""
        items_schema = schema.get("items", {})
        item_type = self._process_schema(items_schema)
        return self._create_subscript("list", [item_type])

    def _process_primitive(self, schema: dict[str, Any]) -> ast.expr:
        """Process primitive types."""
        # Handle const values as Literal types
        if "const" in schema:
            const_value = schema["const"]
            self.imports.add("typing")  # for Literal
            return self._create_subscript("Literal", [ast.Constant(value=const_value)])

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

        # Check if we need Any import
        temp_module = ast.Module(body=self.class_nodes, type_ignores=[])
        code_str = ast.unparse(temp_module)

        for module in sorted(self.imports):
            if module == "typing_extensions":
                names: list[ast.alias] = []
                if "TypedDict" in code_str:
                    names.append(ast.alias(name="TypedDict"))
                if "NotRequired" in code_str:
                    names.append(ast.alias(name="NotRequired"))

                if names:
                    import_nodes.append(ast.ImportFrom(module="typing_extensions", names=names, level=0))
            elif module == "typing":
                names = []
                if "Annotated" in code_str:
                    names.append(ast.alias(name="Annotated"))
                if "Literal" in code_str:
                    names.append(ast.alias(name="Literal"))

                if names:
                    import_nodes.append(ast.ImportFrom(module="typing", names=names, level=0))
            elif module == "pydantic":
                names = []
                if "Field" in code_str:
                    names.append(ast.alias(name="Field"))
                if "with_config" in code_str:
                    names.append(ast.alias(name="with_config"))

                if names:
                    import_nodes.append(ast.ImportFrom(module="pydantic", names=names, level=0))

        # Add Any import if needed
        if "Any" in code_str:
            import_nodes.insert(0, ast.ImportFrom(module="typing", names=[ast.alias(name="Any")], level=0))

        # Create complete module
        all_nodes: list[ast.stmt] = import_nodes + self.class_nodes
        module = ast.Module(body=all_nodes, type_ignores=[])

        return ast.unparse(module)
