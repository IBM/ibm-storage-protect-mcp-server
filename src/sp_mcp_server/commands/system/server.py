from typing import Any, Dict
from ..base import BaseCommand

# --- SERVER COMMANDS ---

class DefineServer(BaseCommand):
    @property
    def name(self) -> str:
        return "define_server"
    
    @property
    def description(self) -> str:
        return (
            "Define a **Server** for server-to-server communications (e.g., replication, library sharing).\n"
            "**Input Parameters**:\n"
            "- server_name (Required): Name of the server.\n"
            "- password (Required): Password for authentication.\n"
            "- hl_address (Required): High level address (IP address or DNS name).\n"
            "- ll_address (Required): Low level address (TCP Port).\n"
            "- description (Optional): Description.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the server was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "Server name."},
                "password": {"type": "string", "description": "Password."},
                "hl_address": {"type": "string", "description": "High level address."},
                "ll_address": {"type": "string", "description": "Low level address."},
                "description": {"type": "string", "description": "Description."}
            },
            "required": ["server_name", "password", "hl_address", "ll_address"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = (f"DEFINE SERVER {arguments['server_name']} PASSWORD={arguments['password']} "
               f"HLADDRESS={arguments['hl_address']} LLADDRESS={arguments['ll_address']}")
        if arguments.get("description"):
             cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class DefineServerGroup(BaseCommand):
    @property
    def name(self) -> str:
        return "define_server_group"
    
    @property
    def description(self) -> str:
        return (
            "Define a **Server Group** to manage multiple servers as a single unit.\n"
            "**Input Parameters**:\n"
            "- group_name (Required): The name of the new server group.\n"
            "- description (Optional): Description of the group.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the server group was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Server group name."},
                "description": {"type": "string", "description": "Description."}
            },
            "required": ["group_name"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE SERVERGROUP {arguments['group_name']}"
        if arguments.get("description"):
            cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class DefineGroupMember(BaseCommand):
    @property
    def name(self) -> str:
        return "define_group_member"
    @property
    def description(self) -> str:
        return (
            "Add a **Server** to a **Server Group**.\n"
            "**Input Parameters**:\n"
            "- group_name (Required): The name of the server group.\n"
            "- server_name (Required): The name of the server to add.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the server was added to the group."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group name."},
                "server_name": {"type": "string", "description": "Server name to add."}
            },
            "required": ["group_name", "server_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DEFINE GRPMEMBER {arguments['group_name']} {arguments['server_name']}")

class DefineEventServer(BaseCommand):
    @property
    def name(self) -> str:
        return "define_event_server"
    @property
    def description(self) -> str:
        return (
            "Define a server as the **Event Server** (target for logging events).\n"
            "**Input Parameters**:\n"
            "- server_name (Required): The name of the server to receive events.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the event server was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "Server name."}
            },
            "required": ["server_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DEFINE EVENTSERVER {arguments['server_name']}")

class UpdateServer(BaseCommand):
    @property
    def name(self) -> str:
        return "update_server"
    @property
    def description(self) -> str:
        return (
            "Updates the properties of an existing **Server** definition used for server-to-server communications.\n"
            "**Input Parameters**:\n"
            "- server_name (Required): The name of the server to update.\n"
            "- password (Optional): Update the password.\n"
            "- hl_address (Optional): Update the High Level Address (IP/Hostname).\n"
            "- ll_address (Optional): Update the Low Level Address (Port).\n"
            "- description (Optional): Update the description.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the server was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "Server name."},
                "password": {"type": "string", "description": "Password."},
                "hl_address": {"type": "string", "description": "High level address."},
                "ll_address": {"type": "string", "description": "Low level address."},
                "description": {"type": "string", "description": "Description."}
            },
            "required": ["server_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE SERVER {arguments['server_name']}"
        if arguments.get("password"): cmd += f" PASSWORD={arguments['password']}"
        if arguments.get("hl_address"): cmd += f" HLADDRESS={arguments['hl_address']}"
        if arguments.get("ll_address"): cmd += f" LLADDRESS={arguments['ll_address']}"
        if arguments.get("description"): cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class UpdateServerGroup(BaseCommand):
    @property
    def name(self) -> str:
        return "update_server_group"
    @property
    def description(self) -> str:
        return (
            "Updates the description of an existing **Server Group**.\n"
            "**Input Parameters**:\n"
            "- group_name (Required): The name of the server group.\n"
            "- description (Optional): The new description for the group.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the group was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group name."},
                "description": {"type": "string", "description": "Description."}
            },
            "required": ["group_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE SERVERGROUP {arguments['group_name']}"
        if arguments.get("description"): cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class DeleteServer(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_server"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Server** definition. This removes the configuration for server-to-server communication.\n"
            "**Input Parameters**:\n"
            "- server_name (Required): The name of the server to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the server was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "Server name."}
            },
            "required": ["server_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SERVER {arguments['server_name']}")

class DeleteServerGroup(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_server_group"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Server Group**. This removes the grouping but does not delete the member servers themselves.\n"
            "**Input Parameters**:\n"
            "- group_name (Required): The name of the server group to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the group was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group name."}
            },
            "required": ["group_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SERVERGROUP {arguments['group_name']}")

class DeleteGroupMember(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_group_member"
    @property
    def description(self) -> str:
        return (
            "Removes a **Server** from a **Server Group**.\n"
            "**Input Parameters**:\n"
            "- group_name (Required): The name of the server group.\n"
            "- server_name (Required): The name of the server to remove.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the member was removed."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group name."},
                "server_name": {"type": "string", "description": "Server name."}
            },
            "required": ["group_name", "server_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE GRPMEMBER {arguments['group_name']} {arguments['server_name']}")

class DeleteEventServer(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_event_server"
    @property
    def description(self) -> str:
        return (
            "Deletes an **Event Server** definition.\n"
            "**Input Parameters**:\n"
            "- server_name (Required): The name of the event server to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the event server was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "Server name."}
            },
            "required": ["server_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE EVENTSERVER {arguments['server_name']}")

class QueryServerStatus(BaseCommand):
    @property
    def name(self) -> str:
        return "query_server_status"

    @property
    def description(self) -> str:
        return (
            "Display the general health and status of the backup server.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Server Name: The name of the backup server.\n"
            "- Server Date/Time: Current date and time on the server.\n"
            "- Server Version: The software version of the server.\n"
            "- Server License Compliance: The license audit result (PASSED/FAILED). "
            "This reflects the last license audit status, NOT database backup health. "
            "The Last License Audit timestamp accompanies this field.\n"
            "- Activity Log Retention: How long event logs are kept.\n"
            "- Password Expiration: Settings for password usage.\n\n"
            "**IMPORTANT NOTE**: Database backup status is NOT reported by QUERY STATUS. "
            "To check database backup history, use the query_volume_history tool with TYPE=DBBACKUP, "
            "or search activity logs for database backup messages (ANR2968E for failures)."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY STATUS")

class QueryServerOption(BaseCommand):
    @property
    def name(self) -> str:
        return "query_server_option"

    @property
    def description(self) -> str:
        return (
            "Display global server configuration options.\n\n"
            "**Usage Guide**:\n"
            "- Call without arguments to list ALL options and their current values.\n"
            "- Call with `option_name` to query a specific option.\n"
            "- Supports wildcards (e.g., `LOG*`).\n\n"
            "**Common Options by Category**:\n"
            "- **Communication**: TCPPORT, MAXSESSIONS, IDLETIMEOUT, COMMMETHOD, COMMTIMEOUT, MINJOBS, MAXJOBS.\n"
            "- **Logging**: ACTIVELOGDIRECTORY, ACTIVELOGSIZE, ARCHLOGDIRECTORY, MIRRORLOGDIRECTORY, ACTLOGRETENTION.\n"
            "- **Security**: PASSWORDLIFE, FIPSMODE, LDAPURL, ADMINONCLIENTPORT, REGAUTH.\n"
            "- **Database**: DBMEMPERCENT, ARCHLOGUSEDTHRESHOLD, BUFFPOOLSIZE.\n"
            "- **Storage/Cloud**: EXPINTERVAL, MOVEBATCHSIZE, MOVESIZETHRESH, RECLAIM, DEDUPREQUIRESBACKUP.\n"
            "- **Integrity**: AUDITSTORAGE, CRCVALIDATE, CHECKTAPEPOS.\n\n"
            "**Input Parameters**:\n"
            "- option_name (Optional): Specific option to query (e.g., 'MAXSESSIONS').\n\n"
            "**Output Parameters**:\n"
            "- Option: Name of the setting.\n"
            "- Setting: Current value."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "option_name": {"type": "string", "description": "Specific option to query."}
            },
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY OPTION"
        if arguments.get("option_name"):
            cmd += f" {arguments['option_name']}"
        return self._execute_simple_query(cmd)
