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

## Detailed Tools Reference
### Storage Pools & Containers

`DefineStoragePool` (`define_storage_pool`)
- Description: Defines a new **Storage Pool** (also referred to as a Container for certain pool types). This is a named resource consisting of multiple storage units (volumes) where backup data is stored.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): Name for the new Storage Pool.
- device_class_name (Required): The **Device Class** determining the hardware type (e.g., LTO, DISK).
- pool_type (Optional): The function of the pool ('PRIMARY', 'COPY', 'ACTIVE', 'CONTAINER').
- description (Optional): Description of the target.
- max_scratch (Optional): Maximum number of scratch volumes allowed.
- reclaim (Optional): Threshold percentage to trigger space reclamation.
- collocate (Optional): Collocation setting to group data (e.g., by Node or Group).
**Output Parameters**:
- Result: Success message indicating the Storage Pool was defined.

`DefineStoragePoolDirectory` (`define_storage_pool_directory`)
- Description: Adds a filesystem directory to a **Container Storage Pool** (Storage Pool Directory) for deduplicated data storage.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): The name of the Container Storage Pool.
- directory (Required): The absolute filesystem path to add.
**Output Parameters**:
- Result: Success message indicating the directory was added.

`UpdateStorageTarget` (`update_storage_target`)
- Description: Update a Storage Pool configuration. A storage pool is a named set of volumes used to store data.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- target_name (Required): Name of the storage pool to update.
- description (Optional): New description for the pool.
- max_scratch (Optional): Maximum number of scratch volumes allowed.
- reclaim_threshold (Optional): Threshold percentage for space reclamation (0-100).
- access_mode (Optional): One of 'READWRITE', 'READONLY', 'UNAVAILABLE', etc.
**Output Parameters**:
- Result: Success message indicating the pool was updated.

`UpdateStoragePool` (`update_storage_pool`)
- Description: Update a storage pool.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): Name of the storage pool to update.
- description (Optional): New description.
- max_scratch (Optional): New max scratch limit.
- reclaim (Optional): New reclamation threshold.
- accession (Optional): New access mode (READWRITE, READONLY, UNAVAILABLE, etc.).

`DeleteStorageTarget` (`delete_storage_target`)
- Description: Removes a Storage Pool. This deletes the pool definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- target_name (Required): Name of the storage pool to delete.
**Output Parameters**:
- Result: Success message indicating the pool was deleted.

`DeleteStoragePool` (`delete_storage_pool`)
- Description: Deletes a **Storage Pool**. Ensure the pool is empty before deleting.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): The name of the storage pool to delete.
**Output Parameters**:
- Result: Success message indicating the pool was deleted.

`QueryStorageContainer` (`query_storage_container`)
- Description: Detailed query for **Storage Pools** (Containers). Returns configuration, usage, and status.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- container_name (Optional): Specific Storage Pool name to query. If omitted, lists all.
- format (Optional): 'standard' or 'detailed' view.
**Output Parameters**:
- Storage Pool Name: Unique identifier.
- Device Class Name: underlying hardware type.
- Estimated Capacity: Total storage available.
- Pct Utilized: Percentage of space used.
- Pct Migrated: Data migrated to secondary tier.

`QueryContainerDirectory` (`query_container_directory`)
- Description: Query directories used for storage by directory-container storage pools.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- container_name (Optional): Storage container name.

**Output Parameters**:
- Storage Pool Name: The container using the directory.
- Directory: The file system path.
- Access: Current access mode (Read/Write).

### Volumes, Libraries and Drives

`DefineVolume` (`define_volume`)
- Description: Defines a **Storage Unit** (known as a **Volume** in SP) within a Storage Pool. Represents a specific disk, file, or tape.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- pool_name (Required): The name of the parent Storage Pool.
- volume_name (Required): Unique identifier/path for the volume.
- access (Optional): Availability mode (e.g., 'READWRITE', 'READONLY').
**Output Parameters**:
- Result: Success message indicating the volume was defined.

`UpdateVolume` (`update_volume`)
- Description: Updates an existing **Storage Volume**. Can modify its access mode.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- volume_name (Required): The name of the volume to update.
- access (Optional): The new access mode (READWRITE, READONLY, UNAVAILABLE, DESTROYED, OFFSITE).
**Output Parameters**:
- Result: Success message indicating the volume was updated.

