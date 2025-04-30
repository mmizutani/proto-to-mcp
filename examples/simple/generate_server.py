"""
Simple example of using proto-to-mcp to generate an MCP server from a Protobuf schema.
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path to import proto_to_mcp
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from proto_to_mcp.parser import ProtoParser
from proto_to_mcp.generator import MCPServerGenerator


def main():
    """Generate an MCP server from a simple Protobuf schema."""
    # Path to the example .proto file
    proto_file = os.path.join(os.path.dirname(__file__), "simple.proto")

    # Parse the proto file
    print(f"Parsing Protobuf schema file: {proto_file}")
    parser = ProtoParser(proto_file)

    # Generate the MCP server
    output_file = os.path.join(os.path.dirname(__file__), "simple_mcp_server.py")
    print(f"Generating MCP server to: {output_file}")
    generator = MCPServerGenerator(parser)
    generator.generate_server_code(output_file)

    print(f"MCP server generated successfully: {output_file}")
    print("You can run it with: python simple_mcp_server.py")


if __name__ == "__main__":
    main()
