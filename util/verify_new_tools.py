import sys
import os
import inspect
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    import sp_mcp_server.commands as mcp_commands
    from sp_mcp_server.commands.base import BaseCommand, BaseOfflineCommand, BaseServermonCommand
    from sp_mcp_server.cli_wrapper import DsmAdmcWrapper, DsmServWrapper, ServermonWrapper
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def verify_tools():
    mock_admc = MagicMock(spec=DsmAdmcWrapper)
    mock_serv = MagicMock(spec=DsmServWrapper)
    mock_mon = MagicMock(spec=ServermonWrapper)
    
    total_tools = 0
    errors = []
    
    print("Verifying commands...")
    
    for name, obj in inspect.getmembers(mcp_commands):
        if inspect.isclass(obj):
            try:
                instance = None
                if issubclass(obj, BaseCommand) and obj is not BaseCommand:
                    instance = obj(mock_admc)
                elif issubclass(obj, BaseOfflineCommand) and obj is not BaseOfflineCommand:
                    instance = obj(mock_serv)
                elif issubclass(obj, BaseServermonCommand) and obj is not BaseServermonCommand:
                    instance = obj(mock_mon)
                
                if instance:
                    tool_name = instance.name
                    desc = instance.description
                    schema = instance.args_schema
                    
                    if not tool_name:
                        errors.append(f"{obj.__name__}: Missing name")
                    if not desc:
                        errors.append(f"{obj.__name__}: Missing description")
                    if not schema:
                        errors.append(f"{obj.__name__}: Missing schema")
                        
                    print(f"Verified: {tool_name} ({obj.__name__})")
                    total_tools += 1
            except Exception as e:
                errors.append(f"Error instantiating {obj.__name__}: {e}")

    print(f"\nTotal tools verified: {total_tools}")
    
    if errors:
        print("\nErrors found:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("\nAll tools verified successfully.")

if __name__ == "__main__":
    verify_tools()
