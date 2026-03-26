from typing import Any, Dict
from ..base import BaseCommand

class QuerySubscriber(BaseCommand):
    @property
    def name(self) -> str:
        return "query_subscriber"

    @property
    def description(self) -> str:
        return (
            "Display information about subscribers to event or report services.\n\n"
            "**Input Parameters**:\n"
            "- subscriber_name (Optional): Subscriber name.\n\n"
            "**Output Parameters**:\n"
            "- Subscriber Name: Name of the subscriber.\n"
            "- Address: Contact or network address."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                 "subscriber_name": {"type": "string"}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY SUBSCRIBER"
        if arguments.get("subscriber_name"):
             cmd += f" {arguments['subscriber_name']}"
        return self._execute_simple_query(cmd)

class QuerySubscription(BaseCommand):
    @property
    def name(self) -> str:
        return "query_subscription"

    @property
    def description(self) -> str:
        return (
            "Display subscription details, linking subscribers to specific profiles or services.\n\n"
            "**Input Parameters**:\n"
            "- subscription_name (Optional): Subscription name.\n\n"
            "**Output Parameters**:\n"
            "- Profile: The subscribed profile.\n"
            "- Administrator: The admin managing it."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "subscription_name": {"type": "string"}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY SUBSCRIPTION"
        if arguments.get("subscription_name"):
             cmd += f" {arguments['subscription_name']}"
        return self._execute_simple_query(cmd)
