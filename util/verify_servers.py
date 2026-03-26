import sys
import os
import inspect
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

# Define dummy types for mocking
class MockTool: pass
class MockTextContent: pass
class MockImageContent: pass
class MockEmbeddedResource: pass

# Mock external dependencies BEFORE importing project modules
mcp_mock = MagicMock()
mcp_server_mock = MagicMock()
mcp_server_stdio_mock = MagicMock()
mcp_types_mock = MagicMock()

# Assign dummy types
mcp_types_mock.Tool = MockTool
mcp_types_mock.TextContent = MockTextContent
mcp_types_mock.ImageContent = MockImageContent
mcp_types_mock.EmbeddedResource = MockEmbeddedResource

sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_server_mock
sys.modules["mcp.server.stdio"] = mcp_server_stdio_mock
sys.modules["mcp.types"] = mcp_types_mock


try:
    from sp_mcp_server import mcp_factory
    from sp_mcp_server import server_groups
    
    # Mock wrappers
    mcp_factory.DsmAdmcWrapper = MagicMock()
    mcp_factory.DsmServWrapper = MagicMock()
    mcp_factory.ServermonWrapper = MagicMock()
    mcp_factory.load_config = MagicMock()
    
    # Mock Server class
    mock_server_instance = MagicMock()
    
    # Setup decorators to just return the function intact
    def mock_decorator(*args, **kwargs):
        def wrapper(func):
            return func
        return wrapper

    mock_server_instance.list_tools = MagicMock(side_effect=mock_decorator)
    mock_server_instance.call_tool = MagicMock(side_effect=mock_decorator)
    
    mcp_factory.Server = MagicMock(return_value=mock_server_instance)

except Exception as e:
    print(f"Error importing modules: {e}")
    # traceback.print_exc()
    sys.exit(1)

def verify_server_split():
    servers_to_verify = [
        ("isp-system-basic", server_groups.ISP_SYSTEM_BASIC),
        ("isp-admin", server_groups.ISP_ADMIN),
        ("isp-scripts", server_groups.ISP_SCRIPTS),
        ("isp-logs", server_groups.ISP_LOGS),
        ("isp-jobs", server_groups.ISP_JOBS),
        ("isp-alerts", server_groups.ISP_ALERTS),
        ("isp-clients", server_groups.ISP_CLIENTS),
        ("isp-schedules", server_groups.ISP_SCHEDULES),
        ("isp-client-opts", server_groups.ISP_CLIENT_OPTS),
        ("isp-domains", server_groups.ISP_DOMAINS),
        ("isp-retention", server_groups.ISP_RETENTION),
        ("isp-pools", server_groups.ISP_POOLS),
        ("isp-volumes", server_groups.ISP_VOLUMES),
        ("isp-hardware", server_groups.ISP_HARDWARE),
        ("isp-devclass", server_groups.ISP_DEVCLASS),
        ("isp-diag", server_groups.ISP_DIAG),
    ]

    total_errors = 0

    for server_name, tool_classes in servers_to_verify:
        print(f"Verifying {server_name}...")
        try:
            # Create server instance
            # Note: create_mcp_server now accepts a list of classes
            server = mcp_factory.create_mcp_server(server_name, tool_classes)
            
            # Count expected tools
            tool_count = len(tool_classes)
            
            print(f"  - Initialized successfully. Expecting {tool_count} tools.")
            
        except Exception as e:
            print(f"  - Error creating server: {e}")
            import traceback
            traceback.print_exc()
            total_errors += 1

    if total_errors == 0:
        print("\nAll server configurations verified successfully.")
    else:
        print("\nErrors found during verification.")
        sys.exit(1)

if __name__ == "__main__":
    verify_server_split()
