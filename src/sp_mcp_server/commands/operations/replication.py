from typing import Any, Dict
from ..base import BaseCommand

class QueryProtectionStatus(BaseCommand):
    @property
    def name(self) -> str:
        return "query_protection_status"

    @property
    def description(self) -> str:
        return (
            "Query the status of storage pool protection operations (e.g., replication to target).\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Storage Pool: The source pool.\n"
            "- Protection Status: Synced or not."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY PROTECTSTATUS")

class QueryReplicationFailures(BaseCommand):
    @property
    def name(self) -> str:
        return "query_replication_failures"
    
    @property
    def description(self) -> str:
        return (
            "Query detailed data about replication failures.\n\n"
            "**Input Parameters**:\n"
            "- None.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: The client that failed.\n"
            "- File Space: The backup volume that failed.\n"
            "- Failure Date: Time of failure."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query("QUERY REPLFAILURES")

class QueryReplicationStatus(BaseCommand):
    @property
    def name(self) -> str:
        return "query_replication_status"

    @property
    def description(self) -> str:
        return (
            "Query active client replication processes.\n\n"
            "**Input Parameters**:\n"
            "- client_name (Optional): Client name to filter.\n\n"
            "**Output Parameters**:\n"
            "- Client Name: Client being replicated.\n"
            "- Bytes Replicated: Data moved.\n"
            "- Status: Current activity."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client name. (maps to node_name)"}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY REPLICATION"
        if arguments.get("client_name"):
            cmd += f" {arguments['client_name']}"
        return self._execute_simple_query(cmd)

class QueryReplicationRule(BaseCommand):
    @property
    def name(self) -> str:
        return "query_replication_rule"

    @property
    def description(self) -> str:
        return (
            "Query rules governing replication behavior.\n\n"
            "**Input Parameters**:\n"
            "- rule_name (Optional): Rule name.\n\n"
            "**Output Parameters**:\n"
            "- Rule Name: Name of the rule.\n"
            "- Priority: Execution priority."
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
        cmd = "QUERY REPLRULE"
        if arguments.get("rule_name"):
            cmd += f" {arguments['rule_name']}"
        return self._execute_simple_query(cmd)

class QueryReplicationServer(BaseCommand):
    @property
    def name(self) -> str:
        return "query_replication_server"

    @property
    def description(self) -> str:
        return (
            "Query a defined replication server.\n\n"
            "**Input Parameters**:\n"
            "- server_name (Optional): Server name.\n\n"
            "**Output Parameters**:\n"
            "- Server Name: The partner server.\n"
            "- Server Address: Network location."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "Server name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY REPLSERVER"
        if arguments.get("server_name"):
            cmd += f" {arguments['server_name']}"
        return self._execute_simple_query(cmd)
