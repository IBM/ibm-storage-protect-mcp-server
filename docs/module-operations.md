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
