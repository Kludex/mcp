"""Command-line interface for json2types."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .generator import generate_types


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="json2types",
        description="Generate Python TypedDict types from JSON Schema.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  json2types schema.json types.py
  json2types --input schema.json --output types.py
  cat schema.json | json2types --output types.py
        """.strip(),
    )

    parser.add_argument("input", nargs="?", help="Input JSON Schema file (use '-' for stdin)")
    parser.add_argument("output", nargs="?", help="Output Python file path")
    parser.add_argument("-i", "--input", dest="input_file", help="Input JSON Schema file (alternative to positional)")
    parser.add_argument(
        "-o", "--output", dest="output_file", help="Output Python file path (alternative to positional)"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    return parser


def resolve_args(args: argparse.Namespace) -> tuple[str, str]:
    """Resolve input and output arguments."""
    # Determine input source
    input_source = args.input or args.input_file
    if not input_source:
        if not sys.stdin.isatty():
            input_source = "-"  # Use stdin
        else:
            raise ValueError("No input specified. Provide a file path or pipe data to stdin.")

    # Determine output destination
    output_dest = args.output or args.output_file
    if not output_dest:
        raise ValueError("Output file path is required.")

    return input_source, output_dest


def read_schema(input_path: str) -> str:
    """Read JSON schema from file or stdin."""
    if input_path == "-":
        return sys.stdin.read()
    else:
        return Path(input_path).read_text(encoding="utf-8")


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        input_source, output_dest = resolve_args(args)

        # Read the schema
        schema_content = read_schema(input_source)

        # Generate types
        output_content = generate_types(schema_content)
        Path(output_dest).write_text(output_content)

        # Success message
        input_desc = "stdin" if input_source == "-" else input_source
        print(f"Generated types from {input_desc} -> {output_dest}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
