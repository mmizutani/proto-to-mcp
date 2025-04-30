# Getting Started with Proto-to-MCP

This guide will help you get started with Proto-to-MCP to generate MCP servers from your Protocol Buffer definitions.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- Python 3.9 or higher
- Protocol Buffers compiler (`protoc`)
- pip (Python package manager)

## Installation

### Install with pip

```bash
pip install proto-to-mcp
```

### Install from source

```bash
git clone https://github.com/mmizutani/proto-to-mcp.git
cd proto-to-mcp
pip install -e .
```

## Basic Usage

### Command-line Interface

The simplest way to use Proto-to-MCP is through its command-line interface:

```bash
# Generate an MCP server from a .proto file
proto-to-mcp path/to/service.proto

# Specify an output file
proto-to-mcp path/to/service.proto --output my_mcp_server.py

# Connect to a running gRPC server
proto-to-mcp path/to/service.proto --grpc-server localhost:50051

# Customize the server name
proto-to-mcp path/to/service.proto --name CustomMCPServer
```

### Programmatic Usage

You can also use Proto-to-MCP programmatically in your Python code:

```python
from proto_to_mcp.parser import ProtoParser
from proto_to_mcp.generator import MCPServerGenerator

# Parse the Protobuf schema
parser = ProtoParser("path/to/service.proto")

# Generate the MCP server
generator = MCPServerGenerator(parser)
generator.generate_server_code(
    output_file="my_mcp_server.py",
    server_name="MyServiceMCP",
    grpc_server="localhost:50051"
)
```

## Running the Generated MCP Server

Once you've generated your MCP server, you can run it directly:

```bash
python my_mcp_server.py --host localhost --port 8000
```

This will start an MCP server that:

1. Listens for MCP requests on http://localhost:8000
2. Routes those requests to your gRPC service (if specified)
3. Converts between MCP and gRPC formats

## Next Steps

- Check out the [examples](examples.md) for more usage patterns
- Read the [API reference](api-reference.md) for detailed documentation
- Learn about [advanced features](advanced-usage.md) for more complex use cases

## Troubleshooting

### Common Issues

**Issue**: "protoc compiler not found"
**Solution**: Make sure Protocol Buffers compiler is installed and in your PATH

**Issue**: "Failed to parse proto file"
**Solution**: Ensure your .proto file is valid by running `protoc --validate_out=. your_file.proto`

**Issue**: MCP server generates but can't connect to gRPC service
**Solution**: Make sure your gRPC service is running at the specified address
