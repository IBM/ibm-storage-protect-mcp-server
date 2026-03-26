from typing import Any, Dict
from ..base import BaseCommand

class DefineSpaceTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "define_space_trigger"
    @property
    def description(self) -> str:
        return (
            "Define a **Space Trigger** for a storage pool. Automatically expands the pool when space runs low.\n"
            "**Input Parameters**:\n"
            "- pool_name (Required): The name of the storage pool.\n"
            "- full_pct (Required): The utilization percentage to trigger expansion.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the trigger was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pool_name": {"type": "string", "description": "Storage pool name."},
                "full_pct": {"type": "integer", "description": "Full percentage threshold."}
            },
            "required": ["pool_name", "full_pct"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DEFINE SPACETRIGGER {arguments['pool_name']} FULLPCT={arguments['full_pct']}")

class UpdateSpaceTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "update_space_trigger"
    @property
    def description(self) -> str:
        return (
            "Updates a **Space Trigger** for a storage pool.\n"
            "**Input Parameters**:\n"
            "- pool_name (Required): The storage pool name.\n"
            "- full_pct (Optional): New full percentage threshold to trigger expansion.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the trigger was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pool_name": {"type": "string", "description": "Pool name."},
                "full_pct": {"type": "integer", "description": "Full percentage."}
            },
            "required": ["pool_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE SPACETRIGGER {arguments['pool_name']}"
        if arguments.get("full_pct"): cmd += f" FULLPCT={arguments['full_pct']}"
        return self._execute_simple_query(cmd)

class DeleteSpaceTrigger(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_space_trigger"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Space Trigger** from a storage pool.\n"
            "**Input Parameters**:\n"
            "- pool_name (Required): The storage pool name.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the trigger was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pool_name": {"type": "string", "description": "Storage pool name."}
            },
            "required": ["pool_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SPACETRIGGER {arguments['pool_name']}")

class DefineStatusThreshold(BaseCommand):
    @property
    def name(self) -> str:
        return "define_status_threshold"
    @property
    def description(self) -> str:
        return (
            "Define a **Status Threshold** definition for system monitoring. Sets conditions for health reporting.\n"
            "**Input Parameters**:\n"
            "- activity (Required): The system activity to monitor (e.g., DBBACKUP).\n"
            "- condition (Optional): The condition to check (e.g., EXISTENCE).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the threshold was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "activity": {"type": "string", "description": "Activity type (e.g. DBBACKUP)."},
                "condition": {"type": "string", "description": "Condition (e.g. EXISTENCE)."}
            },
            "required": ["activity"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE STATUSTHRESHOLD {arguments['activity']}"
        if arguments.get("condition"): cmd += f" CONDITION={arguments['condition']}"
        return self._execute_simple_query(cmd)

class UpdateStatusThreshold(BaseCommand):
    @property
    def name(self) -> str:
        return "update_status_threshold"
    @property
    def description(self) -> str:
        return (
            "Updates a **Status Threshold** definition for system monitoring.\n"
            "**Input Parameters**:\n"
            "- activity (Required): The activity type to monitor.\n"
            "- condition (Optional): The condition indicating a status change (e.g., EXISTS, NOEXIST).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the threshold was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "activity": {"type": "string", "description": "Activity."},
                "condition": {"type": "string", "description": "Condition."}
            },
            "required": ["activity"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE STATUSTHRESHOLD {arguments['activity']}"
        if arguments.get("condition"): cmd += f" CONDITION={arguments['condition']}"
        return self._execute_simple_query(cmd)

class DeleteStatusThreshold(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_status_threshold"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Status Threshold** definition.\n"
            "**Input Parameters**:\n"
            "- activity (Required): The activity type.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the threshold was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "activity": {"type": "string", "description": "Activity."}
            },
            "required": ["activity"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE STATUSTHRESHOLD {arguments['activity']}")

class DefineStorageRule(BaseCommand):
    @property
    def name(self) -> str:
        return "define_storage_rule"
    @property
    def description(self) -> str:
        return (
            "Define a **Storage Rule** for tiering or auditing. Automates data movement between tiers.\n"
            "**Input Parameters**:\n"
            "- rule_name (Required): The name of the new storage rule.\n"
            "- action_type (Required): The action to perform (e.g., TIERBYGROUP).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the rule was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "Rule name."},
                "action_type": {"type": "string", "description": "Action type (e.g. TIERBYGROUP)."}
            },
            "required": ["rule_name", "action_type"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DEFINE STGRULE {arguments['rule_name']} ACTIONTYPE={arguments['action_type']}")

class UpdateStorageRule(BaseCommand):
    @property
    def name(self) -> str:
        return "update_storage_rule"
    @property
    def description(self) -> str:
        return (
            "Updates a **Storage Rule** (e.g., enable/disable).\n"
            "**Input Parameters**:\n"
            "- rule_name (Required): The rule name.\n"
            "- active (Optional): 'YES' or 'NO' to activate/deactivate the rule.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the rule was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "Rule name."},
                "active": {"type": "string", "enum": ["YES", "NO"], "description": "Active status."}
            },
            "required": ["rule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE STGRULE {arguments['rule_name']}"
        if arguments.get("active"): cmd += f" ACTIVE={arguments['active']}"
        return self._execute_simple_query(cmd)

class DeleteStorageRule(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_storage_rule"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Storage Rule**.\n"
            "**Input Parameters**:\n"
            "- rule_name (Required): The rule name.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the rule was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "Rule name."}
            },
            "required": ["rule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE STGRULE {arguments['rule_name']}")

class DefineSubRule(BaseCommand):
    @property
    def name(self) -> str:
        return "define_sub_rule"
    @property
    def description(self) -> str:
        return (
            "Define a **Subrule** for a storage rule. Adds specific targets to a parent rule.\n"
            "**Input Parameters**:\n"
            "- rule_name (Required): The parent storage rule name.\n"
            "- sub_rule_name (Required): The name of the subrule.\n"
            "- target_name (Optional): The target entity (e.g., node group).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the subrule was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "Parent rule name."},
                "sub_rule_name": {"type": "string", "description": "Sub rule name."},
                "target_name": {"type": "string", "description": "Target entity name."}
            },
            "required": ["rule_name", "sub_rule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE SUBRULE {arguments['rule_name']} {arguments['sub_rule_name']}"
        if arguments.get("target_name"): cmd += f" TARGETNAME={arguments['target_name']}"
        return self._execute_simple_query(cmd)

class UpdateSubRule(BaseCommand):
    @property
    def name(self) -> str:
        return "update_sub_rule"
    @property
    def description(self) -> str:
        return (
            "Updates a **Subrule** within a storage rule.\n"
            "**Input Parameters**:\n"
            "- rule_name (Required): The parent rule name.\n"
            "- sub_rule_name (Required): The subrule name.\n"
            "- target_name (Optional): New target entity name.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the subrule was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "Rule name."},
                "sub_rule_name": {"type": "string", "description": "Sub rule name."},
                "target_name": {"type": "string", "description": "New target."}
            },
            "required": ["rule_name", "sub_rule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE SUBRULE {arguments['rule_name']} {arguments['sub_rule_name']}"
        if arguments.get("target_name"): cmd += f" TARGETNAME={arguments['target_name']}"
        return self._execute_simple_query(cmd)

class DeleteSubRule(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_sub_rule"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Subrule** from a storage rule.\n"
            "**Input Parameters**:\n"
            "- rule_name (Required): The parent rule name.\n"
            "- sub_rule_name (Required): The subrule name.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the subrule was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "Rule name."},
                "sub_rule_name": {"type": "string", "description": "Sub rule name."}
            },
            "required": ["rule_name", "sub_rule_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE SUBRULE {arguments['rule_name']} {arguments['sub_rule_name']}")

class QueryStorageRule(BaseCommand):
    @property
    def name(self) -> str:
        return "query_storage_rule"

    @property
    def description(self) -> str:
        return (
            "Display information about storage rules (e.g., tiering rules).\n\n"
            "**Input Parameters**:\n"
            "- rule_name (Optional): Rule name.\n\n"
            "**Output Parameters**:\n"
            "- Rule Name: Name of the rule.\n"
            "- Source Pool: Source container.\n"
            "- Target Pool: Destination container."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "rule_name": {"type": "string", "description": "Rule name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY STGRULE"
        if arguments.get("rule_name"):
             cmd += f" {arguments['rule_name']}"
        return self._execute_simple_query(cmd)
