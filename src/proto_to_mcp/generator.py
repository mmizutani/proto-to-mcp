"""Generator module for creating MCP server code from parsed Protocol Buffer definitions."""
import os
import textwrap
from typing import Any

from .parser import ProtoParser


class MCPServerGenerator:
    """Generator for MCP server code from Protocol Buffer service definitions."""

    def __init__(self, parser: ProtoParser):
        """Initialize the generator with a ProtoParser instance.

        Args:
            parser (ProtoParser): The parser with extracted proto definitions
        """
        self.parser = parser
        self.services = parser.get_services()
        self.messages = parser.get_messages()
        self.package = parser.get_package()

    def generate_server_code(self, output_file: str, server_name: str | None = None, grpc_server: str | None = None) -> None:
        """Generate an MCP server implementation and write it to the specified output file.

        Args:
            output_file (str): Path to write the generated server code
            server_name (Optional[str]): Name for the MCP server (defaults to proto filename)
            grpc_server (Optional[str]): Address of the gRPC server to connect to
        """
        if server_name is None:
            proto_file_basename = os.path.basename(self.parser.proto_file)
            server_name = os.path.splitext(proto_file_basename)[0].title().replace("_", "") + "MCPServer"

        code = self._generate_imports()
        code += self._generate_message_classes()
        code += self._generate_server_class(server_name, grpc_server)
        code += self._generate_main(server_name)

        with open(output_file, "w") as f:
            f.write(code)

    def _generate_imports(self) -> str:
        """Generate the import statements for the MCP server.

        Returns:
            str: Import statements as a string
        """
        return textwrap.dedent("""
        #!/usr/bin/env python3

        import os
        import json
        import argparse
        import logging
        from typing import Dict, List, Optional, Any, Union

        from fastmcp import FastMCP, Parameter, Tool, MCPResponse
        from proto_to_mcp.converter import convert_proto_to_mcp, convert_mcp_to_proto
        from proto_to_mcp.grpc_client import GRPCClient


        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        """)

    def _generate_message_classes(self) -> str:
        """Generate Python classes for Protobuf message types.

        Returns:
            str: Message class definitions as a string
        """
        code = "# Message classes\n"

        for message_name, fields in self.messages.items():
            code += f"class {message_name}:\n"
            code += f"    \"\"\"Represents the {message_name} message from the Protobuf definition.\"\"\"\n\n"

            # Generate __init__ method
            code += "    def __init__(self"
            for field_name, field_info in fields.items():
                code += f", {field_name}: Optional[{self._get_python_type(field_info)}] = None"
            code += "):\n"

            # Initialize fields
            for field_name in fields:
                code += f"        self.{field_name} = {field_name}\n"

            # Generate to_dict method
            code += "\n    def to_dict(self) -> Dict[str, Any]:\n"
            code += "        \"\"\"Convert message to a dictionary.\"\"\"\n"
            code += "        result = {}\n"
            for field_name, field_info in fields.items():
                if "message" in field_info.get("type", "").lower():
                    code += f"        if self.{field_name} is not None:\n"
                    code += f"            result['{field_name}'] = self.{field_name}.to_dict()\n"
                elif field_info.get("label") == "repeated":
                    code += f"        if self.{field_name} is not None:\n"
                    if "message" in field_info.get("type", "").lower():
                        code += f"            result['{field_name}'] = [item.to_dict() for item in self.{field_name}]\n"
                    else:
                        code += f"            result['{field_name}'] = self.{field_name}\n"
                else:
                    code += f"        if self.{field_name} is not None:\n"
                    code += f"            result['{field_name}'] = self.{field_name}\n"
            code += "        return result\n"

            # Generate from_dict static method
            code += "\n    @staticmethod\n"
            code += f"    def from_dict(data: Dict[str, Any]) -> '{message_name}':\n"
            code += f"        \"\"\"Create a {message_name} from a dictionary.\"\"\"\n"
            code += f"        instance = {message_name}()\n"
            for field_name, field_info in fields.items():
                code += f"        if '{field_name}' in data:\n"
                if "message" in field_info.get("type", "").lower():
                    message_type = field_info.get("type")
                    if field_info.get("label") == "repeated":
                        code += f"            instance.{field_name} = []\n"
                        code += f"            for item in data['{field_name}']:\n"
                        code += f"                instance.{field_name}.append({message_type}.from_dict(item))\n"
                    else:
                        code += f"            instance.{field_name} = {message_type}.from_dict(data['{field_name}'])\n"
                else:
                    code += f"            instance.{field_name} = data['{field_name}']\n"
            code += "        return instance\n"

            code += "\n\n"

        return code

    def _get_python_type(self, field_info: dict[str, Any]) -> str:
        """Get the Python type annotation for a field.

        Args:
            field_info (Dict[str, Any]): Information about the field

        Returns:
            str: Python type annotation
        """
        field_type = field_info.get("type", "")

        # Map protobuf types to Python types
        type_mapping = {
            "double": "float",
            "float": "float",
            "int32": "int",
            "int64": "int",
            "uint32": "int",
            "uint64": "int",
            "sint32": "int",
            "sint64": "int",
            "fixed32": "int",
            "fixed64": "int",
            "sfixed32": "int",
            "sfixed64": "int",
            "bool": "bool",
            "string": "str",
            "bytes": "bytes",
        }

        python_type = type_mapping.get(field_type, field_type)

        if field_info.get("label") == "repeated":
            return f"List[{python_type}]"

        return python_type

    def _generate_server_class(self, server_name: str, grpc_server: str | None) -> str:
        """Generate the MCP server class.

        Args:
            server_name (str): Name for the MCP server class
            grpc_server (Optional[str]): Address of the gRPC server to connect to

        Returns:
            str: Server class definition as a string
        """
        code = f"class {server_name}(FastMCP):\n"
        code += f'    """MCP server for {self.package} services."""\n\n'

        # Initialize with gRPC client if specified
        code += "    def __init__(self, grpc_server: Optional[str] = None):\n"
        code += '        """Initialize the MCP server."""\n'
        code += f'        super().__init__(title="{server_name}", description="MCP server for {self.package} services")\n'

        if grpc_server:
            code += f'        self.grpc_client = GRPCClient("{grpc_server}")\n'
        else:
            code += '        self.grpc_client = GRPCClient(os.getenv("GRPC_SERVER")) if os.getenv("GRPC_SERVER") else None\n'

        code += "\n"

        # Generate tool methods for each RPC
        for service_name, methods in self.services.items():
            for method_name, method_info in methods.items():
                input_type = method_info["input_type"]
                output_type = method_info["output_type"]
                python_method_name = self._camel_to_snake(method_name)

                # Skip streaming methods for now (they're more complex)
                if method_info["client_streaming"] or method_info["server_streaming"]:
                    code += f"    # TODO: Implement streaming method {method_name}\n\n"
                    continue

                # Generate the tool method
                code += f"    @Tool(name='{python_method_name}', description='Call the {method_name} RPC from {service_name}')\n"

                # Generate parameters based on input message fields
                if input_type in self.messages:
                    for field_name, field_info in self.messages[input_type].items():
                        python_type = self._get_python_type(field_info)
                        description = f"The {field_name} field for the {input_type} message"
                        code += f"    @Parameter('{field_name}', description='{description}')\n"

                # Generate the method
                code += f"    def {python_method_name}(self, **kwargs) -> MCPResponse:\n"
                code += f'        """Call the {method_name} RPC method."""\n'
                code += f"        request = {input_type}()\n"

                # Set request fields
                if input_type in self.messages:
                    for field_name in self.messages[input_type]:
                        code += f"        if '{field_name}' in kwargs:\n"
                        code += f"            request.{field_name} = kwargs['{field_name}']\n"

                # If we have a gRPC client, use it
                code += "\n        if self.grpc_client:\n"
                code += f"            response = self.grpc_client.call_method('{service_name}', '{method_name}', request.to_dict())\n"
                code += f"            return MCPResponse(convert_proto_to_mcp(response, '{output_type}'))\n"
                code += "        else:\n"
                code += "            # Stub implementation when no gRPC server is available\n"
                code += f"            logger.warning('No gRPC server configured for {service_name}.{method_name}')\n"
                code += "            return MCPResponse({'error': 'No gRPC server configured'})\n\n"

        return code

    def _camel_to_snake(self, name: str) -> str:
        """Convert a camelCase or PascalCase name to snake_case.

        Args:
            name (str): The name to convert

        Returns:
            str: The name in snake_case
        """
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def _generate_main(self, server_name: str) -> str:
        """Generate the main function to run the server.

        Args:
            server_name (str): Name of the server class

        Returns:
            str: Main function code as a string
        """
        return textwrap.dedent(f"""
        def main():
            \"""Run the MCP server.\"""
            parser = argparse.ArgumentParser(description='Run the {server_name}')
            parser.add_argument('--grpc-server', '-g', help='Address of the gRPC server to connect to')
            parser.add_argument('--host', default='localhost', help='Host to bind the server to')
            parser.add_argument('--port', '-p', type=int, default=8000, help='Port to bind the server to')
            args = parser.parse_args()

            server = {server_name}(grpc_server=args.grpc_server)
            server.run(host=args.host, port=args.port)


        if __name__ == '__main__':
            main()
        """)
