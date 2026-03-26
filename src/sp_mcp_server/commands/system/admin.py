from typing import Any, Dict
from ..base import BaseCommand

class DefineAdmin(BaseCommand):
    @property
    def name(self) -> str:
        return "define_admin"
    @property
    def description(self) -> str:
        return (
            "Defines an **Administrator** account with specific privileges.\n"
            "**Input Parameters**:\n"
            "- admin_name (Required): The name of the administrator.\n"
            "- password (Required): The password for the administrator.\n"
            "- contact (Optional): Contact information.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the administrator was defined."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "admin_name": {"type": "string"},
                "password": {"type": "string"},
                "contact": {"type": "string"}
            },
            "required": ["admin_name", "password"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE ADMIN {arguments['admin_name']} {arguments['password']}"
        if arguments.get("contact"):
            cmd += f" CONTACT=\"{arguments['contact']}\""
        return self._execute_simple_query(cmd)

class UpdateUser(BaseCommand):
    @property
    def name(self) -> str:
        return "update_user"
    @property
    def description(self) -> str:
        return (
            "Updates an **Administrator** account (System User). Modify password or contact info.\n"
            "**Input Parameters**:\n"
            "- user_name (Required): The name of the administrator to update.\n"
            "- password (Optional): The new password.\n"
            "- contact (Optional): New contact information.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the user was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_name": {"type": "string", "description": "User name (Admin)."},
                "password": {"type": "string", "description": "New password."},
                "contact": {"type": "string", "description": "Contact info."}
            },
            "required": ["user_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE ADMIN {arguments['user_name']}"
        if arguments.get("password"): cmd += f" {arguments['password']}"
        if arguments.get("contact"): cmd += f" CONTACT=\"{arguments['contact']}\""
        return self._execute_simple_query(cmd)

class SetUserLock(BaseCommand):
    @property
    def name(self) -> str:
        return "set_user_lock"
    @property
    def description(self) -> str:
        return (
            "Locks or unlocks an **Administrator** account. Locked admins cannot log in.\n"
            "**Input Parameters**:\n"
            "- user_name (Required): The name of the administrator.\n"
            "- lock_status (Required): 'lock' to disable access, 'unlock' to enable access.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the lock status was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_name": {"type": "string", "description": "User name."},
                "lock_status": {"type": "string", "enum": ["lock", "unlock"], "description": "Action to perform."}
            },
            "required": ["user_name", "lock_status"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        action = "LOCK ADMIN" if arguments["lock_status"] == "lock" else "UNLOCK ADMIN"
        return self._execute_simple_query(f"{action} {arguments['user_name']}")

class GrantAuthority(BaseCommand):
    @property
    def name(self) -> str:
        return "grant_authority"
    @property
    def description(self) -> str:
        return (
            "Grants specific **Privilege Classes** to an administrator. Controls authorization level.\n"
            "**Input Parameters**:\n"
            "- user_name (Required): The name of the administrator.\n"
            "- classes (Required): Space-separated list of privilege classes (e.g., 'system policy storage').\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the authority was granted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_name": {"type": "string", "description": "User name."},
                "classes": {"type": "string", "description": "Privilege classes (e.g. SYSTEM, POLICY, STORAGE)."}
            },
            "required": ["user_name", "classes"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        # Syntax: GRANT AUTHORITY admin_name CLASSES=class_name
        # Or simple: GRANT AUTHORITY admin_name class_name
        return self._execute_simple_query(f"GRANT AUTHORITY {arguments['user_name']} CLASSES={arguments['classes']}")

class RevokeAuthority(BaseCommand):
    @property
    def name(self) -> str:
        return "revoke_authority"
    @property
    def description(self) -> str:
        return (
            "Revokes specific **Privilege Classes** from an administrator.\n"
            "**Input Parameters**:\n"
            "- user_name (Required): The name of the administrator.\n"
            "- classes (Required): Space-separated list of privilege classes to revoke.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the authority was revoked."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_name": {"type": "string", "description": "User name."},
                "classes": {"type": "string", "description": "Privilege classes to revoke."}
            },
            "required": ["user_name", "classes"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"REVOKE AUTHORITY {arguments['user_name']} CLASSES={arguments['classes']}")

class RegisterLicense(BaseCommand):
    @property
    def name(self) -> str:
        return "register_license"
    @property
    def description(self) -> str:
        return (
            "Registers a new **Software License** key from a specified file.\n"
            "**Input Parameters**:\n"
            "- file_path (Required): The full path to the license file on the server.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the license was registered."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the license file."}
            },
            "required": ["file_path"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"REGISTER LICENSE FILE={arguments['file_path']}")

class DeleteAdmin(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_admin"
    @property
    def description(self) -> str:
        return (
            "Deletes an **Administrator** account.\n"
            "**Input Parameters**:\n"
            "- admin_name (Required): The name of the administrator to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the administrator was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "admin_name": {"type": "string", "description": "Admin name."}
            },
            "required": ["admin_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE ADMIN {arguments['admin_name']}")

class QueryAdminUser(BaseCommand):
    @property
    def name(self) -> str:
        return "query_admin_user"

    @property
    def description(self) -> str:
        return (
            "Display information about server administrators/users.\n\n"
            "**Input Parameters**:\n"
            "- admin_name (Optional): Administrator name.\n\n"
            "**Output Parameters**:\n"
            "- Administrator Name: User ID.\n"
            "- Last Access: When they last logged in.\n"
            "- Days Since Password Set: Password age.\n"
            "- Locked: Account status."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "admin_name": {"type": "string", "description": "Administrator name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY ADMIN"
        if arguments.get("admin_name"):
            cmd += f" {arguments['admin_name']}"
        return self._execute_simple_query(cmd)

class QueryLicenseInfo(BaseCommand):
    @property
    def name(self) -> str:
        return "query_license_info"

    @property
    def description(self) -> str:
        return (
            "Display software license compliance information.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- License Name: Name of the licensed feature.\n"
            "- Compliance Status: Whether the server is compliant.\n"
            "- Licensed Units: Number of units authorized."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY LICENSE")
