# Simple MCP Server Example

This example demonstrates how to use proto-to-mcp to generate and run a Model Context Protocol (MCP) server that wraps a gRPC service.

## Setup

### Install Dependencies

1. First, install proto-to-mcp from the project root:

```bash
# From the project root directory
cd ../..  # Go back to project root from examples/simple
uv pip install -e .
```

2. Then install the simple example dependencies:

```bash
# Go back to examples/simple
cd examples/simple
uv sync
```

Alternatively, you can use the provided Makefile to install dependencies:

```bash
make install
```

## Generating the Server Code

This example includes a utility script to generate the server code from a Proto file:

```bash
python generate_server.py
```

Or using the Makefile:

```bash
make generate
```

This will generate a new MCP server based on the simple.proto file in this directory. The output file will be named `simple_mcp_server.py`.

## Running the Server

After generating the code, you can run the MCP server with:

```bash
# From examples/simple directory
uv run fastmcp run simple_mcp_server.py:mcp
```

Or using the Makefile:

```bash
make run
```

By default, this starts the MCP server with the stdio transport.

### Command-line Options

- `--grpc-server` or `-g`: Address of the gRPC server to connect to (e.g., localhost:50051)
- `--transport` or `-t`: Transport to use (stdio, sse) (default: stdio)
- `--host` or `-H`: Host to bind the server to (default: 127.0.0.1)
- `--port` or `-p`: Port to bind the server to (default: 9000)

Example:

```bash
uv run fastmcp run simple_mcp_server.py:mcp --grpc-server localhost:50051 --port 8080 --transport sse
```

With the Makefile:

```bash
make run-with-port PORT=8080
# or
make run-with-grpc GRPC_SERVER=localhost:50051
# or
make run-with-sse
```

## Available Tools

The server exposes the following MCP tools:

1. `say_hello`: Calls the SayHello RPC from GreeterService

   - Parameter: `name` - The name to greet
2. `get_user`: Calls the GetUser RPC from GreeterService

   - Parameter: `user_id` - The ID of the user to retrieve

## Connecting to the Server

You can connect to this MCP server from any MCP-compatible client, including Claude Desktop, VS Code Copilot, or Cursor.

## Development Notes

If you make changes to the underlying proto file, you can regenerate the MCP server code with:

```bash
python generate_server.py
# or
make generate
```

Note: Without a connected gRPC server, the MCP server will return error responses. This is expected behavior when running in standalone mode.