`UpdateVolumeHistory` (`update_volume_history`)
- Description: Updates **Volume History** information. Can change the physical location of a volume.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- volume_name (Required): The name of the volume.
- location (Optional): The physical location description for the volume.
**Output Parameters**:
- Result: Success message indicating the volume history was updated.

`DeleteVolume` (`delete_volume`)
- Description: Deletes a **Storage Volume**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- volume_name (Required): The name of the volume to delete.
**Output Parameters**:
- Result: Success message indicating the volume was deleted.

`QueryMediaVolume` (`query_media_volume`)
- Description: Queries **Storage Units** (Volumes) within a target. Returns capacity, status, and physical location info.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- volume_name (Optional): Specific volume name.
- container_name (Optional): Filter volumes by Storage Pool.
- status (Optional): Filter by status (e.g., 'FILLING', 'FULL', 'UNAVAILABLE').
**Output Parameters**:
- Volume Name: Unique path/identifier.
- Storage Pool Name: Parent Storage Pool.
- Estimated Capacity: Total size.
- Pct Util: Percentage filled.
- Status: Operational status.

`QueryVolumeHistory` (`query_volume_history`)
- Description: Display historical records of sequential volume usage (e.g., Database Backups).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- type (Optional): Type of history to query (e.g., DBBACKUP, EXPORT, RPFILE).
**Output Parameters**:
- Date/Time: When the volume was written.
- Volume Name: The name of the volume.
- Type: Type of data (e.g., BACKUPFULL, RPFILE).

`QuerySequentialMedia` (`query_sequential_media`)
- Description: Query sequential-access media associated with a storage container.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- container_name (Optional): Storage container name.
**Output Parameters**:
- Volume Name: The media volume.
- State: Mountable or not.
- Location: Current location of the volume.

`QueryMountedVolumes` (`query_mounted_volumes`)
- Description: Display information on currently mounted sequential access volumes.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
**Output Parameters**:
- Volume Name: The mounted volume.
- Drive Name: The drive it is mounted in.
- Library Name: The library containing the drive.

`QueryRecoveryMedia` (`query_recovery_media`)
- Description: Query media needed for disaster recovery.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
**Output Parameters**:
- Volume Name: The media volume.
- Storage Pool Name: The associated container.

`QueryRetentionMedia` (`query_retention_media`)
- Description: Query media moving between retention states (e.g., Vault to Onsite).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- days (Optional): Number of days matching criteria.
**Output Parameters**:
- Volume Name: The media volume.
- State: Current retention state.
- Location: Where the volume is.

`QueryBackupTOC` (`query_backup_toc`)
- Description: Display the Table of Contents (TOC) for a backup image, listing files within it.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- client_name (Optional): Node name.
- backup_set_name (Optional): Backup set/File space name.
**Output Parameters**:
- File Name: Name of the file in the backup.
- Size: Size of the file.
- Creation Date: File creation time.

### Libraries, Drives and Alerts

`DefineLibrary` (`define_library`)
- Description: Defines a **Tape Library** configuration physically or logically connected to the server.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Required): Unique name for the library.
- lib_type (Required): The interface type (e.g., 'SCSI', 'VTL', 'SHARED').
- shared (Optional): 'YES' if the library is shared via SAN, 'NO' otherwise.
**Output Parameters**:
- Result: Success message indicating the library was defined.

`UpdateLibrary` (`update_library`)
- Description: Updates a **Library** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Required): The name of the library.
- shared (Optional): 'YES' or 'NO' to indicate if shared.
**Output Parameters**:
- Result: Success message indicating the library was updated.

`DeleteLibrary` (`delete_library`)
- Description: Deletes a **Library** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Required): The name of the library to delete.
**Output Parameters**:
- Result: Success message indicating the library was deleted.

`QueryTapeLibrary` (`query_tape_library`)
- Description: Display information about tape libraries defined in the system.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Optional): Name of the library.
**Output Parameters**:
- Library Name: Name of the library.
- Library Type: Type of library (e.g., SCSI, SHARED).
- Device: Device identifier.

`QueryLibraryVolume` (`query_library_volume`)
- Description: Query specific volumes physically located within a tape library.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Optional): Library name.
- volume_name (Optional): Volume name.

**Output Parameters**:
- Library Name: Name of the library.
- Volume Name: Name of the volume.
- Status: Current status (e.g., Private, Scratch).
- Owner: Owner of the volume (for private volumes).

