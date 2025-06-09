# Remote-MCP-Server-on-EC2
A tutorial for hosting an example MCP server on AWS EC2

# Background
MCP tools and servers are good when hosted locally, but sometimes, it is better to host them on a remote server. This repo records my struggles and learnings of hosting an MCP server on AWS EC2, and hopefully serves as a reference for others.

There are, however, quite a bit of background knowledge you need, such as how to set up an EC2 instance, running docker, ssh, git, etc and I would not be able to mention all of them here.

## Overview
Assuming we've learned how to set up a local mcp server, where we created tools and used "stdio" as the transport. Now we wonder, how can we host it on a remote server? So, the overall objective is the following:
- Create a MCP server with tools and try to use the "streamable-http" transport (which is currently the transport for remote MCP servers)
- Deploy this MCP server on a remote server, which in our case is an EC2 instance.
- Test the MCP server hosted remotely
- Connect the MCP server to Claude Desktop so that we can use the MCP tools defined in the server.

## Assumptions
Before you start following this repo, you need to set up the following things. I am sure there are many resources out there for these, and I will be brief here.
- (Optional) WSL on Windows. (I used WSL because I thought it would be easier to locally host and test the MCP server, but it might not be necessary.)
- Usual Python development environment: docker, python, pip, venv, git, etc
- An EC2 instance up and running with an Ubuntu distribution. You will need to be able to SSH into it and clone git repos.
- The EC2 security group should be configured to allow inbound traffic from your IP address. Usually ports 22 and 8000 need to be allowed.

# Deployment Steps
## My MCP Server
The `datetime_server.py` includes the processes for setting up a MCP server with a tool that retrieves current date and time. Notice that we are using the streamable-http transport option. In `remote_run()`, we are defining the host IP and port number, which are variables in the docker file.

## Deploy to EC2
(Probably) SSH into your EC2 instance, and clone this repo to it. We then build the docker image and run. Sample docker commands:
```
docker build -t datetime-mcp .
```
Note the "datetime-mcp" is just an identifier for yourself.
```
docker run --name datetime-mcp -p 8000:8000 datetime-mcp
```
Also, depending on how docker and Ubuntu is set up, you may add "sudo" in front of the docker commands.

Now the datetime server should be running on the EC2 instance and theoretically, we should be able to make requests to it somehow.

## Quick Test
To ensure the remote MCP server is running correctly before attempting to connect it to your favourite client (Claude Desktop, Cursor, etc), we can use the `test_datetime_server.py` module to make some sample requests. Don't forget to change the IP address. Note that this module should be run on your local machine. If all goes well, it should be able to give you the current datetime.

## Connect to Claude Desktop
Add the following to the `claude_desktop_config.json`. For additional help, search up how to connect MCP servers to Claude Desktop.
```
{
  "mcpServers": {
    "datetime": {
      "command": "npx",
      "args": ["mcp-remote", "http://YOUR_EC2_IP:8000/mcp", "--allow-http"]
    }
  }
}
```
A few important notes:
- This is not production-level yet, as you can see from the flag "--allow-http" that we are allowing http. For production, try to use https.
- In `datetime_server.py` the setting of `stateless_http=True` in the MCP server is important for Claude.

# For Local Testing
I am sure you would want to mess around with the tools. Here are some ways to develop and to debug.

In `datetime_server.py`, the `local_run()` function is meant for running the mcp server locally. Simply, in terminal: `python datetime_server.py`, and the server should be running in `127.0.0.1:8000`. Make necessary changes to the IP address in the test file if you like. 