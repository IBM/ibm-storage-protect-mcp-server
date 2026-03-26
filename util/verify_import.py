
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

try:
    print("Attempting to import sp_mcp_server.commands.servermon...")
    from sp_mcp_server.commands.servermon import FetchMonitoringData
    print("Import successful!")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
