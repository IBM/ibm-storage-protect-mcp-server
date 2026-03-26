import sys
import os
import inspect
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

# Mock external dependencies
# We need these mocks to import mcp_factory without errors
class MockTool: pass
class MockTextContent: pass
class MockImageContent: pass
class MockEmbeddedResource: pass

mcp_mock = MagicMock()
mcp_server_mock = MagicMock()
mcp_server_stdio_mock = MagicMock()
mcp_types_mock = MagicMock()

mcp_types_mock.Tool = MockTool
mcp_types_mock.TextContent = MockTextContent
mcp_types_mock.ImageContent = MockImageContent
mcp_types_mock.EmbeddedResource = MockEmbeddedResource

sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_server_mock
sys.modules["mcp.server.stdio"] = mcp_server_stdio_mock
sys.modules["mcp.types"] = mcp_types_mock

try:
    from sp_mcp_server.commands import system, operations, storage, policies, clients, offline, servermon
    
    servers = [
        ("isp-ops", [system, operations]),
        ("isp-storage", [storage]),
        ("isp-policy", [policies, clients]),
        ("isp-diag", [offline, servermon])
    ]

    print(f"{'Server':<15} | {'Tools':<5}")
    print("-" * 23)
    
    for server_name, modules in servers:
        tool_count = 0
        for mod in modules:
            for name, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj) and name.startswith(("Define", "Update", "Delete", "Query", "Run", "List")):
                        if hasattr(obj, "name") and hasattr(obj, "description"):
                            tool_count += 1
        print(f"{server_name:<15} | {tool_count:<5}")

except Exception as e:
    print(f"Error: {e}")
