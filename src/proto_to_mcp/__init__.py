"""
proto-to-mcp: Convert Protocol Buffer (Protobuf) schema files to Model Context Protocol (MCP) servers
"""

__version__ = "0.1.0"

from .parser import ProtoParser
from .generator import MCPServerGenerator
from .converter import convert_proto_to_mcp, convert_mcp_to_proto
from .grpc_client import GRPCClient

__all__ = [
    "ProtoParser",
    "MCPServerGenerator",
    "convert_proto_to_mcp",
    "convert_mcp_to_proto",
    "GRPCClient",
]
