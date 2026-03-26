from __future__ import annotations
import asyncio
import sys
import logging
import inspect
from typing import Any, Sequence, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

from .config import load_config
from .cli_wrapper import DsmAdmcWrapper, DsmServWrapper, ServermonWrapper
from .commands.base import BaseCommand, BaseOfflineCommand, BaseServermonCommand

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("ibm-sp-mcp-server")

def create_mcp_server(server_name: str, tool_classes: List[Any], allowed_modes: List[str] = None):
    """
    Creates an MCP Server instance populated with the provided tool command classes.
    
    Args:
        server_name: The name of the MCP server.
        tool_classes: A list of command classes to instantiate and register.
        allowed_modes: List of allowed modes (e.g. ["read-only", "destructive"]). 
                       If None, all modes are allowed.
    """
    
    # Load configuration
    config = load_config()
    
    # Initialize CLI wrappers
    # We initialize all of them, but only use the ones needed by the commands.
    # This is efficient enough for now.
    admc_cli = DsmAdmcWrapper(config)
    serv_cli = DsmServWrapper(config)
    mon_cli = ServermonWrapper(config)
    
    commands = {}

    # Instantiate commands
    for obj in tool_classes:
        try:
            inst = None
            # Check for BaseCommand subclasses (Online commands)
            if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                inst = obj(admc_cli)
                
            # Check for BaseOfflineCommand subclasses (Offline commands)
            elif inspect.isclass(obj) and issubclass(obj, BaseOfflineCommand) and obj is not BaseOfflineCommand:
                inst = obj(serv_cli)
                
            # Check for BaseServermonCommand subclasses (Servermon commands)
            elif inspect.isclass(obj) and issubclass(obj, BaseServermonCommand) and obj is not BaseServermonCommand:
                inst = obj(mon_cli)
            
            if inst:
                # Filter based on allowed_modes
                if allowed_modes:
                     # Check if tool_type matches any allowed mode (e.g. "read-only")
                     # Map "full" to allow everything (or just don't pass allowed_modes if full)
                     # Assuming "read-only" is the main restriction.
                     # If allowed_modes=['read-only'] and tool_type='destructive', skip.
                     
                     # If "full" is in allowed_modes, allow everything.
                     if "full" in allowed_modes:
                         pass
                     elif inst.tool_type not in allowed_modes:
                         continue

                commands[inst.name] = inst
                
        except Exception as e:
            # Log error but continue loading other commands
            logger.error(f"Failed to instantiate command {obj}: {e}")
    
    # Create MCP Server
    server = Server(server_name)

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        tools = []
        for name, cmd in commands.items():
            tools.append(
                Tool(
                    name=cmd.name,
                    description=cmd.description,
                    inputSchema=cmd.args_schema
                )
            )
        return tools

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        if name not in commands:
            raise ValueError(f"Unknown tool: {name}")

        cmd = commands[name]
        try:
            # Execute command
            result = await asyncio.to_thread(cmd.execute, arguments or {})
            return [TextContent(type="text", text=result)]
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return server

async def run_server(server: Server):
    """Run the server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )
