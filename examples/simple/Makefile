.PHONY: all clean install generate run

UV ?= uv

all: install generate

clean:
	rm -rf build dist *.egg-info

install:
	$(UV) sync

generate:
	$(UV) run python generate_server.py

run:
	$(UV) run fastmcp run simple_mcp_server.py:mcp

run-with-stdio:
	$(UV) run fastmcp run simple_mcp_server.py:mcp --transport stdio

run-with-sse:
	$(UV) run fastmcp run simple_mcp_server.py:mcp --transport sse

run-with-grpc:
	$(UV) run fastmcp run simple_mcp_server.py:mcp --grpc-server $(GRPC_SERVER)

run-with-port:
	$(UV) run fastmcp run simple_mcp_server.py:mcp --port $(PORT)
