"""Parser module for extracting service and message definitions from Protocol Buffer schema files."""

import os
import subprocess
import tempfile
from typing import Any

# Replace the incorrect import with an alternative approach
# from google.protobuf.compiler import parser as proto_parser
from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet


class ProtoParser:
    """Parser for Protocol Buffer schema files (.proto) that extracts service and message definitions."""

    def __init__(self, proto_file: str):
        """Initialize the parser with a path to a .proto file.

        Args:
            proto_file (str): Path to the .proto file to parse
        """
        self.proto_file = proto_file
        self.file_descriptor: FileDescriptorProto | None = None
        self.services: dict[str, dict[str, Any]] = {}
        self.messages: dict[str, dict[str, Any]] = {}
        self.package = ""
        self._parse()

    def _parse(self) -> None:
        """Parse the .proto file to extract service and message definitions."""
        try:
            if not os.path.exists(self.proto_file):
                raise ValueError(f"Proto file not found: {self.proto_file}")

            # Parse the proto content using protoc command line tool
            # Create a temporary file for the descriptor set
            with tempfile.NamedTemporaryFile(suffix=".pb") as tmp:
                # Call protoc to generate a FileDescriptorSet
                protoc_cmd = [
                    "protoc",
                    f"--proto_path={os.path.dirname(self.proto_file)}",
                    f"--descriptor_set_out={tmp.name}",
                    "--include_imports",
                    self.proto_file,
                ]

                subprocess.run(protoc_cmd, check=True)

                # Read the descriptor set
                file_descriptor_set = FileDescriptorSet()
                with open(tmp.name, "rb") as f:
                    file_descriptor_set.ParseFromString(f.read())

                # Get the first file descriptor (our target .proto file)
                if not file_descriptor_set.file:
                    raise ValueError("No file descriptors found")

                self.file_descriptor = file_descriptor_set.file[0]

            if self.file_descriptor is None:
                raise ValueError("Failed to parse proto file: file descriptor is None")

            self.package = self.file_descriptor.package

            # Extract messages
            for message_type in self.file_descriptor.message_type:
                self.messages[message_type.name] = self._extract_message_fields(message_type)

            # Extract services
            for service in self.file_descriptor.service:
                methods: dict[str, dict[str, Any]] = {}
                for method in service.method:
                    methods[method.name] = {
                        "input_type": method.input_type.split(".")[-1],
                        "output_type": method.output_type.split(".")[-1],
                        "client_streaming": method.client_streaming,
                        "server_streaming": method.server_streaming,
                    }
                self.services[service.name] = methods

        except Exception as e:
            raise ValueError(f"Failed to parse proto file: {e!s}") from e

    def _extract_message_fields(self, message_type: Any) -> dict[str, dict[str, Any]]:
        """Extract field information from a message type.

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

    def _get_field_type(self, field: Any) -> str:
        """Get the type name for a field.

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

    def get_services(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Get all services defined in the proto file.

        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: A dictionary mapping service names to their methods
        """
        return self.services

    def get_messages(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Get all messages defined in the proto file.

        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: A dictionary mapping message names to their fields
        """
        return self.messages

    def get_package(self) -> str:
        """Get the package name from the proto file.

        Returns:
            str: The package name
        """
        return self.package
