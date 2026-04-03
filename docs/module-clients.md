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

## Detailed Tools Reference

Below are the supported MCP tools in the Clients module. Each entry includes the programmatic name and the tool description text extracted verbatim from the source code.

### `RegisterNode` (`register_node`)
Registers a new **Node** (also commonly called a Client) in SP for data protection. A Node represents a source system (like a server, laptop, or VM) that contains data to be backed up.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Required): The unique name of the node to register (also referred to as `node_name` in some APIs).
- password (Required): The password used for node authentication.
- domain_name (Required): The **Policy Domain** (SLA) to which the node will be assigned.
**Output Parameters**:
- Result: Success message indicating the node was registered.

### `RenameClient` (`rename_client`)
Renames an existing **Node** (Client). This updates the unique identifier used for all backup and restore operations for the source system.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- current_name (Required): The current name of the node.
- new_name (Required): The new name for the node.
**Output Parameters**:
- Result: Success message indicating the node was renamed.

### `SetClientLock` (`set_client_lock`)
Locks or unlocks a **Node** to control access to the backup server. A locked node cannot perform backups or restores.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Required): The name of the node.
- lock_status (Required): Set to 'lock' to disable access, or 'unlock' to enable access.
**Output Parameters**:
- Result: Success message indicating the lock status was updated.

### `UpdateNode` (`update_node`)
Updates properties of an existing **Node** (Client).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): Name of the node to update.
- domain_name (Optional): Assign to a different **Policy Domain**.
- password (Optional): Update the node password.
- contact (Optional): Update contact information.
- cloptset (Optional): Assign a different **Client Configuration Profile** (Option Set).
**Output Parameters**:
- Result: Success message indicating the node was updated.

### `DeleteClient` (`delete_client`)
Decommissions a **Node** and removes all its configuration from the server. This is a destructive operation.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Required): The name of the node to delete.
**Output Parameters**:
- Result: Success message indicating the node was deleted.

### `DeleteNode` (`delete_node`)
Deletes a **Client** (Node). Similar to delete_client but using 'node' terminology.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The name of the node to delete.
**Output Parameters**:
- Result: Success message indicating the node was deleted.

### `QueryClient` (`query_client`)
Display information about registered clients (Nodes).


**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Name of the node to query.
- domain_name (Optional): Filter by Policy Domain. (historically `policy_group` in code)

**Output Parameters**:
- Node Name: The name of the node.
- Platform: The node operating system.
- Policy Domain: The Policy Domain the node belongs to.
- Last Access: Days since last communication.
- Locked: Whether the node is locked.
- Password Set Date: Date password was last set.

### `QueryProxyClient` (`query_proxy_client`)
Query relationships where one node (agent) is authorized to act on behalf of another (target).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- target_client (Optional): Target node name.
- agent_client (Optional): Agent node name.

**Output Parameters**:
- Target Node: The node whose data is being accessed.
- Agent Node: The node granted access.

### `QueryReplicationClient` (`query_replication_client`)
Display information about replication status for a node.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name.

**Output Parameters**:
- Node Name: The executing node.
- State: Replication state (e.g., SYNC, SENDING).
- Target Server: Destination for replication.

### `QueryPVUEstimate` (`query_pvu_estimate`)
Display an estimate of the Processor Value Units (PVU) for license calculation.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name.

**Output Parameters**:
- Node Name: The client.
- PVU Estimate: Estimated PVU details.

---

### Client Options & Profiles (mcp-server-clients-config)

### `DefineClientOptSet` (`define_client_opt_set`)
Defines a **Client Option Set** in SP. This profile contains a set of rules (like include/exclude filters) that can be applied to Nodes.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set_name (Required): Unique name for the configuration profile.
- description (Optional): Description of the profile's purpose.
**Output Parameters**:
- Result: Success message indicating the profile was created.

### `DefineClientOpt` (`define_client_opt`)
Adds a specific configuration rule (Option) to a **Client Option Set**. For example, adding an 'INCLUDE' or 'EXCLUDE' rule.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set_name (Required): Name of the profile to modify.
- option_name (Required): The setting name (e.g., 'DIRMC', 'INCLUDE', 'EXCLUDE').
- option_value (Required): The value for the setting (e.g., file pattern).
- seq_number (Optional): Sequence number to order the rule.
- force (Optional): 'YES' or 'NO' to force the option on the client.
**Output Parameters**:
- Result: Success message indicating the rule was added.

### `UpdateClientOptSet` (`update_client_opt_set`)
Updates the description of a **Client Option Set**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set_name (Required): The name of the option set.
- description (Optional): The new description.
**Output Parameters**:
- Result: Success message indicating the option set was updated.

### `UpdateClientOpt` (`update_client_opt`)
Updates a specific **Client Option** within a set. Can change the sequence number or force flag.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set_name (Required): The name of the option set.
- option_name (Required): The option name.
- seq_number (Required): The existing sequence number to identify the option.
- new_seq_number (Required): The new sequence number to assign.
**Output Parameters**:
- Result: Success message indicating the option was updated.

