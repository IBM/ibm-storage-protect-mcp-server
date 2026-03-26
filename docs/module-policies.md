# IBM Storage Protect MCP - Policy Module

## Overview
The **Policy Module** governs data retention, lifecycle management, and protection rules. It manages policy domains, sets, management classes, and copy groups.

## Micro-MCP-Servers

This module consists of 2 specialized micro-mcp-servers:

### 1. `mcp-server-policies-lifecycle`
**Focus**: High-level policy structures and activation.

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefinePolicyDomain` | Create policy domain | `DEFINE DOMAIN` |
| `DefinePolicySet` | Create policy set | `DEFINE POLICYSET` |
| `ActivatePolicySet` | **Activate** a policy set | `ACTIVATE POLICYSET` |
| `ValidatePolicySet` | Verify a policy set | `VALIDATE POLICYSET` |
| `QueryPolicySet` | View policy hierarchy | `QUERY POLICYSET` |

### 2. `mcp-server-policies-management`
**Focus**: Granular retention rules (Management Classes).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineManagementClass` | Create management class | `DEFINE MGMTCLASS` |
| `DefineCopyGroup` | Create copy group | `DEFINE COPYGROUP` |
| `DefineSchedule` | Create admin/client schedule | `DEFINE SCHEDULE` |
| `QueryProtectionPolicy` | View retention rules | `QUERY MGMTCLASS` |

## Usage

### Running as Micro-MCP-Servers (Recommended for Context Optimization)

```bash
# Terminal 1: Lifecycle Management
mcp-server-policies-lifecycle
```

### Running as Unified Module
You can run both policy micro-mcp-servers together:

```bash
python -m sp_mcp_server.main --enable-servers policy
```
