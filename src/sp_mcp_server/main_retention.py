from __future__ import annotations
import asyncio
from .mcp_factory import create_mcp_server, run_server
from .server_groups import ISP_RETENTION
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    server = create_mcp_server("isp-retention", ISP_RETENTION)
    asyncio.run(run_server(server))

if __name__ == "__main__":
    main()
