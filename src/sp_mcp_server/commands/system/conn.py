from typing import Any, Dict
from ..base import BaseCommand

class DefineConnection(BaseCommand):
    @property
    def name(self) -> str:
        return "define_connection"
    
    @property
    def description(self) -> str:
        return (
            "Define a **Cloud Connection** to a cloud service (e.g., S3, Azure).\n"
            "**Input Parameters**:\n"
            "- connection_name (Required): Name of the connection.\n"
            "- cloud_type (Required): Type of cloud (S3, AZURE, GOOGLE, etc).\n"
            "- bucket_name (Required): Target bucket name.\n"
            "- identity (Required): User ID or Access Key ID.\n"
            "- password (Required): Password or Secret Key.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the connection was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "connection_name": {"type": "string", "description": "Connection name."},
                "cloud_type": {"type": "string", "description": "Cloud type (e.g. S3)."},
                "bucket_name": {"type": "string", "description": "Bucket name."},
                "identity": {"type": "string", "description": "Identity."},
                "password": {"type": "string", "description": "Password."}
            },
            "required": ["connection_name", "cloud_type", "bucket_name", "identity", "password"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = (f"DEFINE CONNECTION {arguments['connection_name']} CLOUDTYPE={arguments['cloud_type']} "
               f"BUCKETNAME={arguments['bucket_name']} IDENTITY=\"{arguments['identity']}\" "
               f"PASSWORD=\"{arguments['password']}\"")
        return self._execute_simple_query(cmd)

class UpdateConnection(BaseCommand):
    @property
    def name(self) -> str:
        return "update_connection"
    @property
    def description(self) -> str:
        return (
            "Updates a **Cloud Connection** configuration (typically password/key).\n"
            "**Input Parameters**:\n"
            "- connection_name (Required): The name of the connection.\n"
            "- password (Optional): The new password or key for the cloud connection.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the connection was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "connection_name": {"type": "string", "description": "Connection name."},
                "password": {"type": "string", "description": "New password."}
            },
            "required": ["connection_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE CONNECTION {arguments['connection_name']}"
        if arguments.get("password"): cmd += f" PASSWORD=\"{arguments['password']}\""
        return self._execute_simple_query(cmd)

class DeleteConnection(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_connection"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Cloud Connection** definition.\n"
            "**Input Parameters**:\n"
            "- connection_name (Required): The name of the connection to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the connection was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "connection_name": {"type": "string", "description": "Connection name."}
            },
            "required": ["connection_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE CONNECTION {arguments['connection_name']}")