`DefineDrive` (`define_drive`)
- Description: Defines a **Tape Drive** within a specific Tape Library.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Required): The name of the parent Library.
- drive_name (Required): Unique name for the drive.
- serial (Optional): Hardware serial number (use 'AUTODETECT' to auto-discover).
- element (Optional): Element address in the library (use 'AUTODETECT' to auto-discover).
**Output Parameters**:
- Result: Success message indicating the drive was defined.

`UpdateDrive` (`update_drive`)
- Description: Updates a **Drive** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Required): The library name containing the drive.
- drive_name (Required): The drive name.
- online (Optional): 'YES' or 'NO' to bring online/offline.
**Output Parameters**:
- Result: Success message indicating the drive was updated.

`DeleteDrive` (`delete_drive`)
- Description: Deletes a **Drive** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Required): The library containing the drive.
- drive_name (Required): The name of the drive to delete.
**Output Parameters**:
- Result: Success message indicating the drive was deleted.

`QueryTapeDrive` (`query_tape_drive`)
- Description: Display information about tape drives associated with a library.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- library_name (Optional): The library name.
- drive_name (Optional): The drive name.
**Output Parameters**:
- Library Name: The library the drive belongs to.
- Drive Name: Name of the drive.
- Device Type: Type of drive device.
- Online: Whether the drive is online and available.

`QueryTapeAlerts` (`query_tape_alerts`)
- Description: Display settings and status for tape drive alerts.

`QuerySanDevices` (`query_san_devices`)
- Description: Query storage devices detected on the Storage Area Network (SAN).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.
**Output Parameters**:
- Device Name: Name of the device.
- Serial Number: Hardware serial number.

`QueryStorageTarget` (`query_storage_target`)
- Description: No implementation for `QueryStorageTarget` was found in the source tree; therefore no verbatim description is available in-code.

### Paths and Device Classes

`DefinePath` (`define_path`)
- Description: Defines a **Data Path** allowing communication between a source and destination.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- source_name (Required): Name of the source (e.g., Server Name).
- destination_name (Required): Name of the destination (e.g., Drive Name).
- source_type (Required): Type of source system ('SERVER', 'DATAMOVER').
- destination_type (Required): Type of destination hardware ('LIBRARY', 'DRIVE').
- library_name (Optional): Name of the library (required if destination is a Drive).
- device (Required): OS-level device path (e.g., /dev/rmt0).
**Output Parameters**:
- Result: Success message indicating the path was defined.

`UpdateDataPath` / `UpdatePath` (`update_data_path`, `update_path`)
- Description: Update the data path between a source (like a server or data mover) and a destination (drive, library) to allow data transfer.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- source_name (Required): Name of the source (e.g., server name).
- destination_name (Required): Name of the destination (e.g., drive name).
- source_type (Required): Type of source (e.g., SERVER, DATAMOVER).
- destination_type (Required): Type of destination (e.g., DRIVE, LIBRARY).
- library (Optional): Name of the library (required for drive paths).
- online (Optional): 'Yes' or 'No' to set path availability.
**Output Parameters**:
- Result: Success message indicating the path was updated.

`DeletePath` (`delete_path`)
- Description: Deletes a **Path** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- source_name (Required): Source name.
- destination_name (Required): Destination name.
- source_type (Required): Source type.
- destination_type (Required): Destination type.
**Output Parameters**:
- Result: Success message indicating the path was deleted.

`QueryDataPath` (`query_data_path`)
- Description: Display information about data paths between source and destination.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- source_name (Optional): Name of the source component.
- destination_name (Optional): Name of the destination component.
**Output Parameters**:
- Source Name: The source of the path (e.g., Server Name).
- Source Type: Type of source (e.g., SERVER).
- Destination Name: The destination (e.g., Drive or Library).
- Destination Type: Type of destination.
- Device: The device path.

### Device Classes and Data Movers

`DefineDeviceClass` (`define_device_class`)
- Description: Defines a **Device Class** in SP. Specifies the hardware type and management policies for storage devices.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- device_class_name (Required): Name for the Device Class.
- dev_type (Required): The underlying technology (e.g., 'LTO', 'DISK', 'FILE').
- library (Optional): The library associated with this device type (required for tape).
- mount_limit (Optional): Maximum concurrent drives/volumes that can be mounted.
**Output Parameters**:
- Result: Success message indicating the device class was defined.

