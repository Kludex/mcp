# This file downloads the schema from https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-06-18/schema.json
# and checks if the `mcp_types/__init__.py` file is up to date.

import difflib
import subprocess
import tempfile
from pathlib import Path

import httpx
import pytest

from json2types import generate_types

MCP_SCHEMA_URL = "https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/refs/heads/main/schema/2025-11-25/schema.json"
MCP_TYPES_PATH = Path(__file__).parent.parent / "src" / "mcp-types" / "mcp_types" / "__init__.py"


def format_with_ruff(code: str) -> str:
    """Format Python code using ruff format."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(code)
        temp_path = Path(temp_file.name)

    try:
        subprocess.run(["uv", "run", "ruff", "format", str(temp_path)], capture_output=True, text=True, check=True)
        subprocess.run(
            ["uv", "run", "ruff", "check", "--fix", "--fix-only", str(temp_path)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Read the formatted code back
        formatted_code = temp_path.read_text()
        return formatted_code
    except subprocess.CalledProcessError as e:
        # If ruff format fails, return the original code
        print(f"Warning: ruff format failed: {e}")
        return code
    finally:
        # Clean up the temporary file
        temp_path.unlink(missing_ok=True)


def test_mcp_types_up_to_date() -> None:
    """Test that mcp_types/__init__.py is up to date with the latest MCP schema."""
    # Download the schema
    response = httpx.get(MCP_SCHEMA_URL)
    response.raise_for_status()
    schema_json: str = response.text

    # Write the file to `tests/mcp_schema.json` if it doesn't exist.
    mcp_schema_path = Path(__file__).parent / "mcp_schema.json"
    if not mcp_schema_path.exists():
        mcp_schema_path.write_text(schema_json)
    else:
        # Read the existing schema
        existing_schema = mcp_schema_path.read_text()
        # Compare the existing schema with the downloaded schema
        if existing_schema != schema_json:
            mcp_schema_path.write_text(schema_json)
            pytest.fail("mcp_schema.json was out of date. It has been updated.")

    # Generate types using json2types
    generated_types = generate_types(schema_json)

    # Format the generated types with ruff
    formatted_generated_types = format_with_ruff(generated_types)

    # Read the existing mcp_types/__init__.py file
    existing_types = MCP_TYPES_PATH.read_text()

    # Compare the formatted generated types with existing types
    if formatted_generated_types.strip() != existing_types.strip():
        # Create a temporary file with the formatted generated types for inspection
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
            temp_file.write(formatted_generated_types)
            temp_path = Path(temp_file.name)

        # Generate diff between existing and formatted generated types
        diff = list(
            difflib.unified_diff(
                existing_types.splitlines(keepends=True),
                formatted_generated_types.splitlines(keepends=True),
                fromfile=str(MCP_TYPES_PATH),
                tofile="generated_from_schema",
                lineterm="",
            )
        )

        # Write the formatted generated types to the actual file
        MCP_TYPES_PATH.write_text(formatted_generated_types)

        # Show the diff and fail the test
        diff_text = "".join(diff)
        pytest.fail(
            f"mcp_types/__init__.py was out of date. File has been updated.\n\n"
            f"Diff:\n{diff_text}\n\n"
            f"Generated types have been written to: {MCP_TYPES_PATH}\n"
            f"Temporary generated file (for inspection): {temp_path}"
        )
