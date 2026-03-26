from typing import Any, Dict
from ..base import BaseCommand

class DefineScratchPadEntry(BaseCommand):
    @property
    def name(self) -> str:
        return "define_scratch_pad_entry"
    @property
    def description(self) -> str:
        return (
            "Define a **Scratch Pad Entry** (Administrator Note) for a specific object or purpose.\n"
            "**Input Parameters**:\n"
            "- object (Required): The name of the object to attach the note to.\n"
            "- message (Required): The content of the note.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the entry was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "object": {"type": "string", "description": "Object name."},
                "message": {"type": "string", "description": "Message text."}
            },
            "required": ["object", "message"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DEFINE SCRATCHPADENTRY {arguments['object']} DESCRIPTION=\"{arguments['message']}\"")

class UpdateScratchPadEntry(BaseCommand):
    @property
    def name(self) -> str:
        return "update_scratch_pad_entry"
    @property
    def description(self) -> str:
        return (
            "Updates a **Scratch Pad** entry (administrator note).\n"
            "**Input Parameters**:\n"
            "- object (Required): The object name associated with the note.\n"
            "- message (Required): The new message/description.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the entry was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "object": {"type": "string", "description": "Object name."},
                "message": {"type": "string", "description": "New message."}
            },
            "required": ["object", "message"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
         return self._execute_simple_query(f"UPDATE SCRATCHPADENTRY {arguments['object']} DESCRIPTION=\"{arguments['message']}\"")

class DeleteScratchPadEntry(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_scratch_pad_entry"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Scratch Pad** entry.\n"
            "**Input Parameters**:\n"
            "- object (Required): The object name associated with the note.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the entry was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "object": {"type": "string", "description": "Object name."}
            },
            "required": ["object"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SCRATCHPADENTRY {arguments['object']}")

class QueryEventLog(BaseCommand):
    @property
    def name(self) -> str:
        return "query_event_log"

    @property
    def description(self) -> str:
        return (
            "Display messages from the server activity/audit log.\n\n"
            "**Input Parameters**:\n"
            "- search (Optional): Search string to filter messages.\n"
            "- begintime (Optional): Start time (e.g. 08:00).\n"
            "- endtime (Optional): End time (e.g. 18:00).\n\n"
            "**Output Parameters**:\n"
            "- Date/Time: When the event occurred.\n"
            "- Message: The log message content.\n"
            "- Severity: Level of importance (Info, Warning, Error)."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "search": {"type": "string", "description": "Search string to filter messages."},
                "begintime": {"type": "string", "description": "Start time (e.g. 08:00)."},
                "endtime": {"type": "string", "description": "End time (e.g. 18:00)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY ACTLOG"
        if arguments.get("search"):
            cmd += f" SEARCH={arguments['search']}"
        if arguments.get("begintime"):
            cmd += f" BEGINTIME={arguments['begintime']}"
        return self._execute_simple_query(cmd)

class QueryPendingCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "query_pending_command"

    @property
    def description(self) -> str:
        return (
            "Display a list of administrative commands that are pending approval.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Command ID: ID to approve/reject.\n"
            "- Command: The command string.\n"
            "- Requestor: Who requested it."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY PENDINGCMD")

class QueryProfile(BaseCommand):
    @property
    def name(self) -> str:
        return "query_profile"

    @property
    def description(self) -> str:
        return (
            "Query a configuration profile subscribed to by other servers.\n\n"
            "**Input Parameters**:\n"
            "- profile_name (Optional): Profile name.\n\n"
            "**Output Parameters**:\n"
            "- Profile Name: Name of the profile.\n"
            "- Description: Description of contents."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "profile_name": {"type": "string", "description": "Profile name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY PROFILE"
        if arguments.get("profile_name"):
            cmd += f" {arguments['profile_name']}"
        return self._execute_simple_query(cmd)

class QueryUserRequest(BaseCommand):
    @property
    def name(self) -> str:
        return "query_user_request"

    @property
    def description(self) -> str:
        return (
            "Query one or more pending manual mount requests (e.g., for tape).\n\n"
            "**Input Parameters**:\n"
            "- request_id (Optional): Request ID.\n\n"
            "**Output Parameters**:\n"
            "- Request ID: ID of the request.\n"
            "- Volume Name: Media required.\n"
            "- Drive Name: Drive to load."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "request_id": {"type": "string", "description": "Request ID."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY REQUEST"
        if arguments.get("request_id"):
             cmd += f" {arguments['request_id']}"
        return self._execute_simple_query(cmd)

class UpdateCollocationGroup(BaseCommand):
    @property
    def name(self) -> str:
        return "update_collocation_group"
    @property
    def description(self) -> str:
        return (
            "Updates a **Collocation Group** description.\n"
            "**Input Parameters**:\n"
            "- group_name (Required): The group name.\n"
            "- description (Optional): The new description.\n"
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
        cmd = f"UPDATE COLLOCGROUP {arguments['group_name']}"
        if arguments.get("description"): cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)
