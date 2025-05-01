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

    def generate_server_code(
        self, output_file: str, server_name: str | None = None, grpc_server: str | None = None
    ) -> None:
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
        code += self._generate_global_variables(server_name)
        code += self._generate_message_classes()
        code += self._generate_tool_functions()
        code += self._generate_main()

        with open(output_file, "w") as f:
            f.write(code)

    def _generate_imports(self) -> str:
        """Generate the import statements for the MCP server.

        Returns:
            str: Import statements as a string
        """
        return textwrap.dedent("""
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

        """)

    def _generate_global_variables(self, server_name: str) -> str:
        """Generate the global variables for the MCP server.

        Args:
            server_name (str): Name for the MCP server

        Returns:
            str: Global variables as a string
        """
        return textwrap.dedent(f"""
        # --- Global MCP Instance and gRPC Client ---
        # Initialize outside the class structure for easier decorator application
        mcp: FastMCP = FastMCP(
            name="{server_name}",
            instructions="MCP server for {self.package} services",
        )
        grpc_client: GRPCClient | None = None

        """)

    def _generate_message_classes(self) -> str:
        """Generate Python classes for Protobuf message types.

        Returns:
            str: Message class definitions as a string
        """
        code = "# --- Message classes ---\n"

        # Determine message dependencies
        dependencies = {}
        for message_name, fields in self.messages.items():
            deps = []
            for field_info in fields.values():
                field_type = field_info.get("type", "")
                if field_type in self.messages and field_type != message_name:
                    deps.append(field_type)
            dependencies[message_name] = deps

        # Topological sort to order messages with dependencies first
        visited = set()
        temp_visited = set()
        order = []

        def visit(name):
            if name in visited:
                return
            if name in temp_visited:
                # Handle circular dependencies
                return

            temp_visited.add(name)
            for dep in dependencies.get(name, []):
                visit(dep)

            temp_visited.remove(name)
            visited.add(name)
            order.append(name)

        for name in self.messages:
            if name not in visited:
                visit(name)

        # Generate classes in dependency order
        for message_name in order:
            fields = self.messages[message_name]
            code += f"class {message_name}:\n"
            code += f'    """Represents the {message_name} message from the Protobuf definition."""\n\n'

            # Generate __init__ method
            code += "    def __init__(self"
            for field_name, field_info in fields.items():
                code += f", {field_name}: {self._get_modern_python_type(field_info)} = None"
            code += "):\n"

            # Initialize fields
            for field_name in fields:
                code += f"        self.{field_name} = {field_name}\n"

            # Generate to_dict method
            code += "\n    def to_dict(self) -> dict[str, Any]:\n"
            code += '        """Convert message to a dictionary."""\n'
            code += "        result: dict[str, Any] = {}\n"
            for field_name, field_info in fields.items():
                field_type = field_info.get("type", "")
                is_message = field_type in self.messages
                is_repeated = field_info.get("label") == "repeated"

                code += f"        if self.{field_name} is not None:\n"
                if is_message and is_repeated:
                    code += f"            result['{field_name}'] = [item.to_dict() for item in self.{field_name}]\n"
                elif is_message:
                    code += f"            result['{field_name}'] = self.{field_name}.to_dict()\n"
                else:
                    code += f"            result['{field_name}'] = self.{field_name}\n"
            code += "        return result\n"

            # Generate from_dict static method
            code += "\n    @staticmethod\n"
            code += f"    def from_dict(data: dict[str, Any]) -> '{message_name}':\n"
            code += f'        """Create a {message_name} from a dictionary."""\n'
            code += f"        instance = {message_name}()\n"
            for field_name, field_info in fields.items():
                field_type = field_info.get("type", "")
                is_message = field_type in self.messages
                is_repeated = field_info.get("label") == "repeated"

                code += f"        if '{field_name}' in data:\n"
                if is_message and is_repeated:
                    code += f"            instance.{field_name} = []\n"
                    code += f"            for item in data['{field_name}']:\n"
                    code += f"                instance.{field_name}.append({field_type}.from_dict(item))\n"
                elif is_message:
                    code += f"            instance.{field_name} = {field_type}.from_dict(data['{field_name}'])\n"
                else:
                    code += f"            instance.{field_name} = data['{field_name}']\n"
            code += "        return instance\n"

            code += "\n\n"

        return code

    def _get_modern_python_type(self, field_info: dict[str, Any]) -> str:
        """Get the Python type annotation for a field using modern syntax.

        Args:
            field_info (dict[str, Any]): Information about the field

        Returns:
            str: Python type annotation with pipe operator for unions
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

        # Default to original type if not found, but ensure it's a string
        python_type = type_mapping.get(field_type, field_type or "Any")

        if field_info.get("label") == "repeated":
            return f"list[{python_type}] | None"

        return f"{python_type} | None"

    def _generate_tool_functions(self) -> str:
        """Generate the tool functions decorated with mcp.tool().

        Returns:
            str: Tool function definitions as a string
        """
        code = "# --- Tool Definitions ---\n"
        code += "# Decorated with the global mcp instance\n\n"

        for service_name, methods in self.services.items():
            for method_name, method_info in methods.items():
                input_type = method_info["input_type"]
                output_type = method_info["output_type"]
                python_method_name = self._camel_to_snake(method_name)

                # Skip streaming methods for now (they're more complex)
                if method_info["client_streaming"] or method_info["server_streaming"]:
                    code += f"# TODO: Implement streaming method {method_name}\n\n"
                    continue

                # Generate the function with decorator
                code += f"@mcp.tool()\n"

                # Create parameter list
                params = []
                if input_type in self.messages:
                    for field_name, field_info in self.messages[input_type].items():
                        python_type = self._get_modern_python_type(field_info)
                        params.append(f"{field_name}: {python_type} = None")

                # Generate the function signature
                code += f"def {python_method_name}({', '.join(params)}) -> dict[str, Any]:\n"

                # Generate function docstring with parameter documentation
                code += f'    """Call the {method_name} RPC from {service_name}.\n\n'
                code += "    Args:\n"
                if input_type in self.messages:
                    for field_name, field_info in self.messages[input_type].items():
                        code += f"        {field_name}: The {field_name} field for the {input_type} message\n"
                code += '    """\n'

                # Create request object
                code += f"    request = {input_type}("
                if input_type in self.messages:
                    params = [f"{field_name}={field_name}" for field_name in self.messages[input_type]]
                    code += f"{', '.join(params)}"
                code += ")\n\n"

                # Call the gRPC service if available
                code += "    if grpc_client:\n"
                code += f"        response = grpc_client.call_method('{service_name}', '{method_name}', request.to_dict())\n"
                code += f"        return cast(dict[str, Any], convert_proto_to_mcp(response, '{output_type}'))\n"
                code += "    else:\n"
                code += "        # Stub implementation when no gRPC server is available\n"
                code += f"        logger.warning('No gRPC server configured for {service_name}.{method_name}')\n"
                code += "        return {'error': 'No gRPC server configured'}\n\n\n"

        return code

    def _camel_to_snake(self, name: str) -> str:
        """Convert a camelCase or PascalCase name to snake_case.

        Args:
            name (str): The name to convert

        Returns:
            str: The name in snake_case
        """
        import re

        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    def _generate_main(self) -> str:
        """Generate the main function to run the server.

        Returns:
            str: Main function code as a string
        """
        return textwrap.dedent('''
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
        ''')
