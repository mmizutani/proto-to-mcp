"""
Command-line interface for proto-to-mcp.
"""
import os
import sys
import argparse
import logging
from typing import List, Optional

from .parser import ProtoParser
from .generator import MCPServerGenerator


logger = logging.getLogger(__name__)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the proto-to-mcp CLI.

    Args:
        args (Optional[List[str]]): Command-line arguments

    Returns:
        int: Exit code
    """
    parser = argparse.ArgumentParser(
        description="Convert Protobuf schema files to MCP server implementations"
    )
    parser.add_argument(
        "proto_file",
        help="Path to the .proto file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path for the generated MCP server file"
    )
    parser.add_argument(
        "--name", "-n",
        help="Name for the MCP server (defaults to the proto filename)"
    )
    parser.add_argument(
        "--grpc-server", "-g",
        help="Address of the gRPC server to connect to"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parsed_args = parser.parse_args(args)

    # Configure logging
    log_level = logging.DEBUG if parsed_args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    try:
        # Validate input file
        proto_file = parsed_args.proto_file
        if not os.path.exists(proto_file):
            logger.error(f"Proto file not found: {proto_file}")
            return 1
        
        if not proto_file.endswith(".proto"):
            logger.error(f"Input file must be a .proto file: {proto_file}")
            return 1

        # Determine output file
        output_file = parsed_args.output
        if not output_file:
            base_name = os.path.splitext(os.path.basename(proto_file))[0]
            output_file = f"{base_name}_mcp_server.py"
            logger.info(f"No output file specified, using: {output_file}")

        # Parse the proto file
        logger.info(f"Parsing proto file: {proto_file}")
        parser = ProtoParser(proto_file)
        
        # Generate the MCP server
        logger.info(f"Generating MCP server: {output_file}")
        generator = MCPServerGenerator(parser)
        generator.generate_server_code(
            output_file=output_file,
            server_name=parsed_args.name,
            grpc_server=parsed_args.grpc_server
        )
        
        logger.info(f"Successfully generated MCP server: {output_file}")
        return 0

    except Exception as e:
        logger.error(f"Error generating MCP server: {str(e)}", exc_info=parsed_args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())