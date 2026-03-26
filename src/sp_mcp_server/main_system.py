import asyncio
import sys
import logging
from .mcp_factory import create_mcp_server, run_server
from .server_groups import (
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

    ISP_SYSTEM_BASIC, ISP_ADMIN, ISP_SCRIPTS, ISP_DIAG
)

# Configure logging
logger = logging.getLogger("ibm-sp-system")

async def main():
    logger.info("Starting ISP System Server...")
    
    # Combine all system-related commands
    all_system_commands = ISP_SYSTEM_BASIC + ISP_ADMIN + ISP_SCRIPTS + ISP_DIAG
    
    server = create_mcp_server("ibm-sp-system", all_system_commands)
    await run_server(server)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception("Server failed")
        sys.exit(1)
