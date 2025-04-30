"""proto-to-mcp: Convert Protocol Buffer (Protobuf) schema files to Model Context Protocol (MCP) servers."""

__version__ = "0.1.0"

from .converter import convert_mcp_to_proto, convert_proto_to_mcp
from .generator import MCPServerGenerator
from .grpc_client import GRPCClient
from .parser import ProtoParser

__all__ = [
    "GRPCClient",
    "MCPServerGenerator",
    "ProtoParser",
    "convert_mcp_to_proto",
    "convert_proto_to_mcp",
]
