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

`DefineAdmin` (`define_admin`)
- Description: Defines an **Administrator** account with specific privileges.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- admin_name (Required): The name of the administrator.
- password (Required): The password for the administrator.
- contact (Optional): Contact information.

**Output Parameters**:
- Result: Success message indicating the administrator was defined.

`UpdateUser` (`update_user`)
- Description: Updates an **Administrator** account (System User). Modify password or contact info.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- user_name (Required): The name of the administrator to update.
- password (Optional): The new password.
- contact (Optional): New contact information.

**Output Parameters**:
- Result: Success message indicating the user was updated.

`DeleteAdmin` (`delete_admin`)
- Description: Deletes an **Administrator** account.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- admin_name (Required): The name of the administrator to delete.

**Output Parameters**:
- Result: Success message indicating the administrator was deleted.

`SetUserLock` (`set_user_lock`)
- Description: Locks or unlocks an **Administrator** account. Locked admins cannot log in.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- user_name (Required): The name of the administrator.
- lock_status (Required): 'lock' to disable access, 'unlock' to enable access.

**Output Parameters**:
- Result: Success message indicating the lock status was updated.

`GrantAuthority` (`grant_authority`)
- Description: Grants specific **Privilege Classes** to an administrator. Controls authorization level.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- user_name (Required): The name of the administrator.
- classes (Required): Space-separated list of privilege classes (e.g., 'system policy storage').

**Output Parameters**:
- Result: Success message indicating the authority was granted.

`RevokeAuthority` (`revoke_authority`)
- Description: Revokes specific **Privilege Classes** from an administrator.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- user_name (Required): The name of the administrator.
- classes (Required): Space-separated list of privilege classes to revoke.

**Output Parameters**:
- Result: Success message indicating the authority was revoked.

`RegisterLicense` (`register_license`)
- Description: Registers a new **Software License** key from a specified file.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- file_path (Required): The full path to the license file on the server.

**Output Parameters**:
- Result: Success message indicating the license was registered.

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

`QueryLicenseInfo` (`query_license_info`)
- Description: Display software license compliance information.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- License Name: Name of the licensed feature.
- Compliance Status: Whether the server is compliant.
- Licensed Units: Number of units authorized.

### Server Configuration & Monitoring

`DefineServer` (`define_server`)
- Description: Define a **Server** for server-to-server communications (e.g., replication, library sharing).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- server_name (Required): Name of the server.
- password (Required): Password for authentication.
- hl_address (Required): High level address (IP address or DNS name).
- ll_address (Required): Low level address (TCP Port).
- description (Optional): Description.

**Output Parameters**:
- Result: Success message indicating the server was defined.

`UpdateServer` (`update_server`)
- Description: Updates the properties of an existing **Server** definition used for server-to-server communications.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- server_name (Required): The name of the server to update.
- password (Optional): Update the password.
- hl_address (Optional): Update the High Level Address (IP/Hostname).
- ll_address (Optional): Update the Low Level Address (Port).
- description (Optional): Update the description.

**Output Parameters**:
- Result: Success message indicating the server was updated.

`DeleteServer` (`delete_server`)
- Description: Deletes a **Server** definition. This removes the configuration for server-to-server communication.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- server_name (Required): The name of the server to delete.

**Output Parameters**:
- Result: Success message indicating the server was deleted.

`DefineServerGroup` (`define_server_group`)
- Description: Define a **Server Group** to manage multiple servers as a single unit.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the new server group.
- description (Optional): Description of the group.

**Output Parameters**:
- Result: Success message indicating the server group was defined.

`UpdateServerGroup` (`update_server_group`)
- Description: Updates the description of an existing **Server Group**.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the server group.
- description (Optional): The new description for the group.

**Output Parameters**:
- Result: Success message indicating the group was updated.

`DeleteServerGroup` (`delete_server_group`)
- Description: Deletes a **Server Group**. This removes the grouping but does not delete the member servers themselves.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the server group to delete.

**Output Parameters**:
- Result: Success message indicating the group was deleted.

`DefineGroupMember` (`define_group_member`)
- Description: Add a **Server** to a **Server Group**.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the server group.
- server_name (Required): The name of the server to add.

**Output Parameters**:
- Result: Success message indicating the server was added to the group.

`DeleteGroupMember` (`delete_group_member`)
- Description: Removes a **Server** from a **Server Group**.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the server group.
- server_name (Required): The name of the server to remove.

**Output Parameters**:
- Result: Success message indicating the member was removed.

`DefineEventServer` (`define_event_server`)
- Description: Define a server as the **Event Server** (target for logging events).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- server_name (Required): The name of the server to receive events.

**Output Parameters**:
- Result: Success message indicating the event server was defined.

`DeleteEventServer` (`delete_event_server`)
- Description: Deletes an **Event Server** definition.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- server_name (Required): The name of the event server to delete.

**Output Parameters**:
- Result: Success message indicating the event server was deleted.

`QueryServerStatus` (`query_server_status`)
- Description: Display the general health and status of the backup server.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Server Name: The name of the backup server.
- Server Date/Time: Current date and time on the server.
- Server Version: The software version of the server.
- License Status: Summary of license compliance.
- Activity Log Retention: How long event logs are kept.
- Password Expiration: Settings for password usage.

`QueryServerOption` (`query_server_option`)
- Description: Display global server configuration options (e.g., ACTIVELOGSIZE, ARCHLOGSIZE).

**Note**: This tool provides read-only information. There is currently **no tool** to modify or set these server options.

