# IBM Storage Protect MCP - Operations Module

## Overview
The **Operations Module** is the daily-driver for server maintenance, disaster recovery, daily protection tasks, and automation rules.

## Micro-MCP-Servers

This module consists of 3 specialized micro-mcp-servers:

### 1. `mcp-server-ops-protection`
**Focus**: Critical Protection (Backup DB, DR, Replication).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `BackupDB` | Backup the server database | `BACKUP DB` |
| `RestoreDB` | Restore the server database | `RESTORE DB` |
| `QueryDRStatus` | Check disaster recovery status | `QUERY DRMEDIA` |
| `QueryReplication` | Check replication status | `QUERY REPLICATION` |
| `QueryRecoveryPlan` | View DR plan | `QUERY RPF` |

### 2. `mcp-server-ops-maintenance`
**Focus**: Data Management and Maintenance.

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `MoveData` | Move data between volumes | `MOVE DATA` |
| `ReclaimStorage` | Reclaim fragmented space | `RECLAIM STGPOOL` |
| `RunServerMon` | Run server monitoring diagnostics | `(Internal Script)` |
| `DefineBackupSet` | Create a portable backup set | `DEFINE BACKUPSET` |

### 3. `mcp-server-ops-rules`
**Focus**: Automation and Alerting.

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineAlertTrigger` | Create an alert trigger | `DEFINE ALERTTRIGGER` |
| `UpdateAlertStatus` | Acknowledge/Close alerts | `UPDATE ALERT` |
| `DefineStorageRule` | Create tiering/replication rules | `DEFINE STGRULE` |

## Usage

### Running as Micro-MCP-Servers (Recommended for Context Optimization)

```bash
# Terminal 1: Daily Protection/DR
mcp-server-ops-protection

