# backup example

import os
from fastmcp import FastMCP

mcp = FastMCP(
    name="MyMcpServer",
    stateless_http=True  # Required for streamable-http transport
)

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Get host and port from environment variables with defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    mcp.run(transport="streamable-http",
            host=host,
            port=port)