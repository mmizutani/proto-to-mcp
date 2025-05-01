"""Converter module for converting between Protocol Buffer and MCP data formats."""

from typing import Any, Dict, List, TypeVar, Union, cast, overload

# Define a type variable for generic data
T = TypeVar('T', bound=Union[Dict[str, Any], List[Any], str, int, float, bool, None])


@overload
def convert_proto_to_mcp(proto_data: Dict[str, Any], message_type: str | None = None) -> Dict[str, Any]: ...


@overload
def convert_proto_to_mcp(proto_data: List[Dict[str, Any]], message_type: str | None = None) -> List[Dict[str, Any]]: ...


def convert_proto_to_mcp(
    proto_data: Dict[str, Any] | List[Dict[str, Any]], message_type: str | None = None
) -> Dict[str, Any] | List[Dict[str, Any]]:
    """Convert Protocol Buffer data to MCP format.

    Args:
        proto_data (Union[Dict[str, Any], List[Dict[str, Any]]]): Data in Protobuf format
        message_type (Optional[str]): The Protobuf message type name

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: Data in MCP format
    """
    if isinstance(proto_data, list):
        return cast(List[Dict[str, Any]], [convert_proto_to_mcp(item, message_type) for item in proto_data])

    if not isinstance(proto_data, dict):
        # If it's a primitive type, just return it as is
        return cast(Dict[str, Any], proto_data)

    result: Dict[str, Any] = {}

    # Process nested objects
    for key, value in proto_data.items():
        if isinstance(value, dict):
            result[key] = convert_proto_to_mcp(value)
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                result[key] = [convert_proto_to_mcp(item) for item in value]
            else:
                result[key] = value
        else:
            result[key] = value

    return result


@overload
def convert_mcp_to_proto(mcp_data: Dict[str, Any], message_type: str | None = None) -> Dict[str, Any]: ...


@overload
def convert_mcp_to_proto(mcp_data: List[Dict[str, Any]], message_type: str | None = None) -> List[Dict[str, Any]]: ...


def convert_mcp_to_proto(
    mcp_data: Dict[str, Any] | List[Dict[str, Any]], message_type: str | None = None
) -> Dict[str, Any] | List[Dict[str, Any]]:
    """Convert MCP data to Protocol Buffer format.

    Args:
        mcp_data (Union[Dict[str, Any], List[Dict[str, Any]]]): Data in MCP format
        message_type (Optional[str]): The target Protobuf message type name

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: Data in Protobuf format
    """
    if isinstance(mcp_data, list):
        return cast(List[Dict[str, Any]], [convert_mcp_to_proto(item, message_type) for item in mcp_data])

    if not isinstance(mcp_data, dict):
        # If it's a primitive type, just return it as is
        return cast(Dict[str, Any], mcp_data)

    result: Dict[str, Any] = {}

    # Process nested objects
    for key, value in mcp_data.items():
        # Convert camelCase to snake_case for keys
        proto_key = _camel_to_snake(key)

        if isinstance(value, dict):
            result[proto_key] = convert_mcp_to_proto(value)
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                result[proto_key] = [convert_mcp_to_proto(item) for item in value]
            else:
                result[proto_key] = value
        else:
            result[proto_key] = value

    return result


def _camel_to_snake(name: str) -> str:
    """Convert a camelCase name to snake_case.

    Args:
        name (str): The name to convert

    Returns:
        str: The name in snake_case
    """
    import re

    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def _snake_to_camel(name: str) -> str:
    """Convert a snake_case name to camelCase.

    Args:
        name (str): The name to convert

    Returns:
        str: The name in camelCase
    """
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
