from typing import Any, Dict
from ..base import BaseCommand

class DefineVolume(BaseCommand):
    @property
    def name(self) -> str:
        return "define_volume"

    @property
    def description(self) -> str:
        return (
            "Defines a **Storage Unit** (known as a **Volume** in SP) within a Storage Target (Pool). Represents a specific disk, file, or tape.\n"
            "**Input Parameters**:\n"
            "- pool_name (Required): The name of the parent Storage Target.\n"
            "- volume_name (Required): Unique identifier/path for the volume.\n"
            "- access (Optional): Availability mode (e.g., 'READWRITE', 'READONLY').\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the volume was defined."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pool_name": {"type": "string", "description": "Storage pool name."},
                "volume_name": {"type": "string", "description": "Volume name."},
                "access": {
                    "type": "string",
                    "enum": ["READWRITE", "READONLY", "UNAVAILABLE", "DESTROYED", "OFFSITE"],
                    "description": "Access mode."
                }
            },
            "required": ["pool_name", "volume_name"]
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE VOLUME {arguments['pool_name']} {arguments['volume_name']}"
        if arguments.get("access"):
            cmd += f" ACCESS={arguments['access']}"
        return self._execute_simple_query(cmd)

class UpdateVolume(BaseCommand):
    @property
    def name(self) -> str:
        return "update_volume"
    @property
    def description(self) -> str:
        return (
            "Updates an existing **Storage Volume**. Can modify its access mode.\n"
            "**Input Parameters**:\n"
            "- volume_name (Required): The name of the volume to update.\n"
            "- access (Optional): The new access mode (READWRITE, READONLY, UNAVAILABLE, DESTROYED, OFFSITE).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the volume was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "volume_name": {"type": "string", "description": "Volume name."},
                "access": {"type": "string", "enum": ["READWRITE", "READONLY", "UNAVAILABLE", "DESTROYED", "OFFSITE"], "description": "Access mode."}
            },
            "required": ["volume_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE VOLUME {arguments['volume_name']}"
        if arguments.get("access"): cmd += f" ACCESS={arguments['access']}"
        return self._execute_simple_query(cmd)

class UpdateVolumeHistory(BaseCommand):
    @property
    def name(self) -> str:
        return "update_volume_history"
    @property
    def description(self) -> str:
        return (
            "Updates **Volume History** information. Can change the physical location of a volume.\n"
            "**Input Parameters**:\n"
            "- volume_name (Required): The name of the volume.\n"
            "- location (Optional): The physical location description for the volume.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the volume history was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "volume_name": {"type": "string", "description": "Volume name."},
                "location": {"type": "string", "description": "Location description."}
            },
            "required": ["volume_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE VOLHISTORY {arguments['volume_name']}"
        if arguments.get("location"): cmd += f" LOCATION=\"{arguments['location']}\""
        return self._execute_simple_query(cmd)

class DeleteVolume(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_volume"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Storage Volume**.\n"
            "**Input Parameters**:\n"
            "- volume_name (Required): The name of the volume to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the volume was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "volume_name": {"type": "string", "description": "Volume name."},
                "discard_data": {"type": "string", "enum": ["YES", "NO"], "description": "Discard data?"}
            },
            "required": ["volume_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DELETE VOLUME {arguments['volume_name']}"
        if arguments.get("discard_data"): cmd += f" DISCARDDATA={arguments['discard_data']}"
        return self._execute_simple_query(cmd)

class QueryMediaVolume(BaseCommand):
    @property
    def name(self) -> str:
        return "query_media_volume"

    @property
    def description(self) -> str:
        return (
            "Queries **Storage Units** (Volumes) within a target. Returns capacity, status, and physical location info.\n"
            "**Input Parameters**:\n"
            "- volume_name (Optional): Specific volume name.\n"
            "- container_name (Optional): Filter volumes by Storage Target (Pool).\n"
            "- status (Optional): Filter by status (e.g., 'FILLING', 'FULL', 'UNAVAILABLE').\n"
            "**Output Parameters**:\n"
            "- Volume Name: Unique path/identifier.\n"
            "- Storage Pool Name: Parent Storage Target.\n"
            "- Estimated Capacity: Total size.\n"
            "- Pct Util: Percentage filled.\n"
            "- Status: Operational status."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "volume_name": {"type": "string", "description": "Specific volume name to query."},
                "container_name": {"type": "string", "description": "Filter by storage container name (maps to pool_name)."},
                "status": {"type": "string", "description": "Filter by volume status (e.g., ONLINE, DAMAGED)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY VOLUME"
        if arguments.get("volume_name"):
            cmd += f" {arguments['volume_name']}"
        
        if arguments.get("container_name"):
            cmd += f" STGPOOL={arguments['container_name']}"
        if arguments.get("status"):
            cmd += f" STATUS={arguments['status']}"
            
        return self._execute_simple_query(cmd)

class QueryVolumeHistory(BaseCommand):
    @property
    def name(self) -> str:
        return "query_volume_history"

    @property
    def description(self) -> str:
        return (
            "Display historical records of sequential volume usage (e.g., Database Backups).\n\n"
            "**Input Parameters**:\n"
            "- type (Optional): Type of history to query (e.g., DBBACKUP, EXPORT, RPFILE).\n\n"
            "**Output Parameters**:\n"
            "- Date/Time: When the volume was written.\n"
            "- Volume Name: The name of the volume.\n"
            "- Type: Type of data (e.g., BACKUPFULL, RPFILE)."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "type": {"type": "string", "description": "Type of history to query (e.g., DBBACKUP, EXPORT, RPFILE)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY VOLHISTORY"
        if arguments.get("type"):
            cmd += f" TYPE={arguments['type']}"
        return self._execute_simple_query(cmd)

class QuerySequentialMedia(BaseCommand):
    @property
    def name(self) -> str:
        return "query_sequential_media"

    @property
    def description(self) -> str:
        return (
            "Query sequential-access media associated with a storage container.\n\n"
            "**Input Parameters**:\n"
            "- container_name (Optional): Storage container name.\n\n"
            "**Output Parameters**:\n"
            "- Volume Name: The media volume.\n"
            "- State: Mountable or not.\n"
            "- Location: Current location of the volume."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "container_name": {"type": "string", "description": "Storage container name (maps to pool name)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY MEDIA"
        if arguments.get("container_name"):
            cmd += f" {arguments['container_name']}"
        return self._execute_simple_query(cmd)

class QueryMountedVolumes(BaseCommand):
    @property
    def name(self) -> str:
        return "query_mounted_volumes"

    @property
    def description(self) -> str:
        return (
            "Display information on currently mounted sequential access volumes.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Volume Name: The mounted volume.\n"
            "- Drive Name: The drive it is mounted in.\n"
            "- Library Name: The library containing the drive."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY MOUNT")

class QueryRecoveryMedia(BaseCommand):
    @property
    def name(self) -> str:
        return "query_recovery_media"

    @property
    def description(self) -> str:
        return (
            "Query media needed for disaster recovery.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Volume Name: The media volume.\n"
            "- Storage Pool Name: The associated container."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY RECOVERYMEDIA")

class QueryRetentionMedia(BaseCommand):
    @property
    def name(self) -> str:
        return "query_retention_media"

    @property
    def description(self) -> str:
        return (
            "Query media moving between retention states (e.g., Vault to Onsite).\n\n"
            "**Input Parameters**:\n"
            "- days (Optional): Number of days matching criteria.\n\n"
            "**Output Parameters**:\n"
            "- Volume Name: The media volume.\n"
            "- State: Current retention state.\n"
            "- Location: Where the volume is."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Number of days matching criteria."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY RETMEDIA"
        if arguments.get("days"):
            cmd += f" {arguments['days']}"
        return self._execute_simple_query(cmd)

class QueryBackupTOC(BaseCommand):
    @property
    def name(self) -> str:
        return "query_backup_toc"

    @property
    def description(self) -> str:
        return (
            "Display the Table of Contents (TOC) for a backup image, listing files within it.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name.\n"
            "- backup_set_name (Optional): Backup set/File space name.\n\n"
            "**Output Parameters**:\n"
            "- File Name: Name of the file in the backup.\n"
            "- Size: Size of the file.\n"
            "- Creation Date: File creation time."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name (maps to node_name)."},
                "backup_set_name": {"type": "string", "description": "Backup set/File space name (maps to filespace)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY TOC"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        if arguments.get("backup_set_name"):
            cmd += f" {arguments['backup_set_name']}"
        return self._execute_simple_query(cmd)
