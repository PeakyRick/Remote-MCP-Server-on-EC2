from fastmcp import FastMCP
import datetime
import pytz
import os

mcp = FastMCP(
    name="Current Date and Time",
    instructions="When you are asked for the current date or time, call current_datetime() and pass along an optional timezone parameter (defaults to NYC).",
    stateless_http=True
)

# Code partially from https://www.haihai.ai/fastmcp/
@mcp.tool()
def current_datetime(timezone: str = "America/New_York") -> str:
    """
    Returns the current date and time as a string. 
    If you are asked for the current date or time, call this function.
    Args:
        timezone: Timezone name (e.g., 'UTC', 'US/Pacific', 'Europe/London').
                 Defaults to 'America/New_York'.
    
    Returns:
        A formatted date and time string.
    """
    
    try:
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Error: Unknown timezone '{timezone}'. Please use a valid timezone name."

def local_run():
    host = "127.0.0.1"
    port = 8000
    mcp.run(transport="streamable-http",
            host=host,
            port=port)

def remote_run():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    mcp.run(transport="streamable-http",
            host=host,
            port=port)

if __name__ == "__main__":
    # local_run()
    remote_run()