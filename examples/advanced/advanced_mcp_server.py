#!/usr/bin/env python3

import argparse
import logging
import os
from typing import Any, cast

from fastmcp import FastMCP

from proto_to_mcp.converter import convert_proto_to_mcp, convert_mcp_to_proto
from proto_to_mcp.grpc_client import GRPCClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- Global MCP Instance and gRPC Client ---
# Initialize outside the class structure for easier decorator application
mcp: FastMCP = FastMCP(
    name="AdvancedMCPServer",
    instructions="MCP server for advanced.example services",
)
grpc_client: GRPCClient | None = None

# --- Enum Classes ---
class BookCategory:
    """Enum representing the BookCategory from the Protobuf definition."""
    FICTION = "FICTION"
    NON_FICTION = "NON_FICTION"
    SCIENCE = "SCIENCE"
    BIOGRAPHY = "BIOGRAPHY"
    TECHNOLOGY = "TECHNOLOGY"
    OTHER = "OTHER"


class BookStatus:
    """Enum representing the BookStatus from the Protobuf definition."""
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    RESERVED = "RESERVED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"


class BookEventType:
    """Enum representing the BookEventType from the Protobuf definition."""
    BOOK_ADDED = "BOOK_ADDED"
    BOOK_UPDATED = "BOOK_UPDATED"
    BOOK_DELETED = "BOOK_DELETED"
    BOOK_BORROWED = "BOOK_BORROWED"
    BOOK_RETURNED = "BOOK_RETURNED"


# --- Message classes ---
class GetBookRequest:
    """Represents the GetBookRequest message from the Protobuf definition."""

    def __init__(self, book_id: str | None = None):
        self.book_id = book_id

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.book_id is not None:
            result['book_id'] = self.book_id
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'GetBookRequest':
        """Create a GetBookRequest from a dictionary."""
        instance = GetBookRequest()
        if 'book_id' in data:
            instance.book_id = data['book_id']
        return instance


class ListBooksRequest:
    """Represents the ListBooksRequest message from the Protobuf definition."""

    def __init__(self, author: str | None = None, category: str | None = None, publish_year: int | None = None, page_size: int | None = None, page_token: str | None = None):
        self.author = author
        self.category = category
        self.publish_year = publish_year
        self.page_size = page_size
        self.page_token = page_token

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.author is not None:
            result['author'] = self.author
        if self.category is not None:
            result['category'] = self.category
        if self.publish_year is not None:
            result['publish_year'] = self.publish_year
        if self.page_size is not None:
            result['page_size'] = self.page_size
        if self.page_token is not None:
            result['page_token'] = self.page_token
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'ListBooksRequest':
        """Create a ListBooksRequest from a dictionary."""
        instance = ListBooksRequest()
        if 'author' in data:
            instance.author = data['author']
        if 'category' in data:
            instance.category = data['category']
        if 'publish_year' in data:
            instance.publish_year = data['publish_year']
        if 'page_size' in data:
            instance.page_size = data['page_size']
        if 'page_token' in data:
            instance.page_token = data['page_token']
        return instance


class AdditionalInfoEntry:
    """Represents the AdditionalInfoEntry message from the Protobuf definition."""

    def __init__(self, key: str | None = None, value: str | None = None):
        self.key = key
        self.value = value

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.key is not None:
            result['key'] = self.key
        if self.value is not None:
            result['value'] = self.value
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'AdditionalInfoEntry':
        """Create an AdditionalInfoEntry from a dictionary."""
        instance = AdditionalInfoEntry()
        if 'key' in data:
            instance.key = data['key']
        if 'value' in data:
            instance.value = data['value']
        return instance


