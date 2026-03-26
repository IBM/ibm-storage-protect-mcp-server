import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from sp_mcp_server.commands.operations import QueryAlertTrigger
    print("Import QueryAlertTrigger successful")
except Exception as e:
    import traceback
    traceback.print_exc()