**Usage Guide**:
- Call without arguments to list ALL options and their current values.
- Call with `option_name` to query a specific option.
- Supports wildcards (e.g., `LOG*`).

**Common Options by Category**:
- **Communication**: TCPPORT, MAXSESSIONS, IDLETIMEOUT, COMMMETHOD, COMMTIMEOUT, MINJOBS, MAXJOBS.
- **Logging**: ACTIVELOGDIRECTORY, ACTIVELOGSIZE, ARCHLOGDIRECTORY, MIRRORLOGDIRECTORY, ACTLOGRETENTION.
- **Security**: PASSWORDLIFE, FIPSMODE, LDAPURL, ADMINONCLIENTPORT, REGAUTH.
- **Database**: DBMEMPERCENT, ARCHLOGUSEDTHRESHOLD, BUFFPOOLSIZE.
- **Storage/Cloud**: EXPINTERVAL, MOVEBATCHSIZE, MOVESIZETHRESH, RECLAIM, DEDUPREQUIRESBACKUP.
- **Integrity**: AUDITSTORAGE, CRCVALIDATE, CHECKTAPEPOS.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_name (Optional): Specific option to query (e.g., 'MAXSESSIONS').

**Output Parameters**:
- Option: Name of the setting.
- Setting: Current value.

### Scripts, DB & Catalog

`DefineScript` (`define_script`)
- Description: Define an **Administrative Script** to automate server tasks.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- script_name (Required): Name of the script.
- description (Optional): Description of what the script does.
- line (Optional): Initial command line to add to the script.

**Output Parameters**:
- Result: Success message indicating the script was defined.

`UpdateScript` (`update_script`)
- Description: Updates an existing **Administrative Script**. You can change the description or append commands.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- script_name (Required): The name of the script to update.
- description (Optional): New description for the script.
- line (Optional): A command line to add or update in the script.

**Output Parameters**:
- Result: Success message indicating the script was updated.

`DeleteScript` (`delete_script`)
- Description: Deletes an **Administrative Script**.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- script_name (Required): The name of the script to delete.

**Output Parameters**:
- Result: Success message indicating the script was deleted.

`QueryAutomationScript` (`query_automation_script`)
- Description: Query defined automation scripts.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- script_name (Optional): Script name.

**Output Parameters**:
- Script Name: Name of the script.
- Description: What the script does.
- Lines: Number of lines in the script.

`QueryCatalog` (`query_catalog`)
- Description: Display information about the server's metadata catalog (database).

**Note**: This is a read-only tool. There is currently **no tool** to extend or increase the database size.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- format (Optional): Level of detail (standard, detailed).

**Output Parameters**:
- Available Space: Total space assigned to the catalog.
- Assigned Capacity: Space actually allocated.
- Maximum Extension: How much the catalog can grow.
- Pages/Usable Pages: Internal database page metrics.
- Used Space: Percentage of catalog space currently used.

`QueryCatalogSpace` (`query_catalog_space`)
- Description: Display storage space utilization for the metadata catalog (database).

**Note**: This is a read-only tool. There is currently **no tool** to extend or increase the database size.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Location: Directory or path of the catalog storage.
- Total Space: Total capacity of the directory.
- Used Space: Space currently used by the catalog.
- Free Space: Available space for growth.

`QuerySystemInfo` (`query_system_info`)
- Description: Query hardware and system information from a client or the server.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Name of the client/workload to query.

**Output Parameters**:
- Node Name: Name of the client/system.
- Platform: Operating system platform.
- Processor Info: Details about the CPU architecture.
- RAM: Total memory available.

`QueryMonitoringConfig` (`query_monitoring_config`)
- Description: Display configuration settings for system monitoring.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Setting Name: The monitoring option.
- Value: Current configuration value.

`QueryMonitoringStatus` (`query_monitoring_status`)
- Description: Display current status of system monitors.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Monitor Name: Name of the monitor.
- Status: Active/Inactive status.

`QueryRecoveryLog` (`query_recovery_log`)
- Description: Display information about the transaction recovery log.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- format (Optional): Level of detail (standard, detailed).

**Output Parameters**:
- Total Space: Total size of the recovery log.
- Used Space: Amount of log space currently in use.
- Free Space: Remaining log space.
- Log Pool Pct: Percentage of the log pool used.

`QueryEnabledEvents` (`query_enabled_events`)
- Description: Query which system events are currently enabled for logging or alerting.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Event Name: The type of event.
- Enabled: Whether the event is active.
- Receiver: Where the event is sent (e.g., CONSOLE, ACTLOG).

`QueryEventRules` (`query_event_rules`)
- Description: Query configured event rules which filter or direct specific events.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Rule Name: Name of the rule.
- Description: What the rule does.

`QueryEventReceiver` (`query_event_receiver`)
- Description: Query configured event receivers (destinations for events).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Receiver Name: Name of the receiver.
- Description: Details about the receiver.

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

`DefineMachine` (`define_machine`)
- Description: Define a **Machine** (Client) manually, declaring its existence to the server.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- machine_name (Required): The name of the machine to define.
- description (Optional): Description of the machine.

**Output Parameters**:
- Result: Success message indicating the machine was defined.

`UpdateMachine` (`update_machine`)
- Description: Updates properties of a registered **Machine** (Client).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- machine_name (Required): The name of the machine.
- description (Optional): New description for the machine.

**Output Parameters**:
- Result: Success message indicating the machine was updated.

`DeleteMachine` (`delete_machine`)
- Description: Deletes a **Machine** (Client) definition.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- machine_name (Required): The name of the machine to delete.

**Output Parameters**:
- Result: Success message indicating the machine was deleted.



