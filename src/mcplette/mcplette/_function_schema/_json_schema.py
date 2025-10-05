from typing import Any, Sequence

from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from pydantic_core import core_schema


class GenerateToolJsonSchema(GenerateJsonSchema):
    def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue:
        json_schema = super().typed_dict_schema(schema)
        # Workaround for https://github.com/pydantic/pydantic/issues/12123
        if "additionalProperties" not in json_schema:  # pragma: no branch
            extra = schema.get("extra_behavior") or schema.get("config", {}).get("extra_fields_behavior")
            if extra == "allow":
                extras_schema = schema.get("extras_schema", None)
                if extras_schema is not None:
                    json_schema["additionalProperties"] = self.generate_inner(extras_schema) or True
                else:
                    json_schema["additionalProperties"] = True  # pragma: no cover
            elif extra == "forbid":
                json_schema["additionalProperties"] = False
        return json_schema

    def _named_required_fields_schema(self, named_required_fields: Sequence[tuple[str, bool, Any]]) -> JsonSchemaValue:
        # Remove largely-useless property titles
        s = super()._named_required_fields_schema(named_required_fields)
        for p in s.get("properties", {}):
            s["properties"][p].pop("title", None)
        return s
