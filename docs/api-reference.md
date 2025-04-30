# API Reference

This document provides detailed API reference for the Proto-to-MCP library.

## ProtoParser

The `ProtoParser` class is responsible for parsing Protocol Buffer schema files and extracting service and message definitions.

```python
from proto_to_mcp.parser import ProtoParser
```

### Constructor

```python
parser = ProtoParser(proto_file)
```

**Parameters:**
- `proto_file` (str): Path to the .proto file to parse

**Raises:**
- `ValueError`: If the .proto file does not exist or cannot be parsed

### Methods

#### get_services()

Returns all services defined in the proto file.

```python
services = parser.get_services()
```

**Returns:**
- `Dict[str, Dict[str, Dict[str, Any]]]`: A dictionary mapping service names to their methods

#### get_messages()

Returns all messages defined in the proto file.

```python
messages = parser.get_messages()
```

**Returns:**
- `Dict[str, Dict[str, Dict[str, Any]]]`: A dictionary mapping message names to their fields

#### get_package()

Returns the package name from the proto file.

```python
package = parser.get_package()
```

**Returns:**
- `str`: The package name

## MCPServerGenerator

The `MCPServerGenerator` class is responsible for generating MCP server code from parsed Protocol Buffer definitions.

```python
from proto_to_mcp.generator import MCPServerGenerator
```

### Constructor

```python
generator = MCPServerGenerator(parser)
```

**Parameters:**
- `parser` (ProtoParser): A ProtoParser instance with parsed proto definitions

### Methods

#### generate_server_code()

Generate an MCP server implementation and write it to the specified output file.

```python
generator.generate_server_code(
    output_file="my_server.py",
    server_name="MyMCPServer",
    grpc_server="localhost:50051"
)
```

**Parameters:**
- `output_file` (str): Path to write the generated server code
- `server_name` (Optional[str]): Name for the MCP server (defaults to proto filename)
- `grpc_server` (Optional[str]): Address of the gRPC server to connect to

## Converter Functions

The converter module provides functions for converting between Protocol Buffer and MCP data formats.

```python
from proto_to_mcp.converter import convert_proto_to_mcp, convert_mcp_to_proto
```

### convert_proto_to_mcp()

Convert Protocol Buffer data to MCP format.

```python
mcp_data = convert_proto_to_mcp(proto_data, message_type)
```

**Parameters:**
- `proto_data` (Union[Dict[str, Any], List[Dict[str, Any]]]): Data in Protobuf format
- `message_type` (Optional[str]): The Protobuf message type name

**Returns:**
- Data in MCP format

### convert_mcp_to_proto()

Convert MCP data to Protocol Buffer format.

```python
proto_data = convert_mcp_to_proto(mcp_data, message_type)
```

**Parameters:**
- `mcp_data` (Union[Dict[str, Any], List[Dict[str, Any]]]): Data in MCP format
- `message_type` (Optional[str]): The target Protobuf message type name

**Returns:**
- Data in Protobuf format

## GRPCClient

The `GRPCClient` class is responsible for connecting to and calling methods on gRPC services.

```python
from proto_to_mcp.grpc_client import GRPCClient
```

### Constructor

```python
client = GRPCClient(server_address)
```

**Parameters:**
- `server_address` (Optional[str]): The address of the gRPC server, e.g., 'localhost:50051'

### Methods

#### call_method()

Call a method on a gRPC service.

```python
response = client.call_method(
    service_name="MyService",
    method_name="MyMethod",
    request_data={"key": "value"}
)
```

**Parameters:**
- `service_name` (str): Name of the service
- `method_name` (str): Name of the method to call
- `request_data` (Dict[str, Any]): Request data as a dictionary

**Returns:**
- `Dict[str, Any]`: Response data as a dictionary

## Command-line Interface

The CLI module provides a command-line interface for the library.

```
Usage: proto-to-mcp [OPTIONS] PROTO_FILE

Options:
  --output, -o TEXT     Output path for the generated MCP server file
  --name, -n TEXT       Name for the MCP server (defaults to the proto filename)
  --grpc-server, -g TEXT  Address of the gRPC server to connect to
  --verbose, -v         Enable verbose logging
  --help                Show help message and exit
```
