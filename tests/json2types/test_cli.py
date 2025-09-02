import io
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from inline_snapshot import snapshot

from json2types.cli import create_parser, main, read_schema, resolve_args


def test_cli_help():
    """Test CLI help output."""
    parser = create_parser()
    help_output = parser.format_help()

    assert help_output == snapshot("""\
usage: json2types [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--version] [input] [output]

Generate Python TypedDict types from JSON Schema.

positional arguments:
  input                 Input JSON Schema file (use '-' for stdin)
  output                Output Python file path

options:
  -h, --help            show this help message and exit
  -i, --input INPUT_FILE
                        Input JSON Schema file (alternative to positional)
  -o, --output OUTPUT_FILE
                        Output Python file path (alternative to positional)
  --version             show program's version number and exit

Examples:
  json2types schema.json types.py
  json2types --input schema.json --output types.py
  cat schema.json | json2types --output types.py
""")


def test_resolve_args_positional():
    """Test argument resolution with positional arguments."""
    parser = create_parser()
    args = parser.parse_args(["schema.json", "types.py"])

    input_source, output_dest = resolve_args(args)
    assert input_source == "schema.json"
    assert output_dest == "types.py"


def test_resolve_args_flags():
    """Test argument resolution with flag arguments."""
    parser = create_parser()
    args = parser.parse_args(["-i", "schema.json", "-o", "types.py"])

    input_source, output_dest = resolve_args(args)
    assert input_source == "schema.json"
    assert output_dest == "types.py"


def test_read_schema_file(tmp_path: Path):
    """Test reading schema from file."""
    test_schema = '{"type": "object"}'

    json_file = tmp_path / "schema.json"
    json_file.write_text(test_schema)

    content = read_schema(str(json_file.absolute()))
    assert content == test_schema


def test_read_schema_stdin():
    """Test reading schema from stdin."""
    test_schema = '{"type": "object"}'

    with patch("sys.stdin", io.StringIO(test_schema)):
        content = read_schema("-")
        assert content == test_schema


def test_cli_integration():
    """Test CLI end-to-end integration."""
    test_schema = """{
      "type": "object",
      "title": "TestCLI",
      "properties": {
        "name": {"type": "string"}
      }
    }"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as schema_file:
        schema_file.write(test_schema)
        schema_file.flush()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as output_file:
            # Test CLI with mocked sys.argv
            test_args = ["json2types", schema_file.name, output_file.name]

            with patch.object(sys, "argv", test_args):
                with patch("sys.stdout", io.StringIO()) as mock_stdout:
                    main()

                    # Check success message
                    output = mock_stdout.getvalue()
                    assert f"Generated types from {schema_file.name} -> {output_file.name}" in output

            # Check generated content
            generated_content = Path(output_file.name).read_text()
            assert generated_content == snapshot("""\
from typing_extensions import TypedDict, NotRequired

class TestCLI(TypedDict):
    name: NotRequired[str]\
""")

            # Cleanup
            Path(schema_file.name).unlink()
            Path(output_file.name).unlink()
