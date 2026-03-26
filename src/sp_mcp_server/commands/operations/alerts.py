from typing import Any, Dict
from ..base import BaseCommand

class DefineAlertTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "define_alert_trigger"
    @property
    def description(self) -> str:
        return (
            "Define an alert trigger with specific threshold.\n"
            "**Input Parameters**:\n"
            "- message_number (Required): Message number to trigger on.\n"
            "- category (Optional): Alert category.\n"
            "- severity (Optional): Alert severity.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the trigger was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message_number": {"type": "integer", "description": "Message number to trigger on."},
                "category": {"type": "string", "description": "Alert category."},
                "severity": {"type": "string", "description": "Alert severity."}
            },
            "required": ["message_number"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE ALERTTRIGGER {arguments['message_number']}"
        if arguments.get("category"): cmd += f" CATEGORY={arguments['category']}"
        if arguments.get("severity"): cmd += f" SEVERITY={arguments['severity']}"
        return self._execute_simple_query(cmd)

class UpdateAlertTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "update_alert_trigger"
    @property
    def description(self) -> str:
        return (
            "Updates a defined **Alert Trigger**. Can modify category or severity.\n"
            "**Input Parameters**:\n"
            "- message_number (Required): The message number identifying the alert.\n"
            "- category (Optional): New category (e.g., SYSTEM).\n"
            "- severity (Optional): New severity (e.g., SEVERE, ERROR).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the trigger was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message_number": {"type": "integer", "description": "Message number."},
                "category": {"type": "string", "description": "New category."},
                "severity": {"type": "string", "description": "New severity."}
            },
            "required": ["message_number"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE ALERTTRIGGER {arguments['message_number']}"
        if arguments.get("category"): cmd += f" CATEGORY={arguments['category']}"
        if arguments.get("severity"): cmd += f" SEVERITY={arguments['severity']}"
        return self._execute_simple_query(cmd)

class UpdateAlertStatus(BaseCommand):
    @property
    def name(self) -> str:
        return "update_alert_status"
    @property
    def description(self) -> str:
        return (
            "Updates the status of an existing **Alert**.\n"
            "**Input Parameters**:\n"
            "- alert_id (Required): The unique ID of the alert.\n"
            "- status (Required): New status (e.g., CLOSED).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the alert status was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "alert_id": {"type": "integer", "description": "Alert ID."},
                "status": {"type": "string", "description": "New status."}
            },
            "required": ["alert_id", "status"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"UPDATE ALERTSTATUS {arguments['alert_id']} STATUS={arguments['status']}")

class DeleteAlertTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_alert_trigger"
    @property
    def description(self) -> str:
        return (
            "Deletes a defined **Alert Trigger**.\n"
            "**Input Parameters**:\n"
            "- message_number (Required): The message number to remove.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the trigger was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message_number": {"type": "integer", "description": "Message number."}
            },
            "required": ["message_number"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE ALERTTRIGGER {arguments['message_number']}")

class QueryAlertTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "query_alert_trigger"

    @property
    def description(self) -> str:
        return (
            "Query the list of defined alert triggers that generate notifications.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Message Number: ID of the message triggering the alert.\n"
            "- Source: Origin of the alert."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY ALERTTRIGGER")

class QueryAlertStatus(BaseCommand):
    @property
    def name(self) -> str:
        return "query_alert_status"

    @property
    def description(self) -> str:
        return (
            "Query the current status of alerts in the system.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Alert ID: Unique ID.\n"
            "- Status: Active/Closed.\n"
            "- Message: Alert details."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY ALERTSTATUS")
