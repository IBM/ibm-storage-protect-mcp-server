# IBM Storage Protect MCP - Clients Module

## Overview
The **Clients Module** focuses on the lifecycle management, configuration, and organization of client nodes (backup clients) within the IBM Storage Protect environment.

## Micro-MCP-Servers

This module consists of 2 specialized micro-mcp-servers:

### 1. `mcp-server-clients-core`
**Focus**: Core Node Lifecycle (Onboarding, Maintenance, Security).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `RegisterNode` | Register a new client node | `REGISTER NODE` |
| `UpdateNode` | Update client properties | `UPDATE NODE` |
| `DeleteNode` | Decommission a client | `REMOVE NODE` |
| `RenameClient` | Rename a node | `RENAME NODE` |
| `SetClientLock` | Lock/Unlock a node | `LOCK/UNLOCK NODE` |
| `QueryClient` | View client details | `QUERY NODE` |
| `DefineNodeGroup` | Create a node group | `DEFINE NODEGROUP` |

### 2. `mcp-server-clients-config`
**Focus**: Client Options, Optimization, and Schedules (Client-side).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineClientOptSet` | Create options set | `DEFINE CLOPTSET` |
| `DefineClientOpt` | Add option to set | `DEFINE CLIENTOPT` |
| `DefineAssociation` | Associate node with schedule | `DEFINE ASSOCIATION` |
| `DefineClientAction` | Schedule ad-hoc action | `DEFINE CLIENTACTION` |

## Usage

### Running as Micro-MCP-Servers (Recommended for Context Optimization)
Run specific servers to isolate capabilities:

```bash
# Terminal 1
mcp-server-clients-core

# Terminal 2
mcp-server-clients-config
```

### Running as Unified Module
You can run both micro-mcp-servers together using the unified entry point with feature flags:

```bash
python -m sp_mcp_server.main --enable-servers clients
```

### Claude Desktop Config
```json
{
  "mcpServers": {
    "isp-clients-core": {
      "command": "mcp-server-clients-core",
      "env": { ... }
    }
  }
}
```