class BookMetadata:
    """Represents the BookMetadata message from the Protobuf definition."""

    def __init__(self, rating: float | None = None, review_count: int | None = None, tags: list[str] | None = None, summary: str | None = None, cover_image_url: str | None = None, additional_info: list[AdditionalInfoEntry] | None = None):
        self.rating = rating
        self.review_count = review_count
        self.tags = tags
        self.summary = summary
        self.cover_image_url = cover_image_url
        self.additional_info = additional_info

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.rating is not None:
            result['rating'] = self.rating
        if self.review_count is not None:
            result['review_count'] = self.review_count
        if self.tags is not None:
            result['tags'] = self.tags
        if self.summary is not None:
            result['summary'] = self.summary
        if self.cover_image_url is not None:
            result['cover_image_url'] = self.cover_image_url
        if self.additional_info is not None:
            result['additional_info'] = self.additional_info
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'BookMetadata':
        """Create a BookMetadata from a dictionary."""
        instance = BookMetadata()
        if 'rating' in data:
            instance.rating = data['rating']
        if 'review_count' in data:
            instance.review_count = data['review_count']
        if 'tags' in data:
            instance.tags = data['tags']
        if 'summary' in data:
            instance.summary = data['summary']
        if 'cover_image_url' in data:
            instance.cover_image_url = data['cover_image_url']
        if 'additional_info' in data:
            instance.additional_info = data['additional_info']
        return instance


class Book:
    """Represents the Book message from the Protobuf definition."""

    def __init__(self, id: str | None = None, title: str | None = None, authors: list[str] | None = None, isbn: str | None = None, publish_year: int | None = None, publisher: str | None = None, category: BookCategory | None = None, price: float | None = None, page_count: int | None = None, language: str | None = None, status: BookStatus | None = None, metadata: BookMetadata | None = None):
        self.id = id
        self.title = title
        self.authors = authors
        self.isbn = isbn
        self.publish_year = publish_year
        self.publisher = publisher
        self.category = category
        self.price = price
        self.page_count = page_count
        self.language = language
        self.status = status
        self.metadata = metadata

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.id is not None:
            result['id'] = self.id
        if self.title is not None:
            result['title'] = self.title
        if self.authors is not None:
            result['authors'] = self.authors
        if self.isbn is not None:
            result['isbn'] = self.isbn
        if self.publish_year is not None:
            result['publish_year'] = self.publish_year
        if self.publisher is not None:
            result['publisher'] = self.publisher
        if self.category is not None:
            result['category'] = self.category
        if self.price is not None:
            result['price'] = self.price
        if self.page_count is not None:
            result['page_count'] = self.page_count
        if self.language is not None:
            result['language'] = self.language
        if self.status is not None:
            result['status'] = self.status
        if self.metadata is not None:
            result['metadata'] = self.metadata.to_dict()
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'Book':
        """Create a Book from a dictionary."""
        instance = Book()
        if 'id' in data:
            instance.id = data['id']
        if 'title' in data:
            instance.title = data['title']
        if 'authors' in data:
            instance.authors = data['authors']
        if 'isbn' in data:
            instance.isbn = data['isbn']
        if 'publish_year' in data:
            instance.publish_year = data['publish_year']
        if 'publisher' in data:
            instance.publisher = data['publisher']
        if 'category' in data:
            instance.category = data['category']
        if 'price' in data:
            instance.price = data['price']
        if 'page_count' in data:
            instance.page_count = data['page_count']
        if 'language' in data:
            instance.language = data['language']
        if 'status' in data:
            instance.status = data['status']
        if 'metadata' in data:
            instance.metadata = BookMetadata.from_dict(data['metadata'])
        return instance


class ListBooksResponse:
    """Represents the ListBooksResponse message from the Protobuf definition."""

    def __init__(self, books: list[Book] | None = None, next_page_token: str | None = None, total_count: int | None = None):
        self.books = books
        self.next_page_token = next_page_token
        self.total_count = total_count

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.books is not None:
            result['books'] = [item.to_dict() for item in self.books]
        if self.next_page_token is not None:
            result['next_page_token'] = self.next_page_token
        if self.total_count is not None:
            result['total_count'] = self.total_count
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'ListBooksResponse':
        """Create a ListBooksResponse from a dictionary."""
        instance = ListBooksResponse()
        if 'books' in data:
            instance.books = []
            for item in data['books']:
                instance.books.append(Book.from_dict(item))
        if 'next_page_token' in data:
            instance.next_page_token = data['next_page_token']
        if 'total_count' in data:
            instance.total_count = data['total_count']
        return instance


class AddBookRequest:
    """Represents the AddBookRequest message from the Protobuf definition."""

    def __init__(self, book: Book | None = None):
        self.book = book

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.book is not None:
            result['book'] = self.book.to_dict()
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'AddBookRequest':
        """Create a AddBookRequest from a dictionary."""
        instance = AddBookRequest()
        if 'book' in data:
            instance.book = Book.from_dict(data['book'])
        return instance


