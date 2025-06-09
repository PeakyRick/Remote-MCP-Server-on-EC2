import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

EC2_IP = "256.256.256.256"  # TODO: Change to your EC2 IP

async def main():
    transport = StreamableHttpTransport(url=f"http://{EC2_IP}:8000/mcp")
    async with Client(transport=transport) as client:
        await client.ping()
        print("Server is running")

        tools = await client.list_tools()
        print(f"Available Tools: {tools}")

        datetime = await client.call_tool("current_datetime")
        print(datetime)

if __name__ == "__main__":
    asyncio.run(main())