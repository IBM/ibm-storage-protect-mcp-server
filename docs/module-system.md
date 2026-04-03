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

## Detailed Tools Reference

### Admin & Security

`DefineAdmin` / `UpdateUser` / `DeleteAdmin` (`define_admin`, `update_user`, `delete_admin`)
- Description: Create, modify or remove administrator accounts. Inputs include `admin_name`, `password`, `contact`.

`SetUserLock` (`set_user_lock`)
- Description: Lock or unlock an administrator account. Inputs: `user_name`, `lock_status` (`lock`/`unlock`).

`GrantAuthority` / `RevokeAuthority` (`grant_authority`, `revoke_authority`)
- Description: Grant or revoke privilege classes to/from an admin (e.g., `SYSTEM`, `POLICY`, `STORAGE`).

`RegisterLicense` / `QueryLicenseInfo` (`register_license`, `query_license_info`)
- Description: Register license files and query license compliance information.

### Server Configuration & Monitoring

`DefineServer` / `UpdateServer` / `DeleteServer` (`define_server`, `update_server`, `delete_server`)
- Description: Define server-to-server communication endpoints and groups (replication, event targets).

`DefineServerGroup` / `DefineGroupMember` / `DeleteServerGroup` (`define_server_group`, `define_group_member`, `delete_server_group`)
- Description: Manage server grouping for administrative operations.

`QueryServerStatus` (`query_server_status`)
- Description: Show server health, version, licensing, and runtime configuration summary.

`QueryServerOption` (`query_server_option`)
- Description: Query global server configuration options. Supports listing all options or filtering by name; many categories are documented in-code (communication, logging, security, DB, storage).

### Scripts, DB & Catalog

`DefineScript` / `UpdateScript` / `DeleteScript` / `QueryAutomationScript` (`define_script`, `update_script`, `delete_script`, `query_automation_script`)
- Description: Define and manage administrative automation scripts and query their contents/metadata.

`QueryCatalog` / `QueryCatalogSpace` (`query_catalog`, `query_catalog_space`)
- Description: Query the server metadata catalog (DB) usage and storage metrics.

`QuerySystemInfo` / `QueryMonitoringConfig` / `QueryMonitoringStatus` (`query_system_info`, `query_monitoring_config`, `query_monitoring_status`)
- Description: Inspect system and monitoring configuration and current monitor statuses.

### Connections & Machines

`DefineConnection` (`define_connection`)
- Description: Define a **Cloud Connection** to a cloud service (e.g., S3, Azure).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- connection_name (Required): Name of the connection.
- cloud_type (Required): Type of cloud (S3, AZURE, GOOGLE, etc).
- bucket_name (Required): Target bucket name.
- identity (Required): User ID or Access Key ID.
- password (Required): Password or Secret Key.
**Output Parameters**:
- Result: Success message indicating the connection was defined.

`UpdateConnection` (`update_connection`)
- Description: Updates a **Cloud Connection** configuration (typically password/key).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- connection_name (Required): The name of the connection.
- password (Optional): The new password or key for the cloud connection.
**Output Parameters**:
- Result: Success message indicating the connection was updated.

`DeleteConnection` (`delete_connection`)
- Description: Deletes a **Cloud Connection** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- connection_name (Required): The name of the connection to delete.
**Output Parameters**:
- Result: Success message indicating the connection was deleted.

`DefineMachine` / `UpdateMachine` / `DeleteMachine` (`define_machine`, `update_machine`, `delete_machine`)
- Description: Define, update, or delete a **Machine** (Node) declaration on the server. Inputs include `machine_name` and optional `description`.

`QueryAdminUser` (`query_admin_user`)
- Description: Display information about server administrators/users.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- admin_name (Optional): Administrator name.
**Output Parameters**:
- Administrator Name: User ID.
- Last Access: When they last logged in.
- Days Since Password Set: Password age.
- Locked: Account status.

