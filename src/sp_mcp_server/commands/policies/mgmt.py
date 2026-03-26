from typing import Any, Dict
from ..base import BaseCommand

class DefineManagementClass(BaseCommand):
    @property
    def name(self) -> str:
        return "define_management_class"
    
    @property
    def description(self) -> str:
        return (
            "Defines a **Retention Policy** (known as a **Management Class** in SP). Determines how files are managed/retained.\n"
            "**Input Parameters**:\n"
            "- domain_name (Required): Parent Policy Domain.\n"
            "- policy_set_name (Required): Parent Policy Profile.\n"
            "- class_name (Required): Name for the Retention Policy.\n"
            "- description (Optional): Description.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the policy was defined."
        )
        
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Domain name."},
                "policy_set_name": {"type": "string", "description": "Policy set name."},
                "class_name": {"type": "string", "description": "Management class name."},
                "description": {"type": "string", "description": "Description."}
            },
            "required": ["domain_name", "policy_set_name", "class_name"]
        }
        
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE MGMTCLASS {arguments['domain_name']} {arguments['policy_set_name']} {arguments['class_name']}"
        if arguments.get("description"):
            cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class UpdateManagementClass(BaseCommand):
    @property
    def name(self) -> str:
        return "update_management_class"
    @property
    def description(self) -> str:
        return (
            "Updates a **Retention Policy** (Management Class) description.\n"
            "**Input Parameters**:\n"
            "- domain_name (Required): The parent Policy Domain.\n"
            "- policy_set_name (Required): The parent Policy Profile (Set).\n"
            "- class_name (Required): The name of the Retention Policy (Management Class).\n"
            "- description (Optional): The new description.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the management class was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Domain name."},
                "policy_set_name": {"type": "string", "description": "Policy set name."},
                "class_name": {"type": "string", "description": "Class name."},
                "description": {"type": "string", "description": "Description."}
            },
            "required": ["domain_name", "policy_set_name", "class_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE MGMTCLASS {arguments['domain_name']} {arguments['policy_set_name']} {arguments['class_name']}"
        if arguments.get("description"): cmd += f" DESCRIPTION=\"{arguments['description']}\""
        return self._execute_simple_query(cmd)

class DeleteManagementClass(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_management_class"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Retention Policy** (Management Class).\n"
            "**Input Parameters**:\n"
            "- domain_name (Required): Parent Policy Domain.\n"
            "- policy_set_name (Required): Parent Policy Profile.\n"
            "- class_name (Required): Name of the Management Class to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the management class was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Domain name."},
                "policy_set_name": {"type": "string", "description": "Policy set name."},
                "class_name": {"type": "string", "description": "Class name."}
            },
            "required": ["domain_name", "policy_set_name", "class_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE MGMTCLASS {arguments['domain_name']} {arguments['policy_set_name']} {arguments['class_name']}")

class QueryProtectionPolicy(BaseCommand):
    @property
    def name(self) -> str:
        return "query_protection_policy"

    @property
    def description(self) -> str:
        return (
            "Queries **Retention Policies** (Management Classes). Defines specific file management behaviors (e.g., standard backup vs long-term archive).\n"
            "**Input Parameters**:\n"
            "- policy_group (Optional): Parent domain.\n"
            "- policy_set (Optional): Parent profile.\n"
            "- policy_name (Optional): Specific Retention Policy name.\n"
            "**Output Parameters**:\n"
            "- Policy Domain: Parent domain.\n"
            "- Policy Set: Parent profile.\n"
            "- Mgmt Class Name: Service level identifier.\n"
            "- Default Mgmt Class: Indicates if this is the default policy."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "policy_group": {"type": "string", "description": "Policy group name."},
                "policy_set": {"type": "string", "description": "Policy set name."},
                "policy_name": {"type": "string", "description": "Protection policy/Management class name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY MGMTCLASS"
        if arguments.get("policy_group"):
            cmd += f" {arguments['policy_group']}"
        if arguments.get("policy_set"):
            cmd += f" {arguments['policy_set']}"
        if arguments.get("policy_name"):
            cmd += f" {arguments['policy_name']}"
        return self._execute_simple_query(cmd)
