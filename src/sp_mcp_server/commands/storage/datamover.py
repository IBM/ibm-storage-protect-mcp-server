from typing import Any, Dict
from ..base import BaseCommand

class DefineDataMover(BaseCommand):
    @property
    def name(self) -> str:
        return "define_data_mover"
        
    @property
    def description(self) -> str:
        return (
            "- Description: Defines a **Data Mover** in SP. Used for operations like NDMP backups (NAS).\n"
            "**Input Parameters**:\n"
            "- name (Required): Unique name for the Data Mover.\n"
            "- type (Required): The protocol type (e.g., 'NAS').\n"
            "- hl_address (Required): High-level address (IP address or DNS name).\n"
            "- ll_address (Required): Low-level address (TCP Port).\n"
            "- data_format (Required): Data format (e.g., 'NETAPPDUMP', 'NDMP').\n"
            "- user_id (Required): Username for authentication.\n"
            "- password (Required): Password for authentication.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the Data Mover was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Data mover name."},
                "type": {"type": "string", "description": "Mover type.", "enum": ["NAS", "NASCLUSTER", "TETRA"]},
                "hl_address": {"type": "string", "description": "IP address."},
                "ll_address": {"type": "string", "description": "Port number."},
                "data_format": {"type": "string", "description": "Data format.", "enum": ["NETAPPDUMP", "NDMP"]},
                "user_id": {"type": "string", "description": "User ID."},
                "password": {"type": "string", "description": "Password."}
            },
            "required": ["name", "type", "hl_address", "ll_address", "data_format", "user_id", "password"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = (f"DEFINE DATAMOVER {arguments['name']} TYPE={arguments['type']} "
               f"HLADDRESS={arguments['hl_address']} LLADDRESS={arguments['ll_address']} "
               f"DATAFORMAT={arguments['data_format']} "
               f"USERID={arguments['user_id']} PASSWORD=\"{arguments['password']}\"")
        return self._execute_simple_query(cmd)

class UpdateDataMover(BaseCommand):
    @property
    def name(self) -> str:
        return "update_data_mover"
    @property
    def description(self) -> str:
        return (
            "- Description: Updates a **Data Mover** configuration.\n"
            "**Input Parameters**:\n"
            "- isp_server_name (Optional): Target ISP Server name from registry.\n"
            "- mover_name (Required): The data mover name.\n"
            "- type (Optional): The new type (e.g., NAS).\n"
            "- user_id (Optional): The user ID for authentication.\n"
            "- password (Optional): The password for authentication.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the data mover was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Data mover name."},
                "hl_address": {"type": "string", "description": "High level address."},
                "ll_address": {"type": "string", "description": "Low level address."},
                "user_id": {"type": "string", "description": "User ID."},
                "password": {"type": "string", "description": "Password."}
            },
            "required": ["name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE DATAMOVER {arguments['name']}"
        if arguments.get("hl_address"): cmd += f" HLADDRESS={arguments['hl_address']}"
        if arguments.get("ll_address"): cmd += f" LLADDRESS={arguments['ll_address']}"
        if arguments.get("user_id"): cmd += f" USERID={arguments['user_id']}"
        if arguments.get("password"): cmd += f" PASSWORD=\"{arguments['password']}\""
        return self._execute_simple_query(cmd)

class DeleteDataMover(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_data_mover"
    @property
    def description(self) -> str:
        return (
            "- Description: Deletes a **Data Mover** definition.\n"
            "**Input Parameters**:\n"
            "- isp_server_name (Optional): Target ISP Server name from registry.\n"
            "- mover_name (Required): The name of the data mover to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the data mover was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Mover name."}
            },
            "required": ["name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE DATAMOVER {arguments['name']}")

class QueryDataMover(BaseCommand):
    @property
    def name(self) -> str:
        return "query_data_mover"

    @property
    def description(self) -> str:
        return (
            "- Description: Display definitions for data movers (e.g., for NAS backup).\n"
            "**Input Parameters**:\n"
            "- isp_server_name (Optional): Target ISP Server name from registry.\n"
            "- name (Optional): Data mover name.\n"
            "**Output Parameters**:\n"
            "- Data Mover Name: Name of the mover.\n"
            "- Type: Type of mover (e.g., NAS).\n"
            "- IP Address: Network address."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Data mover name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY DATAMOVER"
        if arguments.get("name"):
            cmd += f" {arguments['name']}"
        return self._execute_simple_query(cmd)
