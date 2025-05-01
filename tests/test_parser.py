"""Tests for the parser module."""

import os

import pytest

from proto_to_mcp.parser import ProtoParser


def test_proto_parser_initialization() -> None:
    """Test that the ProtoParser initializes correctly with a valid proto file."""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_service.proto")
    parser = ProtoParser(fixture_path)

    # Check that basic properties are set
    assert parser.proto_file == fixture_path
    assert parser.package == "test.fixture"
    assert parser.file_descriptor is not None


def test_proto_parser_services() -> None:
    """Test that the ProtoParser extracts service definitions correctly."""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_service.proto")
    parser = ProtoParser(fixture_path)

    services = parser.get_services()

    # Check that we found the TestService
    assert "TestService" in services

    # Check the methods in TestService
    test_service = services["TestService"]
    assert "GetData" in test_service
    assert "StreamData" in test_service

    # Check method details
    get_data = test_service["GetData"]
    assert get_data["input_type"] == "GetDataRequest"
    assert get_data["output_type"] == "GetDataResponse"
    assert not get_data["client_streaming"]
    assert not get_data["server_streaming"]

    stream_data = test_service["StreamData"]
    assert stream_data["input_type"] == "StreamDataRequest"
    assert stream_data["output_type"] == "DataItem"
    assert not stream_data["client_streaming"]
    assert stream_data["server_streaming"]


def test_proto_parser_messages() -> None:
    """Test that the ProtoParser extracts message definitions correctly."""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_service.proto")
    parser = ProtoParser(fixture_path)

    messages = parser.get_messages()

    # Check that messages are parsed
    assert "GetDataRequest" in messages
    assert "GetDataResponse" in messages
    assert "StreamDataRequest" in messages
    assert "DataItem" in messages
    assert "Metadata" in messages

    # Check field details for a message
    data_item = messages["DataItem"]
    assert "id" in data_item
    assert "name" in data_item
    assert "tags" in data_item
    assert "metadata" in data_item

    # Check types
    assert data_item["id"]["type"] == "int32"
    assert data_item["name"]["type"] == "string"
    assert data_item["tags"]["type"] == "string"
    assert data_item["tags"]["label"] == "repeated"
    assert data_item["metadata"]["type"] == "Metadata"


def test_proto_parser_error_handling() -> None:
    """Test error handling for nonexistent proto files."""
    with pytest.raises(ValueError, match="Proto file not found"):
        ProtoParser("nonexistent_file.proto")