`UpdateDeviceClass` (`update_device_class`)
- Description: Updates a **Device Class** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- devclass_name (Required): The device class name.
- mount_limit (Optional): Max number of mounts allowed (DRIVES or number).
**Output Parameters**:
- Result: Success message indicating the device class was updated.

`DeleteDeviceClass` (`delete_device_class`)
- Description: Deletes a **Device Class** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- devclass_name (Required): The name of the device class to delete.
**Output Parameters**:
- Result: Success message indicating the device class was deleted.

`QueryDeviceType` (`query_device_type`)
- Description: Display information about device types (Device Classes) used for storage.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- device_type_name (Optional): Name of the device class.
**Output Parameters**:
- Device Class Name: Name of the device class.
- Device Access Strategy: Sequential or Random (Disk).
- Storage Type: Underlying storage medium.

`DefineDataMover` (`define_data_mover`)
- Description: Defines a **Data Mover** in SP. Used for operations like NDMP backups (NAS).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- name (Required): Unique name for the Data Mover.
- type (Required): The protocol type (e.g., 'NAS').
- hl_address (Required): High-level address (IP address or DNS name).
- ll_address (Required): Low-level address (TCP Port).
- user_id (Required): Username for authentication.
- password (Required): Password for authentication.
**Output Parameters**:
- Result: Success message indicating the Data Mover was defined.

`UpdateDataMover` (`update_data_mover`)
- Description: Updates a **Data Mover** configuration.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- mover_name (Required): The data mover name.
- type (Optional): The new type (e.g., NAS).
- user_id (Optional): The user ID for authentication.
- password (Optional): The password for authentication.
**Output Parameters**:
- Result: Success message indicating the data mover was updated.

`DeleteDataMover` (`delete_data_mover`)
- Description: Deletes a **Data Mover** definition.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- mover_name (Required): The name of the data mover to delete.
**Output Parameters**:
- Result: Success message indicating the data mover was deleted.

`QueryDataMover` (`query_data_mover`)
- Description: Display definitions for data movers (e.g., for NAS backup).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- name (Optional): Data mover name.
**Output Parameters**:
- Data Mover Name: Name of the mover.
- Type: Type of mover (e.g., NAS).
- IP Address: Network address.

### Miscellaneous Queries

`QueryDamagedData` (`query_damaged_data`)
- Description: Query data marked as damaged within storage containers.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- container_name (Optional): Storage container name to check.

**Output Parameters**:
- Storage Pool Name: The container.
- Object ID: ID of the damaged object.
- Type: Type of damage.

`QueryContainerCleanup` (`query_container_cleanup`)
- Description: Query the cleanup process status for source storage containers.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Storage Pool Name: The container.
- Phase: Cleanup phase.
- Status: Current status.

`QueryContainerConversion` (`query_container_conversion`)
- Description: Query the status of storage container conversion (e.g., changing format).

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Process: The conversion process info.
- Status: Status of conversion.

`QueryDeduplicationStats` (`query_deduplication_stats`)
- Description: Query statistics related to data deduplication savings in storage containers.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- container_name (Optional): Storage container name.

**Output Parameters**:
- Storage Pool Name: The container.
- Total Data Protected: Logical amount of data.
- Total Space Used: Physical space used.
- Deduplication Ratio: Efficiency ratio.

`QueryExtentUpdates` (`query_extent_updates`)
- Description: Query information about updated data extents in the system.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Extent ID: Identifier for the data chunk.
- Status: Status of the update.

`QueryShreddingStatus` (`query_shredding_status`)
- Description: Query the status of secure data shredding operations.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- None.

**Output Parameters**:
- Shredding Active: Yes/No.
- Passes: Number of overwrite passes.

`QueryTargetServer` (`query_target_server`)
- Description: Query the definitions of other backup servers known to this system.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- server_name (Optional): Name of the target server.

**Output Parameters**:
- Server Name: Name of the remote server.
- Server Address: Network address.
- Server Password Set: Indicates if a password is set.

`QueryServerGroup` (`query_server_group`)
- Description: Query server groups, which are collections of servers managed together.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- group_name (Optional): Name of the server group.

**Output Parameters**:
- Group Name: Name of the group.
- Member Server: Servers belonging to the group.


