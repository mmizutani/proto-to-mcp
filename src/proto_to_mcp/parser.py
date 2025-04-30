"""
Parser module for extracting service and message definitions from Protocol Buffer schema files.
"""
import os
from typing import Dict, Any
from google.protobuf.compiler import parser as proto_parser
from google.protobuf.descriptor_pb2 import FileDescriptorProto


class ProtoParser:
    """
    Parser for Protocol Buffer schema files (.proto) that extracts service and message definitions.
    """

    def __init__(self, proto_file: str):
        """
        Initialize the parser with a path to a .proto file.

        Args:
            proto_file (str): Path to the .proto file to parse
        """
        self.proto_file = proto_file
        self.file_descriptor = None
        self.services = {}
        self.messages = {}
        self.package = ""
        self._parse()

    def _parse(self) -> None:
        """
        Parse the .proto file to extract service and message definitions.
        """
        try:
            if not os.path.exists(self.proto_file):
                raise ValueError(f"Proto file not found: {self.proto_file}")

            # Read the proto file content
            with open(self.proto_file, 'r') as f:
                content = f.read()

            # Parse the proto content directly using the protobuf parser
            file_descriptor = FileDescriptorProto()
            proto_parser.Parse(content, file_descriptor)

            self.file_descriptor = file_descriptor
            self.package = file_descriptor.package

            # Extract messages
            for message_type in file_descriptor.message_type:
                self.messages[message_type.name] = self._extract_message_fields(message_type)

            # Extract services
            for service in file_descriptor.service:
                methods = {}
                for method in service.method:
                    methods[method.name] = {
                        "input_type": method.input_type.split(".")[-1],
                        "output_type": method.output_type.split(".")[-1],
                        "client_streaming": method.client_streaming,
                        "server_streaming": method.server_streaming,
                    }
                self.services[service.name] = methods

        except Exception as e:
            raise ValueError(f"Failed to parse proto file: {str(e)}")

    def _extract_message_fields(self, message_type) -> Dict[str, Dict[str, Any]]:
        """
        Extract field information from a message type.

        Args:
            message_type: The message type descriptor

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary mapping field names to their types and properties
        """
        fields = {}
        for field in message_type.field:
            field_info = {
                "number": field.number,
                "type": self._get_field_type(field),
                "label": "repeated" if field.label == 3 else "optional",
            }
            fields[field.name] = field_info
        return fields

    def _get_field_type(self, field) -> str:
        """
        Get the type name for a field.

        Args:
            field: The field descriptor

        Returns:
            str: The type name
        """
        # Handle primitive types
        type_map = {
            1: "double",
            2: "float",
            3: "int64",
            4: "uint64",
            5: "int32",
            6: "fixed64",
            7: "fixed32",
            8: "bool",
            9: "string",
            10: "group",
            11: "message",
            12: "bytes",
            13: "uint32",
            14: "enum",
            15: "sfixed32",
            16: "sfixed64",
            17: "sint32",
            18: "sint64",
        }

        if field.type != 11 and field.type != 14:  # Not a message or enum
            return type_map.get(field.type, "unknown")
        else:
            # For message types, return the type name
            return field.type_name.split(".")[-1]

    def get_services(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Get all services defined in the proto file.

        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: A dictionary mapping service names to their methods
        """
        return self.services

    def get_messages(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Get all messages defined in the proto file.

        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: A dictionary mapping message names to their fields
        """
        return self.messages

    def get_package(self) -> str:
        """
        Get the package name from the proto file.

        Returns:
            str: The package name
        """
        return self.package
