import asyncio
import sys
import logging
import argparse
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .mcp_factory import create_mcp_server, run_server
from .server_groups import (
    ISP_CLIENTS_CORE, ISP_CLIENTS_CONFIG,
    ISP_STORAGE_POOLS, ISP_STORAGE_HARDWARE, ISP_STORAGE_DEVICE,
    ISP_POLICIES_LIFECYCLE, ISP_POLICIES_MANAGEMENT,
    ISP_SYSTEM_ADMIN, ISP_SYSTEM_CONFIG,
    ISP_OPS_PROTECTION, ISP_OPS_MAINTENANCE, ISP_OPS_RULES
)

# Configure logging
logger = logging.getLogger("ibm-sp-mcp-server")

# Define Server Group Mappings
# Define Server Group Mappings
SERVER_GROUPS = {
    # System & Security
    "system": ISP_SYSTEM_ADMIN + ISP_SYSTEM_CONFIG,
    
    # Operations
    "operations": ISP_OPS_PROTECTION + ISP_OPS_MAINTENANCE + ISP_OPS_RULES,
    
    # Clients
    "clients": ISP_CLIENTS_CORE + ISP_CLIENTS_CONFIG,
    
    # Policy
    "policy": ISP_POLICIES_LIFECYCLE + ISP_POLICIES_MANAGEMENT,
    
    # Storage
    "storage": ISP_STORAGE_POOLS + ISP_STORAGE_HARDWARE + ISP_STORAGE_DEVICE
}

def parse_args():
    parser = argparse.ArgumentParser(description="IBM Storage Protect MCP Server")
    parser.add_argument(
        "--enable-servers",
        type=str,
        default="system,operations,clients,policy,storage",
        help="Comma-separated list of server modules to enable (default: all)"
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="full",
        choices=["full", "read-only"],
        help="Operation mode: 'full' (all commands) or 'read-only' (query/info only)"
    )
    return parser.parse_args()

async def main():
    args = parse_args()
    
    # Determine enabled servers
    enabled_servers = [s.strip() for s in args.enable_servers.split(",") if s.strip()]
    
    # Collect tools
    tool_classes = []
    for server_key in enabled_servers:
        if server_key in SERVER_GROUPS:
            logger.info(f"Enabling server module: {server_key}")
            tool_classes.extend(SERVER_GROUPS[server_key])
        else:
            logger.warning(f"Unknown server module: {server_key}")
            
    if not tool_classes:
        logger.error("No valid server modules enabled. Exiting.")
        sys.exit(1)

    # Determine allowed modes
    allowed_modes = ["read-only"] if args.mode == "read-only" else ["full"]
    logger.info(f"Starting server in {args.mode} mode")

    server = create_mcp_server("ibm-sp-mcp-server", tool_classes, allowed_modes=allowed_modes)
    await run_server(server)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception("Server failed")
        sys.exit(1)
