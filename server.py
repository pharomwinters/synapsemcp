from mcp_instance import mcp

# FastMCP handles all the HTTP transport and tool invocation internally
# No need for custom FastAPI endpoints - MCP protocol handles this

if __name__ == "__main__":
    # Run the server using FastMCP's built-in transport
    # Default is STDIO, but you can specify HTTP transports
    
    # For local/development use (STDIO - default)
    # mcp.run()
    
    # For web deployment (Streamable HTTP - recommended)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
    
    # Alternative: SSE transport (deprecated but still available)
    # mcp.run(transport="sse", host="0.0.0.0", port=8000)