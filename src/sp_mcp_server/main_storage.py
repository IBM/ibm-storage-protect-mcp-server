import asyncio
import sys
import logging
from .mcp_factory import create_mcp_server, run_server
from .server_groups import ISP_POOLS, ISP_VOLUMES, ISP_HARDWARE, ISP_DEVCLASS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Configure logging
logger = logging.getLogger("ibm-sp-mcp-server-storage")

async def main():
    logger.info("Starting ISP Storage Server...")
    
    all_storage_commands = ISP_POOLS + ISP_VOLUMES + ISP_HARDWARE + ISP_DEVCLASS
    
    server = create_mcp_server("isp-storage", all_storage_commands)
    await run_server(server)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception("Server failed")
        sys.exit(1)
