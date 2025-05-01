#!/usr/bin/env python3

import argparse
import logging
import os
from typing import Any, cast

from fastmcp import FastMCP

from proto_to_mcp.converter import convert_proto_to_mcp
from proto_to_mcp.grpc_client import GRPCClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Global MCP Instance and gRPC Client ---
# Initialize outside the class structure for easier decorator application
mcp: FastMCP = FastMCP(
    name="SimpleMCPServer",
    instructions="MCP server for simple.example services",
)
grpc_client: GRPCClient | None = None

# --- Message classes ---
class HelloRequest:
    """Represents the HelloRequest message from the Protobuf definition."""

    def __init__(self, name: str | None = None):
        self.name = name

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.name is not None:
            result['name'] = self.name
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'HelloRequest':
        """Create a HelloRequest from a dictionary."""
        instance = HelloRequest()
        if 'name' in data:
            instance.name = data['name']
        return instance


class HelloResponse:
    """Represents the HelloResponse message from the Protobuf definition."""

    def __init__(self, greeting: str | None = None, timestamp: str | None = None):
        self.greeting = greeting
        self.timestamp = timestamp

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.greeting is not None:
            result['greeting'] = self.greeting
        if self.timestamp is not None:
            result['timestamp'] = self.timestamp
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'HelloResponse':
        """Create a HelloResponse from a dictionary."""
        instance = HelloResponse()
        if 'greeting' in data:
            instance.greeting = data['greeting']
        if 'timestamp' in data:
            instance.timestamp = data['timestamp']
        return instance


class UserRequest:
    """Represents the UserRequest message from the Protobuf definition."""

    def __init__(self, user_id: int | None = None):
        self.user_id = user_id

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.user_id is not None:
            result['user_id'] = self.user_id
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'UserRequest':
        """Create a UserRequest from a dictionary."""
        instance = UserRequest()
        if 'user_id' in data:
            instance.user_id = data['user_id']
        return instance


class UserProfile:
    """Represents the UserProfile message from the Protobuf definition."""

    def __init__(self, full_name: str | None = None, age: int | None = None, interests: list[str] | None = None):
        self.full_name = full_name
        self.age = age
        self.interests = interests

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.full_name is not None:
            result['full_name'] = self.full_name
        if self.age is not None:
            result['age'] = self.age
        if self.interests is not None:
            result['interests'] = self.interests
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'UserProfile':
        """Create a UserProfile from a dictionary."""
        instance = UserProfile()
        if 'full_name' in data:
            instance.full_name = data['full_name']
        if 'age' in data:
            instance.age = data['age']
        if 'interests' in data:
            instance.interests = data['interests']
        return instance


class UserResponse:
    """Represents the UserResponse message from the Protobuf definition."""

    def __init__(self, user_id: int | None = None, username: str | None = None, email: str | None = None, active: bool | None = None, profile: UserProfile | None = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.active = active
        self.profile = profile

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.user_id is not None:
            result['user_id'] = self.user_id
        if self.username is not None:
            result['username'] = self.username
        if self.email is not None:
            result['email'] = self.email
        if self.active is not None:
            result['active'] = self.active
        if self.profile is not None:
            result['profile'] = self.profile.to_dict()
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'UserResponse':
        """Create a UserResponse from a dictionary."""
        instance = UserResponse()
        if 'user_id' in data:
            instance.user_id = data['user_id']
        if 'username' in data:
            instance.username = data['username']
        if 'email' in data:
            instance.email = data['email']
        if 'active' in data:
            instance.active = data['active']
        if data.get('profile'):
            instance.profile = UserProfile.from_dict(data['profile'])
        return instance


# --- Tool Definitions ---
# Decorated with the global mcp instance

@mcp.tool()
def say_hello(name: str | None = None) -> dict[str, Any]:
    """Call the SayHello RPC from GreeterService.

    Args:
        name: The name field for the HelloRequest message
    """
    request = HelloRequest(name=name)

    if grpc_client:
        response = grpc_client.call_method('GreeterService', 'SayHello', request.to_dict())
        return cast(dict[str, Any], convert_proto_to_mcp(response, 'HelloResponse'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for GreeterService.SayHello')
        return {'error': 'No gRPC server configured'}


@mcp.tool()
def get_user(user_id: int | None = None) -> dict[str, Any]:
    """Call the GetUser RPC from GreeterService.

    Args:
        user_id: The user_id field for the UserRequest message
    """
    request = UserRequest(user_id=user_id)

    if grpc_client:
        response = grpc_client.call_method('GreeterService', 'GetUser', request.to_dict())
        return cast(dict[str, Any], convert_proto_to_mcp(response, 'UserResponse'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for GreeterService.GetUser')
        return {'error': 'No gRPC server configured'}


# --- Main Execution ---

def main() -> None:
    """Run the MCP server."""
    global grpc_client # Allow modification of the global client

    parser = argparse.ArgumentParser(description='Run the SimpleMCPServer')
    parser.add_argument('--grpc-server', '-g', help='Address of the gRPC server to connect to')
    parser.add_argument('--transport', '-t', help='Transport to use (stdio, sse)', default="stdio")
    parser.add_argument('--host', '-H', help='Host to use', default="127.0.0.1")
    parser.add_argument('--port', '-p', help='Port to use', default=9000)
    args = parser.parse_args()

    # Initialize the gRPC client if address is provided
    grpc_addr = args.grpc_server or os.getenv("GRPC_SERVER")
    if grpc_addr:
        grpc_client = GRPCClient(grpc_addr)
        logger.info(f"Attempting to connect to gRPC server at {grpc_addr}")
    else:
        logger.warning("No gRPC server address provided via argument or environment variable.")

    mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