# Terminal 2: Maintenance Tasks
mcp-server-ops-maintenance
```

### Running as Unified Module
You can run all operations-related micro-mcp-servers together:

```bash
python -m sp_mcp_server.main --enable-servers operations
```


## Detailed Tools Reference

The following entries contain the tool descriptions verbatim as defined in the source `commands/operations` modules.

### `DefineClientAction` (`define_client_action`)
Define a **Node Action** (one-time schedule). Forces a node operation (e.g., backup) immediately or shortly.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The node name (or * for all).
- action (Required): The action to perform (e.g., INCREMENTAL).
**Output Parameters**:
- Result: Success message indicating the action was scheduled.

### `MoveDataContainer` (`move_data_container`)
Moves data from one volume to another within the same or different storage pool. Useful for emptying volumes.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- volume_name (Required): The name of the source volume to move data from.
- target_pool (Optional): The destination storage pool. If omitted, uses the same pool.
**Output Parameters**:
- Result: Success message indicating the data movement has started.

### `MoveClientData` (`move_client_data`)
Moves data belonging to a specific client node to a different storage pool.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Required): The name of the client node.
- source_pool (Required): The source storage pool where data currently resides.
- target_pool (Required): The destination storage pool.
**Output Parameters**:
- Result: Success message indicating the data movement has started.

### `MigrateStorageTarget` (`migrate_storage_target`)
Manually triggers data migration for a storage pool. Moves data from higher-level pool (disk) to lower-level pool (tape/cloud).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): The name of the storage pool to migrate.
- low_mig (Optional): The low migration threshold percentage. Migration stops when utilization reaches this.
**Output Parameters**:
- Result: Success message indicating the migration process has started.

### `ReclaimStorageSpace` (`reclaim_storage_space`)
Manually triggers space reclamation for a storage pool. Reclaims fragmented space on sequential access volumes.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): The name of the storage pool to reclaim.
- threshold (Optional): The percentage of reclaimable space required to trigger reclamation for a volume.
**Output Parameters**:
- Result: Success message indicating the reclamation process has started.

### `QueryBackgroundJob` (`query_background_job`)
Display information about currently active background processes/jobs.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- job_id (Optional): Specific job/process number.

**Output Parameters**:
- Process ID: Unique job identifier.
- Description: Type of job (e.g., Migration, Backup).
- Status: Current state.
- Files/Bytes Processed: Progress metrics.

### `QueryExportJob` (`query_export_job`)
Query for active or suspended export operations (data movement out of system).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name to filter export jobs.

**Output Parameters**:
- Process ID: The background job ID.
- State: Active or Suspended.
- Phase: Export phase.

### `QueryMaintenanceJob` (`query_maintenance_job`)
Query a specific maintenance job.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- job_id (Optional): Job ID.

**Output Parameters**:
- Job ID: The job identifier.
- Type: Type of maintenance.
- Status: Current status.

### `QueryRestoreJob` (`query_restore_job`)
Query restartable restore sessions.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Session ID: The restore session.
- Node Name: The node restoring.
- State: Restartable state.

### Replication & Protection Queries

### `QueryProtectionStatus` (`query_protection_status`)
Query the status of storage pool protection operations (e.g., replication to target).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Storage Pool: The source pool.
- Protection Status: Synced or not.

### `QueryReplicationFailures` (`query_replication_failures`)
Query detailed data about replication failures.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Node Name: The node that failed.
- File Space: The backup volume that failed.
- Failure Date: Time of failure.

### `QueryReplicationStatus` (`query_replication_status`)
Query active node replication processes.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name to filter.

**Output Parameters**:
- Node Name: Node being replicated.
- Bytes Replicated: Data moved.
- Status: Current activity.

### `QueryReplicationRule` (`query_replication_rule`)
Query rules governing replication behavior.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Optional): Rule name.

**Output Parameters**:
- Rule Name: Name of the rule.
- Priority: Execution priority.

### `QueryReplicationServer` (`query_replication_server`)
Query a defined replication server.

### Filesystem & Virtual FS

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.

- server_name (Optional): Server name.


**Output Parameters**:
- Server Name: The partner server.
- Server Address: Network location.

### Backup Set Management

### `DefineBackupSet` (`define_backup_set`)
Define a **Backup Set** from existing backup versions on the server. Backup sets are portable collections of node data.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The node name.
- backup_set_name (Required): The name of the new backup set.
- file_space_name (Optional): Specific file space to include.
**Output Parameters**:
- Result: Success message indicating the backup set was defined.

### `UpdateBackupSet` (`update_backup_set`)
Updates the retention rule for a **Backup Set**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The client node name.
- backup_set_name (Required): The backup set name.
- retention (Required): New retention period in days or NOLIMIT.
**Output Parameters**:
- Result: Success message indicating the backup set was updated.

### `DeleteBackupSet` (`delete_backup_set`)
Deletes a **Backup Set**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The client node name.
- backup_set_name (Required): The backup set name.
**Output Parameters**:
- Result: Success message indicating the backup set was deleted.

### Retention / Hold

### `DefineHold` (`define_hold`)
Define a **Hold** on retention set data. Prevents deletion of retention sets until the hold is released.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- hold_name (Required): The name of the hold to define.
**Output Parameters**:
- Result: Success message indicating the hold was defined.

### `DeleteHold` (`delete_hold`)
Deletes a **Hold** on retention set data.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- hold_name (Required): The name of the hold to delete.
**Output Parameters**:
- Result: Success message indicating the hold was deleted.

### `DefineRetentionRule` (`define_retention_rule`)
Define a **Retention Rule** for managing long-term data retention (Retention Sets).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The name of the retention rule.
- node_name (Required): The node name pattern to apply the rule to.
**Output Parameters**:
- Result: Success message indicating the rule was defined.

### Rules & Automation (select tools)

### `DefineSpaceTrigger` (`define_space_trigger`)
Define a **Space Trigger** for a storage pool. Automatically expands the pool when space runs low.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Optional): The name of the storage pool. If omitted, applies to all pools.
- full_pct (Optional): The utilization percentage to trigger expansion. Default: 80%.
- space_expansion (Optional): The percentage to expand the pool by. Default: 20%.
**Output Parameters**:
- Result: Success message indicating the trigger was defined.

### `UpdateSpaceTrigger` (`update_space_trigger`)
Updates a **Space Trigger** for a storage pool.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Optional): The storage pool name. If omitted, updates global trigger.
- full_pct (Optional): New full percentage threshold to trigger expansion.
- space_expansion (Optional): New percentage to expand the pool by.
**Output Parameters**:
- Result: Success message indicating the trigger was updated.

### `DeleteSpaceTrigger` (`delete_space_trigger`)
Deletes a **Space Trigger** from a storage pool.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Optional): The storage pool name. If omitted, deletes global trigger.
**Output Parameters**:
- Result: Success message indicating the trigger was deleted.

### `DefineStatusThreshold` (`define_status_threshold`)
Define a **Status Threshold** definition for system monitoring. Sets conditions for health reporting.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- threshold_name (Required): The name of the threshold (max 48 chars).
- activity (Required): The system activity to monitor. Valid values: PROCESSSUMMARY, SESSIONSUMMARY, CLIENTSESSIONSUMMARY, SCHEDCLIENTSESSIONSUMMARY, DBUTIL, DBFREESPACE, DBUSEDSPACE, ARCHIVELOGFREESPACE, STGPOOLUTIL, STGPOOLCAPACITY, AVGSTGPOOLUTIL, TOTSTGPOOLCAPACITY, TOTSTGPOOLS, TOTRWSTGPOOLS, TOTNOTRWSTGPOOLS, STGPOOLINUSEANDDEFINED, ACTIVELOGUTIL, ARCHLOGUTIL, CPYSTGPOOLUTIL, PMRYSTGPOOLUTIL, DEVCLASSPCTDRVOFFLINE, DEVCLASSPCTDRVPOLLING, DEVCLASSPCTLIBPATHSOFFLINE, DEVCLASSPCTPATHSOFFLINE, DEVCLASSPCTDISKSUNAVAILABLE, FILEDEVCLASSPCTSCRUNALLOCATABLE.
- condition (Optional): The condition to check. Valid values: GT, GE, LT, LE, EQual, EXists. Default: EXists.
- value (Optional): The threshold value. Required for GT, GE, LT, LE, EQual conditions. Not used with EXists.
- status (Optional): The status to report when threshold is met. Valid values: Normal, Warning, Error. Default: Normal.
**Output Parameters**:
- Result: Success message indicating the threshold was defined.

### `UpdateStatusThreshold` (`update_status_threshold`)
Updates a **Status Threshold** definition for system monitoring.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- threshold_name (Required): The name of the threshold.
- activity (Optional): The activity type to monitor.
- condition (Optional): The condition type. Valid values: GT, GE, LT, LE, EQual, EXists.
**Output Parameters**:
- Result: Success message indicating the threshold was updated.

### `DeleteStatusThreshold` (`delete_status_threshold`)
Deletes a **Status Threshold** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- threshold_name (Required): The name of the threshold.
**Output Parameters**:
- Result: Success message indicating the threshold was deleted.

### `DefineStorageRule` (`define_storage_rule`)
Define a **Storage Rule** for tiering or auditing. Automates data movement between tiers.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The name of the new storage rule.
- action_type (Required): The action to perform (e.g., TIERBYGROUP).
**Output Parameters**:
- Result: Success message indicating the rule was defined.

### `UpdateStorageRule` (`update_storage_rule`)
Updates a **Storage Rule** (e.g., enable/disable).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The rule name.
- active (Optional): 'YES' or 'NO' to activate/deactivate the rule.
**Output Parameters**:
- Result: Success message indicating the rule was updated.

### `DeleteStorageRule` (`delete_storage_rule`)
Deletes a **Storage Rule**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The rule name.
**Output Parameters**:
- Result: Success message indicating the rule was deleted.

### `DefineSubRule` (`define_sub_rule`)
Define a **Subrule** for a storage rule. Adds specific targets to a parent rule.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The parent storage rule name.
- sub_rule_name (Required): The name of the subrule.
- target_name (Optional): The target entity (e.g., node group).
**Output Parameters**:
- Result: Success message indicating the subrule was defined.

### `UpdateSubRule` (`update_sub_rule`)
Updates a **Subrule** within a storage rule.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The parent rule name.
- sub_rule_name (Required): The subrule name.
- target_name (Optional): New target entity name.
**Output Parameters**:
- Result: Success message indicating the subrule was updated.

### `DeleteSubRule` (`delete_sub_rule`)
Deletes a **Subrule** from a storage rule.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The parent rule name.
- sub_rule_name (Required): The subrule name.
**Output Parameters**:
- Result: Success message indicating the subrule was deleted.

### `QueryStorageRule` (`query_storage_rule`)
Display information about storage rules (e.g., tiering rules).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Optional): Rule name.

**Output Parameters**:
- Rule Name: Name of the rule.
- Source Pool: Source container.
- Target Pool: Destination container.

### Filesystem & Virtual FS

### `DefineObjectDomain` (`define_object_domain`)
Define a policy domain for object clients (e.g., S3 clients).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The name of the new domain.
**Output Parameters**:
- Result: Success message indicating the domain was defined.

### `DefineVirtualFSMapping` (`define_virtual_fs_mapping`)
Define a **Virtual File Space Mapping**. Maps a client file space to a target server.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The client node name.
- fs_name (Required): The name of the virtual file space.
- target_server (Required): The target server where data is stored.
**Output Parameters**:
- Result: Success message indicating the mapping was defined.

### `UpdateVirtualFSMapping` (`update_virtual_fs_mapping`)
Updates a **Virtual File Space Mapping**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The client node name.
- fs_name (Required): The virtual filespace name.
- target_server (Optional): The new target server for the mapping.
**Output Parameters**:
- Result: Success message indicating the mapping was updated.

### `DeleteVirtualFSMapping` (`delete_virtual_fs_mapping`)
Deletes a **Virtual File Space Mapping**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- node_name (Required): The client node name.
- fs_name (Required): The virtual filespace name.
**Output Parameters**:
- Result: Success message indicating the mapping was deleted.

### Recovery Media

### `DefineRecoveryMedia` (`define_recovery_media`)
Define **Recovery Media** information for disaster recovery. Records details about media containing system recovery data.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- media_name (Required): The name of the recovery media (max 30 chars).
- volume_names (Optional): Comma-separated list of volume names associated with this media.
- description (Optional): Description of the media contents.
- location (Optional): Physical location of the media.
- media_type (Optional): Type of media. Valid values: BOOT, OTHER. Default: OTHER.
- product (Optional): Product name associated with the media.
- product_info (Optional): Additional product information.
**Output Parameters**:
- Result: Success message indicating the media was defined.

### `UpdateRecoveryMedia` (`update_recovery_media`)
Updates **Recovery Media** information.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- media_name (Required): The recovery media name.
- volume_names (Optional): New comma-separated list of volume names.
- description (Optional): New description.
- location (Optional): New physical location.
- media_type (Optional): New media type. Valid values: BOOT, OTHER.
- product (Optional): New product name.
- product_info (Optional): New product information.
**Output Parameters**:
- Result: Success message indicating the media was updated.

### `DeleteRecoveryMedia` (`delete_recovery_media`)
Deletes **Recovery Media** information.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- media_name (Required): The recovery media name.
**Output Parameters**:
- Result: Success message indicating the media was deleted.

### Misc & Admin Utilities

### `DefineScratchPadEntry` (`define_scratch_pad_entry`)
Define a **Scratch Pad Entry** (Administrator Note) for a specific object or purpose.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- object (Required): The name of the object to attach the note to.
- message (Required): The content of the note.
**Output Parameters**:
- Result: Success message indicating the entry was defined.

### `UpdateScratchPadEntry` (`update_scratch_pad_entry`)
Updates a **Scratch Pad** entry (administrator note).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- object (Required): The object name associated with the note.
- message (Required): The new message/description.
**Output Parameters**:
- Result: Success message indicating the entry was updated.

### `DeleteScratchPadEntry` (`delete_scratch_pad_entry`)
Deletes a **Scratch Pad** entry.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- object (Required): The object name associated with the note.
**Output Parameters**:
- Result: Success message indicating the entry was deleted.

### `QueryEventLog` (`query_event_log`)
Display messages from the server activity/audit log.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- search (Optional): Search string to filter messages.
- begintime (Optional): Start time (e.g. 08:00).
- endtime (Optional): End time (e.g. 18:00).

**Output Parameters**:
- Date/Time: When the event occurred.
- Message: The log message content.
- Severity: Level of importance (Info, Warning, Error).

### `QueryPendingCommand` (`query_pending_command`)
Display a list of administrative commands that are pending approval.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Command ID: ID to approve/reject.
- Command: The command string.
- Requestor: Who requested it.

### `QueryProfile` (`query_profile`)
Query a configuration profile subscribed to by other servers.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- profile_name (Optional): Profile name.

**Output Parameters**:
- Profile Name: Name of the profile.
- Description: Description of contents.

### `QueryUserRequest` (`query_user_request`)
Query one or more pending manual mount requests (e.g., for tape).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- request_id (Optional): Request ID.

**Output Parameters**:
- Request ID: ID of the request.
- Volume Name: Media required.
- Drive Name: Drive to load.

### `UpdateCollocationGroup` (`update_collocation_group`)
Updates a **Collocation Group** description.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Required): The group name.
- description (Optional): The new description.
**Output Parameters**:
- Result: Success message indicating the group was updated.


