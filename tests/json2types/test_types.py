import pytest
from inline_snapshot import snapshot

from json2types import generate_types


@pytest.mark.parametrize(
    "schema, output",
    [
        pytest.param(
            """
{
  "type": "object",
  "title": "Primitives",
  "properties": {
    "text": {"type": "string"},
    "count": {"type": "integer"},
    "price": {"type": "number"},
    "active": {"type": "boolean"},
    "nothing": {"type": "null"}
  }
}
  """,
            snapshot("""\
from typing_extensions import TypedDict, NotRequired

class Primitives(TypedDict):
    text: NotRequired[str]
    count: NotRequired[int]
    price: NotRequired[float]
    active: NotRequired[bool]
    nothing: NotRequired[None]\
"""),
            id="basic-types",
        ),
        pytest.param(
            """{
      "type": "object",
      "title": "ArrayTest",
      "properties": {
        "tags": {
          "type": "array",
          "items": {"type": "string"}
        },
        "numbers": {
          "type": "array",
          "items": {"type": "integer"}
        }
      }
    }""",
            snapshot("""\
from typing_extensions import TypedDict, NotRequired

class ArrayTest(TypedDict):
    tags: NotRequired[list[str]]
    numbers: NotRequired[list[int]]\
"""),
            id="array",
        ),
        pytest.param(
            """{
      "type": "object",
      "title": "RequiredTest",
      "properties": {
        "required_field": {"type": "string"},
        "optional_field": {"type": "string"}
      },
      "required": ["required_field"]
    }""",
            snapshot("""\
from typing_extensions import TypedDict, NotRequired

class RequiredTest(TypedDict):
    required_field: str
    optional_field: NotRequired[str]\
"""),
            id="required-optional",
        ),
        pytest.param(
            """{
      "type": "object",
      "title": "Company",
      "properties": {
        "name": {"type": "string"},
        "ceo": {"$ref": "#/$defs/Person"},
        "employees": {
          "type": "array",
          "items": {"$ref": "#/$defs/Person"}
        }
      },
      "required": ["name", "ceo"],
      "$defs": {
        "Person": {
          "type": "object",
          "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "age": {"type": "integer"}
          },
          "required": ["firstName", "lastName"]
        }
      }
    }""",
            snapshot("""\
from pydantic import Field
from typing import Annotated
from typing_extensions import TypedDict, NotRequired

class Person(TypedDict):
    first_name: Annotated[str, Field(alias='firstName')]
    last_name: Annotated[str, Field(alias='lastName')]
    age: NotRequired[int]

class Company(TypedDict):
    name: str
    ceo: Person
    employees: NotRequired[list[Person]]\
"""),
            id="internal-refs",
        ),
        pytest.param(
            """{
      "type": "object",
      "title": "NamingTest",
      "properties": {
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "userId": {"type": "integer"},
        "isActive": {"type": "boolean"},
        "snake_case": {"type": "string"},
        "ALLCAPS": {"type": "string"}
      }
    }""",
            snapshot("""\
from pydantic import Field
from typing import Annotated
from typing_extensions import TypedDict, NotRequired

class NamingTest(TypedDict):
    first_name: Annotated[NotRequired[str], Field(alias='firstName')]
    last_name: Annotated[NotRequired[str], Field(alias='lastName')]
    user_id: Annotated[NotRequired[int], Field(alias='userId')]
    is_active: Annotated[NotRequired[bool], Field(alias='isActive')]
    snake_case: NotRequired[str]
    allcaps: Annotated[NotRequired[str], Field(alias='ALLCAPS')]\
"""),
            id="field-name-conversion",
        ),
        pytest.param(
            """{
      "type": "object",
      "title": "UserProfile",
      "properties": {
        "nested": {
          "type": "object",
          "properties": {
            "value": {"type": "string"}
          }
        }
      }
    }""",
            snapshot("""\
from typing_extensions import TypedDict, NotRequired

class Nested(TypedDict):
    value: NotRequired[str]

class UserProfile(TypedDict):
    nested: NotRequired[Nested]\
"""),
            id="class-name-conversion",
        ),
        pytest.param(
            """{
      "type": "object",
      "title": "User",
      "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "address": {
          "type": "object",
          "title": "Address",
          "properties": {
            "street": {"type": "string"},
            "city": {"type": "string"},
            "zipCode": {"type": "string"}
          },
          "required": ["street", "city"]
        },
        "preferences": {
          "type": "object",
          "properties": {
            "theme": {"type": "string"},
            "notifications": {"type": "boolean"}
          }
        }
      },
      "required": ["name", "address"]
    }""",
            snapshot("""\
from pydantic import Field
from typing import Annotated
from typing_extensions import TypedDict, NotRequired

class Address(TypedDict):
    street: str
    city: str
    zip_code: Annotated[NotRequired[str], Field(alias='zipCode')]

class Preferences(TypedDict):
    theme: NotRequired[str]
    notifications: NotRequired[bool]

class User(TypedDict):
    name: str
    age: NotRequired[int]
    address: Address
    preferences: NotRequired[Preferences]\
"""),
            id="nested-objects",
        ),
    ],
)
def test_types(schema: str, output: str):
    """Test basic primitive types."""
    assert generate_types(schema) == output
