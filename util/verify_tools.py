
import sys
import os
from typing import Dict, Any

# Add src to python path
sys.path.append(os.path.join(os.getcwd(), "src"))

from sp_mcp_server.commands.query import ONLINE_QUERY_COMMAND_CLASSES, OFFLINE_QUERY_COMMAND_CLASSES, SERVERMON_COMMAND_CLASSES

class MockCLI:
    def execute(self, command: str) -> tuple:
        # Return stdout, stderr, code
        return f"EXECUTED: {command}", "", 0

def verify_tool_classes():
    all_commands = ONLINE_QUERY_COMMAND_CLASSES + OFFLINE_QUERY_COMMAND_CLASSES + SERVERMON_COMMAND_CLASSES
    print(f"Verifying {len(all_commands)} tools...")
    
    # Simple mock that works for both DsmAdmcWrapper and DsmServWrapper because
    # verify logic only instantiates class. 
    # But wait, BaseCommand init takes 'cli'.
    # We pass MockCLI. Does MockCLI have 'execute'? 
    # No, it currently has execute_command. BaseCommand calls self.cli.execute(cmd).
    # I should update MockCLI to have execute method returning tuple.
    
    mock_cli = MockCLI()
    
    for cls in all_commands:
        try:
            # Instantiate
            tool = cls(mock_cli)
            
            # Check properties
            name = tool.name
            desc = tool.description
            schema = tool.args_schema
            
            # Verify description format
            if "**Input Parameters**" not in desc or "**Output Parameters**" not in desc:
                # Some simple tools might not have inputs, but we expect Outputs in all
                if "**Output Parameters**" not in desc:
                    print(f"WARNING: {name} description missing Output Parameters section")

            print(f"[OK] {name}")
            
        except Exception as e:
            print(f"[FAIL] {cls.__name__}: {str(e)}")

if __name__ == "__main__":
    verify_tool_classes()
