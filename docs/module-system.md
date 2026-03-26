# IBM Storage Protect MCP - System Module

## Overview
The **System Module** handles global server configuration, administrative access control (security), server-to-server communications, and diagnostics.

## Micro-MCP-Servers

This module consists of 2 specialized micro-mcp-servers:

### 1. `mcp-server-system-admin`
**Focus**: Administration, Privilege Management, and Security.

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineAdmin` | Create an admin user | `DEFINE ADMIN` |
| `GrantAuthority` | Grant administrative privileges | `GRANT AUTHORITY` |
| `RevokeAuthority` | Revoke administrative privileges | `REVOKE AUTHORITY` |
| `RegisterLicense` | Register server license | `REGISTER LICENSE` |
| `SetUserLock` | Lock/Unlock admin account | `LOCK/UNLOCK ADMIN` |
| `DefineMachine` | Register machine (if applicable) | `DEFINE MACHINE` |

### 2. `mcp-server-system-config`
**Focus**: Server Configuration, Scripts, and Monitoring.

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineServer` | configure server-to-server settings | `DEFINE SERVER` |
| `DefineScript` | Create automation scripts | `DEFINE SCRIPT` |
| `QuerySystemInfo` | View global system info | `QUERY SYSTEM` |
| `QueryServerStatus` | View server status and settings | `QUERY STATUS` |

## Usage

### Running as Micro-MCP-Servers (Recommended for Context Optimization)

```bash
# Terminal 1: Security & Admins
mcp-server-system-admin

# Terminal 2: Global Config
mcp-server-system-config
```

### Running as Unified Module
You can run all system-related micro-mcp-servers together:

```bash
python -m sp_mcp_server.main --enable-servers system
```