### `UpdateProfile` (`update_profile`)
Updates a **Profile** description. Profiles are used to subscribing to configuration info.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- profile_name (Required): The name of the profile.
- description (Optional): The new description.
**Output Parameters**:
- Result: Success message indicating the profile was updated.

### `DeleteClientOptSet` (`delete_client_opt_set`)
Deletes a **Client Option Set**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set_name (Required): The name of the option set to delete.
**Output Parameters**:
- Result: Success message indicating the option set was deleted.

### `DeleteClientOpt` (`delete_client_opt`)
Deletes a specific **Client Option** from a set.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set_name (Required): The name of the option set.
- option_name (Required): The option name to remove.
- seq_number (Optional): Specific sequence number.
**Output Parameters**:
- Result: Success message indicating the option was deleted.

### `QueryClientOptionSet` (`query_client_option_set`)
Query node option sets, which centralize node configuration.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- option_set (Optional): Name of the option set.

**Output Parameters**:
- Option Set Name: Name of the set.
- Option: The configuration option (e.g., INCLUDE/EXCLUDE).
- Value: The value of the option.

### `DefineNodeGroup` (`define_node_group`)
Defines a **Node Group** in SP. Groups allow you to manage multiple Nodes collectively.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): Name of the new Client Group.
- description (Optional): Description of the group.
**Output Parameters**:
- Result: Success message indicating the group was defined.

### `UpdateNodeGroup` (`update_node_group`)
Updates an existing **Node Group**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the node group to update.
- description (Optional): The new description for the group.
**Output Parameters**:
- Result: Success message indicating the group was updated.

### `RemoveClientFromGroup` (`remove_client_from_group`)
Removes a **Node** from a **Node Group**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the Node Group.
- client_name (Required): The name of the Node to remove from the group.
**Output Parameters**:
- Result: Success message indicating the Node was removed from the group.

### `DeleteNodeGroup` (`delete_node_group`)
Deletes a **Node Group**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The name of the group to delete.
**Output Parameters**:
- Result: Success message indicating the group was deleted.

### `QueryClientGroup` (`query_client_group`)
Query definitions of node groups.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Optional): Name of the node group.

**Output Parameters**:
- Group Name: Name of the node group.
- Description: Description of the group.

### `DefineAssociation` (`define_association`)
Associates **Nodes** with a **Schedule** to automate backup operations.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The Policy Domain where the schedule exists.
- schedule_name (Required): The name of the Schedule.
- node_names (Required): Space-separated list of node names to associate.
**Output Parameters**:
- Result: Success message indicating the association was created.

### `DeleteAssociation` (`delete_association`)
Deletes a **Node Association** with a schedule.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Policy domain.
- schedule_name (Required): Schedule name.
- node_names (Required): Node name(s) to disassociate.
**Output Parameters**:
- Result: Success message indicating the association was deleted.

### `QueryActiveSession` (`query_active_session`)
Display information about currently active administrative and node sessions.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- session_id (Optional): Specific session ID to query.

**Output Parameters**:
- Session ID: Unique identifier for the session.
- Node Name: Name of the connected node/admin.
- State: Current activity state (e.g., Run, Idle).
- Bytes Sent/Recv: Amount of data transferred.
- Wait Time: Time spent waiting for media.

### `QueryDataOccupancy` (`query_data_occupancy`)
Display statistics on where node data is stored and how much space it occupies.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name to filter.
- backup_volume (Optional): Specific backup volume/filespace name.

**Output Parameters**:
- Node Name: The node.
- Backup Volume Type: Specific file space or workload.
- Storage Pool: Where the data resides.
- Files: Number of files stored.
- Physical Space: Space occupied (MB/GB).

### `QueryAuditDataOccupancy` (`query_audit_data_occupancy`)
Query calculated total storage utilization for a node for audit purposes.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name to filter.

**Output Parameters**:
- Node Name: The node.
- Backup Data: Space used by backup data.
- Archive Data: Space used by archive data.
- Total Space: Total space utilized.

### `QueryClientBackupVolume` (`query_client_backup_volume`)
Query information about node backup volumes (File Spaces). A backup volume represents a logical partition of data managed for a node (e.g., C: drive, /home, System State).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name.
- backup_volume (Optional): Backup volume/filespace name.

**Output Parameters**:
- Node Name: The node.
- Backup Volume (File Space): The specific volume or mount point.
- Capacity: Total size of the volume on the client.
- Pct Utilized: Percentage used on the client.

### `QueryVirtualMountPoint` (`query_virtual_mount_point`)
Query virtual mount point mappings for nodes, which map local paths to virtual filespaces.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name.
- virtual_path (Optional): Virtual mount point name.

**Output Parameters**:
- Node Name: The node.
- Virtual Mount Point: Name of the virtual filespace.
- Local Path: The physical path mapped.

### `QueryClientDataPlacement` (`query_client_data_placement`)
Query distribution of node data across storage containers and volumes.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name.
- storage_container (Optional): Storage container name.

**Output Parameters**:
- Node Name: The node.
- Storage Pool: The container.
- Volume Name: The specific volume.

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
