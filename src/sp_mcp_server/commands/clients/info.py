from typing import Any, Dict
from ..base import BaseCommand

class QueryActiveSession(BaseCommand):
    @property
    def name(self) -> str:
        return "query_active_session"

    @property
    def description(self) -> str:
        return (
            "Display information about currently active administrative and client sessions.\n\n"
            "**Input Parameters**:\n"
            "- session_id (Optional): Specific session ID to query.\n\n"
            "**Output Parameters**:\n"
            "- Session ID: Unique identifier for the session.\n"
            "- Client Name: Name of the connected client/admin.\n"
            "- State: Current activity state (e.g., Run, Idle).\n"
            "- Bytes Sent/Recv: Amount of data transferred.\n"
            "- Wait Time: Time spent waiting for media."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "Specific session ID to query."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY SESSION"
        if arguments.get("session_id"):
            cmd += f" {arguments['session_id']}"
        return self._execute_simple_query(cmd)

class QueryDataOccupancy(BaseCommand):
    @property
    def name(self) -> str:
        return "query_data_occupancy"

    @property
    def description(self) -> str:
        return (
            "Display statistics on where client data is stored and how much space it occupies.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name to filter.\n"
            "- backup_volume (Optional): Specific backup volume/filespace name.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The client.\n"
            "- Backup Volume Type: Specific file space or workload.\n"
            "- Storage Pool: Where the data resides.\n"
            "- Files: Number of files stored.\n"
            "- Physical Space: Space occupied (MB/GB)."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name to filter (maps to node_name)."},
                "backup_volume": {"type": "string", "description": "Specific backup volume/filespace name (maps to filespace_name)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY OCCUPANCY"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        if arguments.get("backup_volume"):
            cmd += f" {arguments['backup_volume']}"
        return self._execute_simple_query(cmd)

class QueryAuditDataOccupancy(BaseCommand):
    @property
    def name(self) -> str:
        return "query_audit_data_occupancy"

    @property
    def description(self) -> str:
        return (
            "Query calculated total storage utilization for a client for audit purposes.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name to filter.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The client.\n"
            "- Backup Data: Space used by backup data.\n"
            "- Archive Data: Space used by archive data.\n"
            "- Total Space: Total space utilized."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name (maps to node_name)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY AUDITOCCUPANCY"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        return self._execute_simple_query(cmd)

class QueryClientBackupVolume(BaseCommand):
    @property
    def name(self) -> str:
        return "query_client_backup_volume"

    @property
    def description(self) -> str:
        return (
            "Query information about client backup volumes (File Spaces). "
            "A backup volume represents a logical partition of data managed for a client (e.g., C: drive, /home, System State).\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name.\n"
            "- backup_volume (Optional): Backup volume/filespace name.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The client.\n"
            "- Backup Volume (File Space): The specific volume or mount point.\n"
            "- Capacity: Total size of the volume on the client.\n"
            "- Pct Utilized: Percentage used on the client."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name (maps to node_name)."},
                "backup_volume": {"type": "string", "description": "Backup volume name (maps to filespace_name)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY FILESPACE"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        if arguments.get("backup_volume"):
            cmd += f" {arguments['backup_volume']}"
        return self._execute_simple_query(cmd)

class QueryVirtualMountPoint(BaseCommand):
    @property
    def name(self) -> str:
        return "query_virtual_mount_point"

    @property
    def description(self) -> str:
        return (
            "Query virtual mount point mappings, which map local paths to virtual filespaces.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name.\n"
            "- virtual_path (Optional): Virtual mount point name.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The client.\n"
            "- Virtual Mount Point: Name of the virtual filespace.\n"
            "- Local Path: The physical path mapped."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name."},
                "virtual_path": {"type": "string", "description": "Virtual mount point name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY VIRTUALFSMAPPING"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        if arguments.get("virtual_path"):
            cmd += f" {arguments['virtual_path']}"
        return self._execute_simple_query(cmd)

class QueryClientDataPlacement(BaseCommand):
    @property
    def name(self) -> str:
        return "query_client_data_placement"

    @property
    def description(self) -> str:
        return (
            "Query distribution of client data across storage containers and volumes.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name.\n"
            "- storage_container (Optional): Storage container name.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The client.\n"
            "- Storage Pool: The container.\n"
            "- Volume Name: The specific volume."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name."},
                "storage_container": {"type": "string", "description": "Storage container name (stgpool)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY NODEDATA"
        if arguments.get("client_name"):
             cmd += f" {arguments['client_name']}"
        if arguments.get("storage_container"):
             cmd += f" STGPOOL={arguments['storage_container']}"
        return self._execute_simple_query(cmd)
