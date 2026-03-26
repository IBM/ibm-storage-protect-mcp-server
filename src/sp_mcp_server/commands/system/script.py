from typing import Any, Dict
from ..base import BaseCommand

class DefineScript(BaseCommand):
    @property
    def name(self) -> str:
        return "define_script"
    
    @property
    def description(self) -> str:
        return (
            "Define an **Administrative Script** to automate server tasks.\n"
            "**Input Parameters**:\n"
            "- script_name (Required): Name of the script.\n"
            "- description (Optional): Description of what the script does.\n"
            "- line (Optional): Initial command line to add to the script.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the script was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "script_name": {"type": "string", "description": "Script name."},
                "description": {"type": "string", "description": "Description."},
                "line": {"type": "string", "description": "Initial script command line."}
            },
            "required": ["script_name"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE SCRIPT {arguments['script_name']}"
        if arguments.get("description"):
            cmd += f" DESCRIPTION=\"{arguments['description']}\""
        if arguments.get("line"):
            cmd += f" \"{arguments['line']}\""
        return self._execute_simple_query(cmd)

class UpdateScript(BaseCommand):
    @property
    def name(self) -> str:
        return "update_script"
    @property
    def description(self) -> str:
        return (
            "Updates an existing **Administrative Script**. You can change the description or append commands.\n"
            "**Input Parameters**:\n"
            "- script_name (Required): The name of the script to update.\n"
            "- description (Optional): New description for the script.\n"
            "- line (Optional): A command line to add or update in the script.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the script was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "script_name": {"type": "string", "description": "Script name."},
                "description": {"type": "string", "description": "Description."},
                "line": {"type": "string", "description": "Command line to update/append."}
            },
            "required": ["script_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE SCRIPT {arguments['script_name']}"
        if arguments.get("line"): cmd += f" \"{arguments['line']}\""
        if arguments.get("description"): cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class DeleteScript(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_script"
    @property
    def description(self) -> str:
        return (
            "Deletes an **Administrative Script**.\n"
            "**Input Parameters**:\n"
            "- script_name (Required): The name of the script to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the script was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "script_name": {"type": "string", "description": "Script name."}
            },
            "required": ["script_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SCRIPT {arguments['script_name']}")

class QueryAutomationScript(BaseCommand):
    @property
    def name(self) -> str:
        return "query_automation_script"

    @property
    def description(self) -> str:
        return (
            "Query defined automation scripts.\n\n"
            "**Input Parameters**:\n"
            "- script_name (Optional): Script name.\n\n"
            "**Output Parameters**:\n"
            "- Script Name: Name of the script.\n"
            "- Description: What the script does.\n"
            "- Lines: Number of lines in the script."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "script_name": {"type": "string", "description": "Script name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY SCRIPT"
        if arguments.get("script_name"):
             cmd += f" {arguments['script_name']}"
        return self._execute_simple_query(cmd)