class AddBookResponse:
    """Represents the AddBookResponse message from the Protobuf definition."""

    def __init__(self, book_id: str | None = None, success: bool | None = None):
        self.book_id = book_id
        self.success = success

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.book_id is not None:
            result['book_id'] = self.book_id
        if self.success is not None:
            result['success'] = self.success
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'AddBookResponse':
        """Create a AddBookResponse from a dictionary."""
        instance = AddBookResponse()
        if 'book_id' in data:
            instance.book_id = data['book_id']
        if 'success' in data:
            instance.success = data['success']
        return instance


class UpdateBookRequest:
    """Represents the UpdateBookRequest message from the Protobuf definition."""

    def __init__(self, book_id: str | None = None, book: Book | None = None, update_mask: list[str] | None = None):
        self.book_id = book_id
        self.book = book
        self.update_mask = update_mask

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.book_id is not None:
            result['book_id'] = self.book_id
        if self.book is not None:
            result['book'] = self.book.to_dict()
        if self.update_mask is not None:
            result['update_mask'] = self.update_mask
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'UpdateBookRequest':
        """Create a UpdateBookRequest from a dictionary."""
        instance = UpdateBookRequest()
        if 'book_id' in data:
            instance.book_id = data['book_id']
        if 'book' in data:
            instance.book = Book.from_dict(data['book'])
        if 'update_mask' in data:
            instance.update_mask = data['update_mask']
        return instance


class DeleteBookRequest:
    """Represents the DeleteBookRequest message from the Protobuf definition."""

    def __init__(self, book_id: str | None = None):
        self.book_id = book_id

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.book_id is not None:
            result['book_id'] = self.book_id
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'DeleteBookRequest':
        """Create a DeleteBookRequest from a dictionary."""
        instance = DeleteBookRequest()
        if 'book_id' in data:
            instance.book_id = data['book_id']
        return instance


class DeleteBookResponse:
    """Represents the DeleteBookResponse message from the Protobuf definition."""

    def __init__(self, success: bool | None = None):
        self.success = success

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.success is not None:
            result['success'] = self.success
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'DeleteBookResponse':
        """Create a DeleteBookResponse from a dictionary."""
        instance = DeleteBookResponse()
        if 'success' in data:
            instance.success = data['success']
        return instance


class BookEventsRequest:
    """Represents the BookEventsRequest message from the Protobuf definition."""

    def __init__(self, event_types: list[BookEventType] | None = None, category_filter: str | None = None):
        self.event_types = event_types
        self.category_filter = category_filter

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.event_types is not None:
            result['event_types'] = self.event_types
        if self.category_filter is not None:
            result['category_filter'] = self.category_filter
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'BookEventsRequest':
        """Create a BookEventsRequest from a dictionary."""
        instance = BookEventsRequest()
        if 'event_types' in data:
            instance.event_types = data['event_types']
        if 'category_filter' in data:
            instance.category_filter = data['category_filter']
        return instance


class BookEvent:
    """Represents the BookEvent message from the Protobuf definition."""

    def __init__(self, event_type: BookEventType | None = None, book_id: str | None = None, book: Book | None = None, timestamp: str | None = None):
        self.event_type = event_type
        self.book_id = book_id
        self.book = book
        self.timestamp = timestamp

    def to_dict(self) -> dict[str, Any]:
        """Convert message to a dictionary."""
        result: dict[str, Any] = {}
        if self.event_type is not None:
            result['event_type'] = self.event_type
        if self.book_id is not None:
            result['book_id'] = self.book_id
        if self.book is not None:
            result['book'] = self.book.to_dict()
        if self.timestamp is not None:
            result['timestamp'] = self.timestamp
        return result

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'BookEvent':
        """Create a BookEvent from a dictionary."""
        instance = BookEvent()
        if 'event_type' in data:
            instance.event_type = data['event_type']
        if 'book_id' in data:
            instance.book_id = data['book_id']
        if 'book' in data:
            instance.book = Book.from_dict(data['book'])
        if 'timestamp' in data:
            instance.timestamp = data['timestamp']
        return instance


# --- Tool Definitions ---
# Decorated with the global mcp instance

