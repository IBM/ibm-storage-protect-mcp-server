import asyncio
import sys
import logging
from .mcp_factory import create_mcp_server, run_server
from .server_groups import ISP_DOMAINS, ISP_RETENTION, ISP_SCHEDULES
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Configure logging
logger = logging.getLogger("ibm-sp-mcp-server-policy")

async def main():
    logger.info("Starting ISP Policy Server...")
    
    all_policy_commands = ISP_DOMAINS + ISP_RETENTION + ISP_SCHEDULES
    
    server = create_mcp_server("isp-policy", all_policy_commands)
    await run_server(server)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception("Server failed")
        sys.exit(1)
