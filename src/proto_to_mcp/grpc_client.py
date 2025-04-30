"""gRPC client module for connecting to gRPC services."""
import importlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


class GRPCClient:
    """Client for connecting to and calling methods on gRPC services."""

    def __init__(self, server_address: str | None = None):
        """Initialize the gRPC client.

        Args:
            server_address (Optional[str]): The address of the gRPC server, e.g., 'localhost:50051'
        """
        self.server_address = server_address
        self.stubs = {}

    def call_method(self, service_name: str, method_name: str, request_data: dict[str, Any]) -> dict[str, Any]:
        """Call a method on a gRPC service.

        Args:
            service_name (str): Name of the service
            method_name (str): Name of the method to call
            request_data (Dict[str, Any]): Request data as a dictionary

        Returns:
            Dict[str, Any]: Response data as a dictionary
        """
        if not self.server_address:
            logger.warning("No gRPC server address provided")
            return {"error": "No gRPC server address provided"}

        try:
            # Get or create the stub for this service
            stub = self._get_stub(service_name)
            if not stub:
                return {"error": f"Failed to create stub for {service_name}"}

            # Get the method from the stub
            method = getattr(stub, method_name, None)
            if not method:
                return {"error": f"Method {method_name} not found on {service_name}"}

            # Create the request object
            request_class = self._get_request_class(service_name, method_name)
            if not request_class:
                return {"error": f"Request class for {method_name} not found"}

            # Create the request object and populate it
            try:
                request = request_class(**request_data)
            except Exception as e:
                logger.error(f"Error creating request object: {e}")
                return {"error": f"Error creating request: {e!s}"}

            # Make the gRPC call
            response = method(request)

            # Convert the response to a dictionary
            return self._message_to_dict(response)

        except Exception as e:
            logger.error(f"Error calling gRPC method {service_name}.{method_name}: {e}")
            return {"error": f"Error calling gRPC method: {e!s}"}

    def _get_stub(self, service_name: str):
        """Get or create a stub for a service.

        Args:
            service_name (str): Name of the service

        Returns:
            Optional[Any]: The stub for the service, or None if it couldn't be created
        """
        if service_name in self.stubs:
            return self.stubs[service_name]

        try:
            # Try to import the generated gRPC module
            # This assumes the module follows standard gRPC Python naming conventions
            pb2_module_name = f"{self._to_snake_case(service_name)}_pb2"
            pb2_grpc_module_name = f"{self._to_snake_case(service_name)}_pb2_grpc"

            try:
                importlib.import_module(pb2_module_name)
                pb2_grpc = importlib.import_module(pb2_grpc_module_name)
            except ImportError:
                logger.error(f"Could not import {pb2_module_name} or {pb2_grpc_module_name}")
                return None

            # Create a secure channel to the server
            import grpc
            channel = grpc.insecure_channel(self.server_address)

            # Create the stub
            stub_class_name = f"{service_name}Stub"
            stub_class = getattr(pb2_grpc, stub_class_name, None)
            if not stub_class:
                logger.error(f"Stub class {stub_class_name} not found in {pb2_grpc_module_name}")
                return None

            stub = stub_class(channel)
            self.stubs[service_name] = stub
            return stub

        except Exception as e:
            logger.error(f"Error creating stub for {service_name}: {e}")
            return None

    def _get_request_class(self, service_name: str, method_name: str):
        """Get the request class for a method.

        Args:
            service_name (str): Name of the service
            method_name (str): Name of the method

        Returns:
            Optional[Any]: The request class, or None if it couldn't be found
        """
        try:
            # Convert method name from CamelCase to snake_case if needed
            method_snake = self._to_snake_case(method_name)

            # Try to import the generated gRPC module
            pb2_module_name = f"{self._to_snake_case(service_name)}_pb2"

            try:
                pb2 = importlib.import_module(pb2_module_name)
            except ImportError:
                logger.error(f"Could not import {pb2_module_name}")
                return None

            # Look for common request naming patterns
            request_class_names = [
                f"{method_name}Request",
                f"{service_name}{method_name}Request",
                f"{method_snake.title().replace('_', '')}Request",
            ]

            for class_name in request_class_names:
                request_class = getattr(pb2, class_name, None)
                if request_class:
                    return request_class

            logger.error(f"Could not find request class for {method_name} in {pb2_module_name}")
            return None

        except Exception as e:
            logger.error(f"Error getting request class for {method_name}: {e}")
            return None

    def _message_to_dict(self, message) -> dict[str, Any]:
        """Convert a gRPC message to a dictionary.

        Args:
            message: The gRPC message object

        Returns:
            Dict[str, Any]: The message as a dictionary
        """
        try:
            # Use the MessageToDict utility from google.protobuf.json_format if available
            from google.protobuf.json_format import MessageToDict
            return MessageToDict(message, preserving_proto_field_name=True)
        except ImportError:
            # Fallback to a manual conversion if the import fails
            result = {}
            for field in message.DESCRIPTOR.fields:
                value = getattr(message, field.name)
                if hasattr(value, 'DESCRIPTOR'):
                    result[field.name] = self._message_to_dict(value)
                elif isinstance(value, list | tuple):
                    result[field.name] = [
                        self._message_to_dict(item) if hasattr(item, 'DESCRIPTOR') else item
                        for item in value
                    ]
                else:
                    result[field.name] = value
            return result

    def _to_snake_case(self, name: str) -> str:
        """Convert a CamelCase name to snake_case.

        Args:
            name (str): The name to convert

        Returns:
            str: The name in snake_case
        """
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
