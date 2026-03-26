# IBM Storage Protect MCP - Storage Module

## Overview
The **Storage Module** manages the physical and logical storage infrastructure, including storage pools, volumes, libraries, tape drives, and device classes.

## Micro-MCP-Servers

This module consists of 3 specialized micro-mcp-servers:

### 1. `mcp-server-storage-pools`
**Focus**: Logical storage hierarchy (Pools and Volumes).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineStoragePool` | Create storage pool | `DEFINE STGPOOL` |
| `UpdateStoragePool` | Modify pool settings | `UPDATE STGPOOL` |
| `DefineVolume` | Add volume to pool | `DEFINE VOLUME` |
| `UpdateVolume` | Modify volume | `UPDATE VOLUME` |
| `QueryStorageContainer` | View container details | `QUERY CONTAINER` |

### 2. `mcp-server-storage-hardware`
**Focus**: Physical hardware management (Libraries, Drives, Paths).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineLibrary` | Define tape/disk library | `DEFINE LIBRARY` |
| `DefineDrive` | Define tape drive | `DEFINE DRIVE` |
| `DefinePath` | Define data path | `DEFINE PATH` |
| `CheckinLibVol` | Check-in tapes | `CHECKIN LIBVOL` |
| `QueryTapeLibrary` | View library statuses | `QUERY LIBRARY` |

### 3. `mcp-server-storage-device`
**Focus**: Device classes and data movers (Tiering configuration).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineDeviceClass` | Create device class | `DEFINE DEVCLASS` |
| `DefineDataMover` | Configure data mover | `DEFINE DATAMOVER` |
| `MigrateStorageTarget` | Migrate target | `MIGRATE STGPOOL` (target) |

## Usage

### Running as Micro-MCP-Servers (Recommended for Context Optimization)

```bash
# Terminal 1: Manage Pools
mcp-server-storage-pools

# Terminal 2: Manage Hardware
mcp-server-storage-hardware
```

### Running as Unified Module
You can run all storage-related micro-mcp-servers together:

```bash
python -m sp_mcp_server.main --enable-servers storage
```