@mcp.tool()
def get_book(book_id: str | None = None) -> dict[str, Any]:
    """Call the GetBook RPC from LibraryService.

    Args:
        book_id: The book_id field for the GetBookRequest message
    """
    request = GetBookRequest(book_id=book_id)

    # Convert request to proto format
    proto_request = convert_mcp_to_proto(request.to_dict(), 'GetBookRequest')

    if grpc_client:
        # Send proto-formatted request to gRPC service
        proto_response = grpc_client.call_method('LibraryService', 'GetBook', proto_request)

        # Convert proto response to MCP format for the client
        return cast(dict[str, Any], convert_proto_to_mcp(proto_response, 'Book'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for LibraryService.GetBook')
        return {'error': 'No gRPC server configured'}


@mcp.tool()
def list_books(author: str | None = None, category: str | None = None, publish_year: int | None = None, page_size: int | None = None, page_token: str | None = None) -> dict[str, Any]:
    """Call the ListBooks RPC from LibraryService.

    Args:
        author: The author field for the ListBooksRequest message
        category: The category field for the ListBooksRequest message
        publish_year: The publish_year field for the ListBooksRequest message
        page_size: The page_size field for the ListBooksRequest message
        page_token: The page_token field for the ListBooksRequest message
    """
    request = ListBooksRequest(author=author, category=category, publish_year=publish_year, page_size=page_size, page_token=page_token)

    # Convert request to proto format
    proto_request = convert_mcp_to_proto(request.to_dict(), 'ListBooksRequest')

    if grpc_client:
        # Send proto-formatted request to gRPC service
        proto_response = grpc_client.call_method('LibraryService', 'ListBooks', proto_request)

        # Convert proto response to MCP format for the client
        return cast(dict[str, Any], convert_proto_to_mcp(proto_response, 'ListBooksResponse'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for LibraryService.ListBooks')
        return {'error': 'No gRPC server configured'}


@mcp.tool()
def add_book(book: Book | None = None) -> dict[str, Any]:
    """Call the AddBook RPC from LibraryService.

    Args:
        book: The book field for the AddBookRequest message
    """
    request = AddBookRequest(book=book)

    # Convert request to proto format
    proto_request = convert_mcp_to_proto(request.to_dict(), 'AddBookRequest')

    if grpc_client:
        # Send proto-formatted request to gRPC service
        proto_response = grpc_client.call_method('LibraryService', 'AddBook', proto_request)

        # Convert proto response to MCP format for the client
        return cast(dict[str, Any], convert_proto_to_mcp(proto_response, 'AddBookResponse'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for LibraryService.AddBook')
        return {'error': 'No gRPC server configured'}


@mcp.tool()
def update_book(book_id: str | None = None, book: Book | None = None, update_mask: list[str] | None = None) -> dict[str, Any]:
    """Call the UpdateBook RPC from LibraryService.

    Args:
        book_id: The book_id field for the UpdateBookRequest message
        book: The book field for the UpdateBookRequest message
        update_mask: The update_mask field for the UpdateBookRequest message
    """
    request = UpdateBookRequest(book_id=book_id, book=book, update_mask=update_mask)

    # Convert request to proto format
    proto_request = convert_mcp_to_proto(request.to_dict(), 'UpdateBookRequest')

    if grpc_client:
        # Send proto-formatted request to gRPC service
        proto_response = grpc_client.call_method('LibraryService', 'UpdateBook', proto_request)

        # Convert proto response to MCP format for the client
        return cast(dict[str, Any], convert_proto_to_mcp(proto_response, 'Book'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for LibraryService.UpdateBook')
        return {'error': 'No gRPC server configured'}


@mcp.tool()
def delete_book(book_id: str | None = None) -> dict[str, Any]:
    """Call the DeleteBook RPC from LibraryService.

    Args:
        book_id: The book_id field for the DeleteBookRequest message
    """
    request = DeleteBookRequest(book_id=book_id)

    # Convert request to proto format
    proto_request = convert_mcp_to_proto(request.to_dict(), 'DeleteBookRequest')

    if grpc_client:
        # Send proto-formatted request to gRPC service
        proto_response = grpc_client.call_method('LibraryService', 'DeleteBook', proto_request)

        # Convert proto response to MCP format for the client
        return cast(dict[str, Any], convert_proto_to_mcp(proto_response, 'DeleteBookResponse'))
    else:
        # Stub implementation when no gRPC server is available
        logger.warning('No gRPC server configured for LibraryService.DeleteBook')
        return {'error': 'No gRPC server configured'}


# TODO: Implement streaming method BookEvents


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
