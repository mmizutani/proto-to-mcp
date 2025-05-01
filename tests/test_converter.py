"""Tests for the converter module."""

from proto_to_mcp.converter import convert_mcp_to_proto, convert_proto_to_mcp


def test_convert_proto_to_mcp_primitives():
    """Test conversion of primitive types from Protobuf to MCP format."""
    proto_data = {"id": 123, "name": "test", "active": True, "score": 98.6}

    mcp_data = convert_proto_to_mcp(proto_data)

    assert mcp_data == proto_data  # Primitive types should be unchanged


def test_convert_proto_to_mcp_nested():
    """Test conversion of nested objects from Protobuf to MCP format."""
    proto_data = {
        "user": {"id": 123, "name": "test_user"},
        "posts": [{"id": 1, "title": "Post 1"}, {"id": 2, "title": "Post 2"}],
    }

    mcp_data = convert_proto_to_mcp(proto_data)

    assert mcp_data["user"]["id"] == 123
    assert mcp_data["user"]["name"] == "test_user"
    assert len(mcp_data["posts"]) == 2
    assert mcp_data["posts"][0]["id"] == 1
    assert mcp_data["posts"][1]["title"] == "Post 2"


def test_convert_mcp_to_proto_primitives():
    """Test conversion of primitive types from MCP to Protobuf format."""
    mcp_data = {"id": 123, "name": "test", "isActive": True, "score": 98.6}

    proto_data = convert_mcp_to_proto(mcp_data)

    # Check camelCase to snake_case conversion
    assert "is_active" in proto_data
    assert proto_data["is_active"]
    assert proto_data["id"] == 123
    assert proto_data["name"] == "test"
    assert proto_data["score"] == 98.6


def test_convert_mcp_to_proto_nested():
    """Test conversion of nested objects from MCP to Protobuf format."""
    mcp_data = {
        "userData": {"userId": 123, "displayName": "test_user"},
        "userPosts": [{"postId": 1, "postTitle": "Post 1"}, {"postId": 2, "postTitle": "Post 2"}],
    }

    proto_data = convert_mcp_to_proto(mcp_data)

    # Check nested object conversions
    assert "user_data" in proto_data
    assert "user_posts" in proto_data

    assert proto_data["user_data"]["user_id"] == 123
    assert proto_data["user_data"]["display_name"] == "test_user"

    assert len(proto_data["user_posts"]) == 2
    assert proto_data["user_posts"][0]["post_id"] == 1
    assert proto_data["user_posts"][1]["post_title"] == "Post 2"


def test_camel_snake_conversion_functions():
    """Test the camel/snake case conversion utility functions."""
    from proto_to_mcp.converter import _camel_to_snake, _snake_to_camel

    # Test camelCase to snake_case
    assert _camel_to_snake("userName") == "user_name"
    assert _camel_to_snake("UserName") == "user_name"
    assert _camel_to_snake("userId123") == "user_id123"

    # Test snake_case to camelCase
    assert _snake_to_camel("user_name") == "userName"
    assert _snake_to_camel("user_id_123") == "userId123"
    assert _snake_to_camel("simple") == "simple"
