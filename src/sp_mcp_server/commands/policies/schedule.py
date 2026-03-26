from typing import Any, Dict
from ..base import BaseCommand

class DefineSchedule(BaseCommand):
    @property
    def name(self) -> str:
        return "define_schedule"
        
    @property
    def description(self) -> str:
        return (
            "Defines a **Job Schedule** (known as a **Client Schedule** in SP) to automate backup tasks.\n"
            "**Input Parameters**:\n"
            "- domain_name (Required): Parent Policy Domain.\n"
            "- schedule_name (Required): Name for the Schedule.\n"
            "- action (Optional): The type of action (e.g., 'INCREMENTAL', 'SELECTIVE').\n"
            "- start_time (Optional): Schedule start time.\n"
            "- duration (Optional): execution window duration.\n"
            "- period (Optional): Frequency (days) between runs.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the schedule was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Domain name."},
                "schedule_name": {"type": "string", "description": "Schedule name."},
                "action": {"type": "string", "description": "Action (e.g. INCREMENTAL)."},
                "start_time": {"type": "string", "description": "Start time."},
                "duration": {"type": "integer", "description": "Duration value."},
                "period": {"type": "integer", "description": "Period value."}
            },
            "required": ["domain_name", "schedule_name"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE SCHEDULE {arguments['domain_name']} {arguments['schedule_name']}"
        if arguments.get("action"):
            cmd += f" ACTION={arguments['action']}"
        if arguments.get("start_time"):
            cmd += f" STARTTIME={arguments['start_time']}"
        if arguments.get("duration"):
            cmd += f" DURATION={arguments['duration']}"
        if arguments.get("period"):
             cmd += f" PERIOD={arguments['period']}"
        return self._execute_simple_query(cmd)

class UpdateSchedule(BaseCommand):
    @property
    def name(self) -> str:
        return "update_schedule"
    @property
    def description(self) -> str:
        return (
            "Updates a **Job Schedule** (Client Schedule).\n"
            "**Input Parameters**:\n"
            "- domain_name (Required): The Policy Domain.\n"
            "- schedule_name (Required): The Schedule name.\n"
            "- action (Optional): New action type.\n"
            "- start_time (Optional): New start time.\n"
            "- duration (Optional): New duration.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the schedule was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Domain name."},
                "schedule_name": {"type": "string", "description": "Schedule name."},
                "action": {"type": "string", "description": "Action."},
                "start_time": {"type": "string", "description": "Start time."},
                "duration": {"type": "integer", "description": "Duration."}
            },
            "required": ["domain_name", "schedule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE SCHEDULE {arguments['domain_name']} {arguments['schedule_name']}"
        if arguments.get("action"): cmd += f" ACTION={arguments['action']}"
        if arguments.get("start_time"): cmd += f" STARTTIME={arguments['start_time']}"
        if arguments.get("duration"): cmd += f" DURATION={arguments['duration']}"
        return self._execute_simple_query(cmd)

class DeleteSchedule(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_schedule"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Job Schedule** (Client Schedule).\n"
            "**Input Parameters**:\n"
            "- domain_name (Required): Parent Policy Domain.\n"
            "- schedule_name (Required): Name of the schedule to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the schedule was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Domain name."},
                "schedule_name": {"type": "string", "description": "Schedule name."}
            },
            "required": ["domain_name", "schedule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SCHEDULE {arguments['domain_name']} {arguments['schedule_name']}")

class QuerySchedule(BaseCommand):
    @property
    def name(self) -> str:
        return "query_schedule"

    @property
    def description(self) -> str:
        return (
            "Display information about administrative and client data protection schedules.\n\n"
            "**Input Parameters**:\n"
            "- schedule_name (Optional): Name of the schedule.\n"
            "- policy_group (Optional): Policy group for client schedules.\n"
            "- type (Optional): Type of schedule (admin or client).\n\n"
            "**Output Parameters**:\n"
            "- Schedule Name: Name of the schedule.\n"
            "- Start Date/Time: When the schedule activates.\n"
            "- Duration: How long the window is open.\n"
            "- Period: Frequency (e.g., Daily, Weekly)."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "schedule_name": {"type": "string", "description": "Name of the schedule"},
                "policy_group": {"type": "string", "description": "Policy group for client schedules (maps to domain_name)."},
                "type": {"type": "string", "enum": ["admin", "client"], "description": "Type of schedule"}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY SCHEDULE"
        if arguments.get("policy_group"):
            cmd += f" {arguments['policy_group']}"
        if arguments.get("schedule_name"):
            cmd += f" {arguments['schedule_name']}"
        
        if arguments.get("type") == "admin":
             cmd += " TYPE=ADMIN"
        
        return self._execute_simple_query(cmd)

class QueryScheduledEvent(BaseCommand):
    @property
    def name(self) -> str:
        return "query_scheduled_event"

    @property
    def description(self) -> str:
        return (
            "Display results and status of past or projected future scheduled events.\n\n"
            "**Input Parameters**:\n"
            "- policy_group (Optional): Policy group.\n"
            "- schedule_name (Optional): Schedule name.\n"
            "- begindate (Optional): Filter start date.\n"
            "- starttime (Optional): Filter start time.\n"
            "- enddate (Optional): Filter end date.\n"
            "- endtime (Optional): Filter end time.\n\n"
            "**Output Parameters**:\n"
            "- Scheduled Start: Planned execution time.\n"
            "- Actual Start: When it really ran.\n"
            "- Status: Missed, Completed, Failed, Future.\n"
            "- Result: Return code."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "policy_group": {"type": "string", "description": "Policy group (maps to domain_name)."},
                 "schedule_name": {"type": "string", "description": "Schedule name."},
                 "begindate": {"type": "string", "description": "Filter start date."},
                 "starttime": {"type": "string", "description": "Filter start time."},
                 "enddate": {"type": "string", "description": "Filter end date."},
                 "endtime": {"type": "string", "description": "Filter end time."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY EVENT"
        if arguments.get("policy_group"):
            cmd += f" {arguments['policy_group']}"
        if arguments.get("schedule_name"):
            cmd += f" {arguments['schedule_name']}"
            
        if arguments.get("begindate"):
             cmd += f" BEGINDATE={arguments['begindate']}"
        if arguments.get("starttime"):
             cmd += f" STARTTIME={arguments['starttime']}"
        if arguments.get("enddate"):
             cmd += f" ENDDATE={arguments['enddate']}"
        if arguments.get("endtime"):
             cmd += f" ENDTIME={arguments['endtime']}"
             
        return self._execute_simple_query(cmd)

class QueryScheduleAssociation(BaseCommand):
    @property
    def name(self) -> str:
        return "query_schedule_association"

    @property
    def description(self) -> str:
        return (
            "Display associations between client nodes and schedules.\n\n"
            "**Input Parameters**:\n"
            "- policy_group (Optional): Policy group.\n"
            "- schedule_name (Optional): Schedule name.\n"
            "- client_name (Optional): Client name.\n\n"
            "**Output Parameters**:\n"
            "- Schedule Name: The schedule.\n"
            "- Client Name: The associated node."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
             "type": "object",
             "properties": {
                 "policy_group": {"type": "string", "description": "Policy group (maps to domain_name)."},
                 "schedule_name": {"type": "string", "description": "Schedule name."},
                 "client_name": {"type": "string", "description": "Client name (maps to node_name)."}
             }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY ASSOCIATION"
        if arguments.get("policy_group"):
            cmd += f" {arguments['policy_group']}"
        if arguments.get("schedule_name"):
            cmd += f" {arguments['schedule_name']}"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        return self._execute_simple_query(cmd)
