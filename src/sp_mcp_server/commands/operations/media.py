from typing import Any, Dict
from ..base import BaseCommand

class DefineRecoveryMedia(BaseCommand):
    @property
    def name(self) -> str:
        return "define_recovery_media"
    @property
    def description(self) -> str:
        return (
            "Define **Recovery Media** information about a source server's database backup volume.\n"
            "**Input Parameters**:\n"
            "- source_server (Required): The name of the source server.\n"
            "- volume_name (Required): The volume name containing the backup.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the media was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source_server": {"type": "string", "description": "Source server name."},
                "volume_name": {"type": "string", "description": "Volume name."}
            },
            "required": ["source_server", "volume_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DEFINE RECOVERYMEDIA {arguments['source_server']} {arguments['volume_name']}")

class UpdateRecoveryMedia(BaseCommand):
    @property
    def name(self) -> str:
        return "update_recovery_media"
    @property
    def description(self) -> str:
        return (
            "Updates the location of **Recovery Media**.\n"
            "**Input Parameters**:\n"
            "- source_server (Required): The source server.\n"
            "- volume_name (Required): The volume name.\n"
            "- location (Required): The new physical location description.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the media was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source_server": {"type": "string", "description": "Source server."},
                "volume_name": {"type": "string", "description": "Volume name."},
                "location": {"type": "string", "description": "New location."}
            },
            "required": ["source_server", "volume_name", "location"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"UPDATE RECOVERYMEDIA {arguments['source_server']} {arguments['volume_name']} LOCATION=\"{arguments['location']}\"")

class DeleteRecoveryMedia(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_recovery_media"
    @property
    def description(self) -> str:
        return (
            "Deletes **Recovery Media** information.\n"
            "**Input Parameters**:\n"
            "- source_server (Required): The source server.\n"
            "- volume_name (Required): The volume name.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the media was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source_server": {"type": "string", "description": "Source server."},
                "volume_name": {"type": "string", "description": "Volume name."}
            },
            "required": ["source_server", "volume_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE RECOVERYMEDIA {arguments['source_server']} {arguments['volume_name']}")
