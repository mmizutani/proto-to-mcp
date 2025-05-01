"""Tests for the generator module."""

import os
import tempfile
from typing import Any, Dict

from proto_to_mcp.generator import MCPServerGenerator
from proto_to_mcp.parser import ProtoParser


def get_test_parser() -> ProtoParser:
    """Helper function to get a parser for testing."""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_service.proto")
    return ProtoParser(fixture_path)


def test_server_generator_initialization() -> None:
    """Test that the MCPServerGenerator can be initialized with a parser."""
    parser = get_test_parser()
    generator = MCPServerGenerator(parser)
    assert generator.services == parser.get_services()
    assert generator.messages == parser.get_messages()
    assert generator.package == parser.get_package()


def test_generate_server_code() -> None:
    """Test that the generate_server_code method creates a file with the expected content."""
    parser = get_test_parser()
    generator = MCPServerGenerator(parser)

    # Create a temporary file for the output
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        temp_filename = temp_file.name

    try:
        # Generate the server code
        generator.generate_server_code(temp_filename, "TestMCPServer")

        # Check that the file exists and contains expected content
        assert os.path.exists(temp_filename)

        with open(temp_filename) as f:
            content = f.read()

            # Check for key elements
            assert "class TestMCPServer(FastMCP):" in content
            assert "class DataItem:" in content
            assert "class GetDataRequest:" in content
            assert "class GetDataResponse:" in content
            assert "@Tool" in content
            assert "def get_data(self" in content

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_camel_to_snake() -> None:
    """Test the _camel_to_snake method."""
    parser = get_test_parser()
    generator = MCPServerGenerator(parser)

    assert generator._camel_to_snake("GetUserData") == "get_user_data"
    assert generator._camel_to_snake("getUserData") == "get_user_data"
    assert generator._camel_to_snake("userData") == "user_data"
