from typing import Any, Dict
from ..base import BaseCommand

class RegisterNode(BaseCommand):
    @property
    def name(self) -> str:
        return "register_node"
    @property
    def description(self) -> str:
        return (
            "Registers a new **Client** (known as a **Node** in SP) for data protection. A Client represents a source system (like a server, laptop, or VM) that contains data to be backed up.\n"
            "**Input Parameters**:\n"
            "- client_name (Required): The unique name of the Client to register.\n"
            "- password (Required): The password used for Client authentication.\n"
            "- domain_name (Required): The **Policy Domain** (SLA) to which the Client will be assigned.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the Client was registered."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Name of the client to register."},
                "password": {"type": "string", "description": "Client password."},
                "domain_name": {"type": "string", "description": "Policy domain name."},
            },
            "required": ["client_name", "password", "domain_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"REGISTER NODE {arguments['client_name']} {arguments['password']} DOMAIN={arguments['domain_name']}"
        return self._execute_simple_query(cmd)

class RenameClient(BaseCommand):
    @property
    def name(self) -> str:
        return "rename_client"
    @property
    def description(self) -> str:
        return (
            "Renames an existing **Client** (Node). This updates the unique identifier used for all backup and restore operations for the source system.\n"
            "**Input Parameters**:\n"
            "- current_name (Required): The current name of the Client.\n"
            "- new_name (Required): The new name for the Client.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the Client was renamed."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "current_name": {"type": "string", "description": "Current client name."},
                "new_name": {"type": "string", "description": "New client name."}
            },
            "required": ["current_name", "new_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"RENAME NODE {arguments['current_name']} {arguments['new_name']}")

class SetClientLock(BaseCommand):
    @property
    def name(self) -> str:
        return "set_client_lock"
    @property
    def description(self) -> str:
        return (
            "Locks or unlocks a **Client** (Node) to control access to the backup server. A locked Client cannot perform backups or restores.\n"
            "**Input Parameters**:\n"
            "- client_name (Required): The name of the Client.\n"
            "- lock_status (Required): Set to 'lock' to disable access, or 'unlock' to enable access.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the lock status was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name."},
                "lock_status": {"type": "string", "enum": ["lock", "unlock"], "description": "Action to perform."}
            },
            "required": ["client_name", "lock_status"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        action = "LOCK NODE" if arguments["lock_status"] == "lock" else "UNLOCK NODE"
        return self._execute_simple_query(f"{action} {arguments['client_name']}")

class UpdateNode(BaseCommand):
    @property
    def name(self) -> str:
        return "update_node"
    @property
    def description(self) -> str:
        return (
            "Updates properties of an existing **Client** (Node).\n"
            "**Input Parameters**:\n"
            "- node_name (Required): Name of the Client to update.\n"
            "- domain_name (Optional): Assign to a different **Policy Domain**.\n"
            "- password (Optional): Update the Client password.\n"
            "- contact (Optional): Update contact information.\n"
            "- cloptset (Optional): Assign a different **Client Configuration Profile** (Option Set).\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the Client was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "node_name": {"type": "string", "description": "Node name."},
                "domain_name": {"type": "string", "description": "New domain."},
                "password": {"type": "string", "description": "New password."},
                "contact": {"type": "string", "description": "Contact info."},
                "cloptset": {"type": "string", "description": "Option set."}
            },
            "required": ["node_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE NODE {arguments['node_name']}"
        if arguments.get("password"): cmd += f" {arguments['password']}"
        if arguments.get("domain_name"): cmd += f" DOMAIN={arguments['domain_name']}"
        if arguments.get("contact"): cmd += f" CONTACT=\"{arguments['contact']}\""
        if arguments.get("cloptset"): cmd += f" CLOPTSET={arguments['cloptset']}"
        return self._execute_simple_query(cmd)

class DeleteClient(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_client"
    @property
    def description(self) -> str:
        return (
            "Decomissions a **Client** (Node) and removes all its configuration from the server. This is a destructive operation.\n"
            "**Input Parameters**:\n"
            "- client_name (Required): The name of the Client to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the Client was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name."}
            },
            "required": ["client_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE NODE {arguments['client_name']}")

class DeleteNode(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_node"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Client** (Node). Similar to delete_client but using 'node' terminology.\n"
            "**Input Parameters**:\n"
            "- node_name (Required): The name of the node to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the node was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "node_name": {"type": "string", "description": "Node name."}
            },
            "required": ["node_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE NODE {arguments['node_name']}")

class QueryClient(BaseCommand):
    @property
    def name(self) -> str:
        return "query_client"

    @property
    def description(self) -> str:
        return (
            "Display information about registered clients (Nodes).\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Name of the client to query.\n"
            "- policy_group (Optional): Filter by policy group/domain.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The name of the client node.\n"
            "- Platform: The client operating system.\n"
            "- Policy Domain: The policy group the client belongs to.\n"
            "- Last Access: Days since last communication.\n"
            "- Locked: Whether the client is locked.\n"
            "- Password Set Date: Date password was last set."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Name of the client to query. (maps to node_name)"},
                "policy_group": {"type": "string", "description": "Filter by policy group/domain. (maps to domain_name)"}
            },
            "required": []
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY NODE"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        if arguments.get("policy_group"):
            cmd += f" DOMAIN={arguments['policy_group']}"
        return self._execute_simple_query(cmd)

class QueryProxyClient(BaseCommand):
    @property
    def name(self) -> str:
        return "query_proxy_client"

    @property
    def description(self) -> str:
        return (
            "Query relationships where one client (agent) is authorized to act on behalf of another (target).\n\n"
            "**Input Parameters**:\n"
            "- target_client (Optional): Target client name.\n"
            "- agent_client (Optional): Agent client name.\n\n"
            "**Output Parameters**:\n"
            "- Target Client: The client whose data is being accessed.\n"
            "- Agent Client: The client granted access."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "target_client": {"type": "string", "description": "Target client name (maps to target_node)."},
                 "agent_client": {"type": "string", "description": "Agent client name (maps to agent_node)."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY PROXYNODE"
        if arguments.get("target_client"):
            cmd += f" TARGET={arguments['target_client']}"
        if arguments.get("agent_client"):
            cmd += f" AGENT={arguments['agent_client']}"
        return self._execute_simple_query(cmd)

class QueryReplicationClient(BaseCommand):
    @property
    def name(self) -> str:
        return "query_replication_client"

    @property
    def description(self) -> str:
        return (
            "Display information about replication status for a client.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The executing client.\n"
            "- State: Replication state (e.g., SYNC, SENDING).\n"
            "- Target Server: Destination for replication."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "client_name": {"type": "string", "description": "Client name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY REPLNODE"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        return self._execute_simple_query(cmd)

class QueryPVUEstimate(BaseCommand):
    @property
    def name(self) -> str:
        return "query_pvu_estimate"

    @property
    def description(self) -> str:
        return (
            "Display an estimate of the Processor Value Units (PVU) for license calculation.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name.\n\n"
            "**Output Parameters**:\n"
            "- Node Name: The client.\n"
            "- PVU Estimate: Estimated PVU details."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY PVUESTIMATE"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        return self._execute_simple_query(cmd)
