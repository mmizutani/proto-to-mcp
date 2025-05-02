# proto-to-mcp

[![Build Status](https://img.shields.io/github/workflow/status/username/proto-to-mcp/CI)](https://github.com/username/proto-to-mcp/actions)
[![PyPI version](https://img.shields.io/pypi/v/proto-to-mcp.svg)](https://pypi.org/project/proto-to-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/proto-to-mcp.svg)](https://pypi.org/project/proto-to-mcp/)

A tool for automatically converting Protocol Buffer (Protobuf) schema files (.proto) into Model Context Protocol (MCP) server implementations in Python.

## Overview

proto-to-mcp bridges the gap between existing Protobuf/gRPC services and the Model Context Protocol ecosystem, allowing LLMs to interact with structured data and services defined in .proto files. By automatically generating MCP server code from Protobuf definitions, it eliminates the need for manual integration and ensures consistency between your service definitions and MCP interfaces.

The Model Context Protocol (MCP) provides a standardized way for AI models to interact with external data sources and tools. This project allows you to expose existing Protobuf-based services as MCP servers that can be used by LLM applications like Claude Desktop, VS Code Copilot, Cursor, and other MCP-compatible clients.

## Features

- **Automatic Code Generation**: Convert .proto files directly to Python MCP server implementations
- **Type Conversion**: Intelligent mapping between Protobuf and MCP data types
- **gRPC Integration**: Seamless connection to backend gRPC services
- **Customizable**: Configure how Protobuf services map to MCP capabilities
- **CLI Support**: Easy-to-use command-line interface
- **Comprehensive Documentation**: Detailed guides for various use cases

## Installation

### Prerequisites

- Python 3.9 or newer
- A working installation of Protocol Buffers (protoc compiler)

### Install via pip

```bash
pip install proto-to-mcp
```

### Install via uv (recommended)

```bash
# Install uv if you don't have it
pip install uv

# Install proto-to-mcp with uv
uv pip install proto-to-mcp
```

### Install from source

```bash
git clone https://github.com/username/proto-to-mcp.git
cd proto-to-mcp
pip install -e .
```

### Install from source using uv

```bash
git clone https://github.com/mmizutani/proto-to-mcp.git
cd proto-to-mcp
uv pip install -e .
```

## Usage

### Basic Usage

Convert a Protobuf schema file to an MCP server:

```bash
proto-to-mcp path/to/service.proto -o mcp_server.py
```

Run the generated MCP server:

```bash
python mcp_server.py
```

Connect to the MCP server in Claude Desktop, VS Code, or any other MCP-compatible client.

### Advanced Options

```bash
proto-to-mcp --help
```

```
usage: proto-to-mcp [-h] [--output OUTPUT] [--name NAME] [--grpc-server GRPC_SERVER] proto_file

Convert Protobuf schema files to MCP server implementations

positional arguments:
  proto_file            Path to the .proto file

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output path for the generated MCP server file
  --name NAME, -n NAME  Name for the MCP server (defaults to the proto filename)
  --grpc-server GRPC_SERVER, -g GRPC_SERVER
                        Address of the gRPC server to connect to
```

### Programmatic Usage

```python
from proto_to_mcp import ProtoParser, MCPServerGenerator

# Parse the proto file
parser = ProtoParser("path/to/service.proto")

# Generate MCP server code
generator = MCPServerGenerator(parser)
generator.generate_server_code("output_server.py", "MyService")
```

## Examples

### Simple Example: User Service

Given a `user_service.proto` file:

```protobuf
syntax = "proto3";

package users;

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
}

message GetUserRequest {
  int32 id = 1;
}

message GetUserResponse {
  User user = 1;
}

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}
```

Generate an MCP server:

```bash
proto-to-mcp user_service.proto -o user_mcp_server.py
```

The generated MCP server will expose a `get_user` tool that can be called by LLM applications to retrieve user information.

### Integration with Existing gRPC Services

To connect the generated MCP server to an existing gRPC service:

```bash
proto-to-mcp user_service.proto -g localhost:50051 -o user_mcp_server.py
```

This will configure the server to forward requests to the gRPC service running on `localhost:50051`.

## Architecture

proto-to-mcp consists of several core components:

1. **ProtoParser**: Parses .proto files to extract message and service definitions
2. **MCPServerGenerator**: Generates Python code for the MCP server based on the parsed definitions
3. **Conversion Utilities**: Handles data conversion between Protobuf and MCP formats
4. **gRPC Client**: Manages connections to backend gRPC services
5. **CLI**: Provides command-line interface for easy usage

The generated MCP server uses the FastMCP framework, which provides a high-level, Pythonic interface for building MCP servers.

## Project Structure

```
/
├── .github/
│   └── workflows/
│       └── ci.yml                      # Continuous integration workflow
├── src/
│   └── proto_to_mcp/
│       ├── __init__.py                 # Package initialization
│       ├── parser.py                   # Protobuf schema parser
│       ├── generator.py                # MCP server code generator
│       ├── converter.py                # Type conversion utilities
│       ├── grpc_client.py              # gRPC client implementation
│       └── cli.py                      # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_parser.py                  # Tests for parser module
│   ├── test_generator.py               # Tests for generator module
│   ├── test_converter.py               # Tests for converter module
│   └── fixtures/
│       └── example.proto               # Test Protobuf files
├── examples/
│   ├── simple/
│   │   ├── user_service.proto          # Basic user service example
│   │   └── README.md                   # Example documentation
│   └── advanced/
│       ├── blog_service.proto          # More complex example
│       └── README.md                   # Advanced example documentation
├── docs/
│   ├── index.md                        # Documentation homepage
│   ├── usage.md                        # Usage documentation
│   ├── api.md                          # API reference
│   └── contributing.md                 # Contribution guidelines
├── pyproject.toml                      # Project metadata and dependencies
├── setup.py                            # Package setup script
├── LICENSE                             # MIT License
└── README.md                           # This file
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mmizutani/proto-to-mcp.git
cd proto-to-mcp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies using pip
pip install -e ".[dev]"

# Or using uv (recommended for faster installation)
pip install uv
uv pip install -e ".[dev]"
```

### Formatting and Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for code formatting and linting. Ruff replaces multiple tools (Black, isort, flake8) with a single, fast Rust-based solution.

To format your code:

```bash
ruff format src tests
```

To lint your code:

```bash
ruff check src tests
```

To automatically fix linting issues where possible:

```bash
ruff check --fix src tests
```

You can also install pre-commit hooks to automatically format and lint your code before each commit:

```bash
pip install pre-commit
pre-commit install
```

### Using the Makefile

The project includes a Makefile with several useful commands to streamline development:

```bash
# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run type checking
make typecheck

# Run linting, type checking, and tests
make all

# Fix linting issues and format code
make fix

# Clean build artifacts and cache
make clean

# Install development dependencies using pip
make install-dev

# Install development dependencies using uv
make install-uv-dev
```

### Testing

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure your code passes all tests and follows the project's coding style.

## Roadmap

- [ ] Replace custom Protobuf parser with [proto-schema-parser](https://github.com/criccomini/proto-schema-parser), where the lexer and parser are autogenerated from Buf's ANTLR lexer and parser grammar files.
- [ ] MCP client generation from Protobuf definitions (Python and Go)
- [ ] Integration with popular frameworks like FastAPI
- [ ] Support Protobuf validation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) - The standard for AI model context integration
- [Protocol Buffers](https://protobuf.dev) - Google's language-neutral, platform-neutral extensible mechanism for serializing structured data
- [FastMCP](https://github.com/jlowin/fastmcp) - The fast, Pythonic way to build MCP servers
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk) - The official Python SDK for Model Context Protocol
