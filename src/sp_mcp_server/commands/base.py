from abc import ABC, abstractmethod
from typing import Any, Dict, List
import json
from ..cli_wrapper import DsmAdmcWrapper


class BaseCommand(ABC):
    """Abstract base class for all dsmadmc commands exposed as MCP tools."""

    def __init__(self, cli: DsmAdmcWrapper):
        self.cli = cli

    @property
    @abstractmethod
    def name(self) -> str:
        """The tool name exposed to the MCP client."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """The tool description exposed to the MCP client."""
        pass

    @property
    @abstractmethod
    def args_schema(self) -> Dict[str, Any]:
        """JSON schema describing the tool arguments."""
        pass

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> str:
        """
        Execute the command with the given arguments.
        Returns the formatted output string.
        """
        pass

    @property
    def tool_type(self) -> str:
        """Infers the tool type based on the name (read-only vs destructive)."""
        if self.name.lower().startswith("query") or "info" in self.name.lower():
            return "read-only"
        return "destructive"

    def _parse_comma_delimited(self, stdout: str) -> List[Dict[str, str]]:
        """
        Helper to parse dsmadmc -comma output.
        Note: dsmadmc output often includes header lines or information messages
        which might need stripping.
        """
        lines = stdout.strip().splitlines()
        results = []
        if not lines:
            return results

        # This is a naive parser. Real ISP output might be more complex.
        # Often the first lines are headers if not using -dataonly=yes
        # With -dataonly=yes, we might still get some preamble in some versions,
        # but locally wrappers sets -DATAONLY=YES.

        for line in lines:
            if not line.strip():
                continue
            # Basic CSV parsing logic or just return raw lines
            # For robustness in this MVP, we might return structured text
            # if we can't guarantee schema.
            pass

        return []

    def _format_command_error(self, prefix: str, stdout: str, stderr: str) -> str:
        """Return the most useful command error text available."""
        error_text = (stderr or "").strip() or (stdout or "").strip()
        return f"{prefix}{error_text}"

    def _execute_simple_query(self, query_cmd: str) -> str:
        """
        Common pattern: run a simple query and return stdout or error.
        """
        stdout, stderr, code = self.cli.execute(query_cmd)
        if code != 0:
            return self._format_command_error("Error executing command: ", stdout, stderr)
        return stdout


from ..cli_wrapper import DsmServWrapper


class BaseOfflineCommand(ABC):
    """Abstract base class for offline dsmserv utility commands."""

    def __init__(self, cli: DsmServWrapper):
        self.cli = cli

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def args_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> str:
        pass

    def _execute_utility(self, command: str) -> str:
        """Execute and return output."""
        stdout, stderr, code = self.cli.execute(command)
        if code != 0:
            return self._format_command_error("Error executing utility: ", stdout, stderr)
        return stdout

    def _format_command_error(self, prefix: str, stdout: str, stderr: str) -> str:
        """Return the most useful command error text available."""
        error_text = (stderr or "").strip() or (stdout or "").strip()
        return f"{prefix}{error_text}"


from ..cli_wrapper import ServermonWrapper


class BaseServermonCommand(ABC):
    """Abstract base class for servermon commands."""

    def __init__(self, cli: ServermonWrapper):
        self.cli = cli

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def args_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> str:
        pass

    def _execute_servermon(self, args: List[str]) -> str:
        stdout, stderr, code = self.cli.execute(args)
        if code != 0:
            return self._format_command_error("Error running servermon: ", stdout, stderr)
        return stdout

    def _format_command_error(self, prefix: str, stdout: str, stderr: str) -> str:
        """Return the most useful command error text available."""
        error_text = (stderr or "").strip() or (stdout or "").strip()
        return f"{prefix}{error_text}"