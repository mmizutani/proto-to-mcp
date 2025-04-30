"""
Tests for the parser module.
"""
import os
import pytest
from proto_to_mcp.parser import ProtoParser


def test_proto_parser_initialization():
    """Test that the ProtoParser can be initialized with a valid file path."""
    # This is a mock test since we don't have an actual .proto file
    # In a real test, you would use a fixture file
    with pytest.raises(ValueError):
        ProtoParser("nonexistent_file.proto")


def test_get_package():
    """Test that the get_package method returns the correct package name."""
    # This is a mock test that would normally use a fixture
    parser = MockProtoParser()
    assert parser.get_package() == "test.package"


def test_get_services():
    """Test that the get_services method returns the correct services."""
    parser = MockProtoParser()
    services = parser.get_services()
    assert "TestService" in services
    assert "GetData" in services["TestService"]


def test_get_messages():
    """Test that the get_messages method returns the correct messages."""
    parser = MockProtoParser()
    messages = parser.get_messages()
    assert "TestMessage" in messages
    assert "id" in messages["TestMessage"]
    assert messages["TestMessage"]["id"]["type"] == "int32"


# Mock class for testing without requiring protoc
class MockProtoParser(ProtoParser):
    """Mock version of ProtoParser for testing."""

    def __init__(self):
        """Initialize with mock data instead of parsing a file."""
        self.proto_file = "mock_file.proto"
        self.file_descriptor = None
        self.package = "test.package"
        self.services = {
            "TestService": {
                "GetData": {
                    "input_type": "GetDataRequest",
                    "output_type": "GetDataResponse",
                    "client_streaming": False,
                    "server_streaming": False,
                }
            }
        }
        self.messages = {
            "TestMessage": {
                "id": {
                    "number": 1,
                    "type": "int32",
                    "label": "optional",
                },
                "name": {
                    "number": 2,
                    "type": "string",
                    "label": "optional",
                }
            },
            "GetDataRequest": {
                "id": {
                    "number": 1,
                    "type": "int32",
                    "label": "optional",
                }
            },
            "GetDataResponse": {
                "data": {
                    "number": 1,
                    "type": "TestMessage",
                    "label": "optional",
                }
            }
        }

    def _parse(self):
        """Mock implementation that does nothing."""
        pass
