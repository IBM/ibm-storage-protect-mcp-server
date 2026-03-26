import asyncio
import sys
import logging
from .mcp_factory import create_mcp_server, run_server
from .server_groups import ISP_OPS_RULES
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-server-ops-rules")

async def main():
    server = create_mcp_server("mcp-server-ops-rules", ISP_OPS_RULES)
    await run_server(server)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
