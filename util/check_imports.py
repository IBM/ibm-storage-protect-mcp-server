import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "src"))



try:
    import sp_mcp_server.commands.operations as ops
    print(f"Operations module file: {ops.__file__}")
    print(f"Has QueryAlertTrigger: {'QueryAlertTrigger' in dir(ops)}")
    # print(dir(ops))
    
    from sp_mcp_server import server_groups
    print("Import server_groups successful")
except Exception as e:
    import traceback
    traceback.print_exc()
