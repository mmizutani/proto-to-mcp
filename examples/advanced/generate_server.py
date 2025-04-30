"""Advanced example of using proto-to-mcp with custom configurations and a gRPC backend."""
import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path to import proto_to_mcp
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from proto_to_mcp.generator import MCPServerGenerator
from proto_to_mcp.parser import ProtoParser


def main():
    """Generate an MCP server with advanced configurations."""
    parser = argparse.ArgumentParser(description='Generate an MCP server with custom configurations')
    parser.add_argument('--proto', default='advanced.proto', help='Input proto file')
    parser.add_argument('--output', default='advanced_mcp_server.py', help='Output MCP server file')
    parser.add_argument('--server-name', default='AdvancedMCPServer', help='Name for the MCP server class')
    parser.add_argument('--grpc-server', default='localhost:50051', help='Address of the gRPC server to connect to')
    args = parser.parse_args()

    # Get absolute paths
    proto_file = os.path.join(os.path.dirname(__file__), args.proto)
    output_file = os.path.join(os.path.dirname(__file__), args.output)

    # Parse the proto file
    print(f"Parsing Protobuf schema file: {proto_file}")
    parser = ProtoParser(proto_file)

    # Display parsed information
    print(f"Found package: {parser.get_package()}")
    print(f"Found services: {', '.join(parser.get_services().keys())}")
    print(f"Found messages: {', '.join(parser.get_messages().keys())}")

    # Generate the MCP server with custom configuration
    print(f"Generating MCP server to: {output_file}")
    generator = MCPServerGenerator(parser)
    generator.generate_server_code(
        output_file=output_file,
        server_name=args.server_name,
        grpc_server=args.grpc_server
    )

    print(f"MCP server generated successfully: {output_file}")
    print(f"You can run it with: python {args.output} --grpc-server={args.grpc_server}")
    print("Note: Make sure the gRPC server is running at the specified address")


if __name__ == "__main__":
    main()
