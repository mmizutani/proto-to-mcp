# Proto-to-MCP Documentation

This directory contains documentation for the Proto-to-MCP project.

## Contents

- [Getting Started](getting-started.md)
- [API Reference](api-reference.md)
- [Examples](examples.md)

## Overview

Proto-to-MCP is a tool that automatically generates Model Context Protocol (MCP) servers from Protocol Buffer (Protobuf) schema files. This allows AI models to interact with your gRPC services through the Model Context Protocol (MCP) without having to manually implement the MCP server.

## Key Concepts

### Protocol Buffers (Protobuf)

Protocol Buffers are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You define how you want your data to be structured once, then you can use special generated source code to easily write and read your structured data to and from a variety of data streams and using a variety of languages.

### Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a standardized protocol for AI models to interact with tools and services. It provides a structured way for models to describe their capabilities and for clients to invoke those capabilities.

### gRPC

gRPC is a modern open source remote procedure call (RPC) framework that can run anywhere. It enables client and server applications to communicate transparently, and makes it easier to build connected systems.

## Architecture

Proto-to-MCP works by:

1. Parsing a Protocol Buffer schema file (`.proto`) to extract service and message definitions
2. Generating Python code for an MCP server that:
   - Defines equivalent message types in Python
   - Creates MCP tools corresponding to the gRPC service methods
   - Connects to a running gRPC server to handle the actual requests
   - Translates between MCP and Protobuf formats

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Proto      │     │  Proto-to-  │     │  MCP        │
│  Schema     │────▶│  MCP        │────▶│  Server     │
│  (.proto)   │     │  Generator  │     │  Code       │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  AI         │     │  MCP        │     │  gRPC       │
│  Model      │◀───▶│  Server     │◀───▶│  Service    │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```
