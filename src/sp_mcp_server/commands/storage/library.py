from typing import Any, Dict
from ..base import BaseCommand

class DefineLibrary(BaseCommand):
    @property
    def name(self) -> str:
        return "define_library"

    @property
    def description(self) -> str:
        return (
            "Defines a **Tape Library** configuration physically or logically connected to the server.\n"
            "**Input Parameters**:\n"
            "- library_name (Required): Unique name for the library.\n"
            "- lib_type (Required): The interface type (e.g., 'SCSI', 'VTL', 'SHARED').\n"
            "- shared (Optional): 'YES' if the library is shared via SAN, 'NO' otherwise.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the library was defined."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "library_name": {"type": "string", "description": "Library name."},
                "lib_type": {
                    "type": "string",
                    "description": "Type of library (e.g. SCSI, SHARED, VTL)."
                },
                "shared": {"type": "string", "enum": ["YES", "NO"], "description": "Shared library status."}
            },
            "required": ["library_name", "lib_type"]
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"DEFINE LIBRARY {arguments['library_name']} LIBTYPE={arguments['lib_type']}"
        if arguments.get("shared"):
            cmd += f" SHARED={arguments['shared']}"
        return self._execute_simple_query(cmd)

class UpdateLibrary(BaseCommand):
    @property
    def name(self) -> str:
        return "update_library"
    @property
    def description(self) -> str:
        return (
            "Updates a **Library** definition.\n"
            "**Input Parameters**:\n"
            "- library_name (Required): The name of the library.\n"
            "- shared (Optional): 'YES' or 'NO' to indicate if shared.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the library was updated."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "library_name": {"type": "string", "description": "Library name."},
                "shared": {"type": "string", "enum": ["YES", "NO"], "description": "Shared status."}
            },
            "required": ["library_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = f"UPDATE LIBRARY {arguments['library_name']}"
        if arguments.get("shared"): cmd += f" SHARED={arguments['shared']}"
        return self._execute_simple_query(cmd)

class DeleteLibrary(BaseCommand):
    @property
    def name(self) -> str:
        return "delete_library"
    @property
    def description(self) -> str:
        return (
            "Deletes a **Library** definition.\n"
            "**Input Parameters**:\n"
            "- library_name (Required): The name of the library to delete.\n"
            "**Output Parameters**:\n"
            "- Result: Success message indicating the library was deleted."
        )
    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "library_name": {"type": "string", "description": "Library name."}
            },
            "required": ["library_name"]
        }
    def execute(self, arguments: Dict[str, Any]) -> str:
        return self._execute_simple_query(f"DELETE LIBRARY {arguments['library_name']}")

class QueryTapeLibrary(BaseCommand):
    @property
    def name(self) -> str:
        return "query_tape_library"

    @property
    def description(self) -> str:
        return (
            "Display information about tape libraries defined in the system.\n\n"
            "**Input Parameters**:\n"
            "- library_name (Optional): Name of the library.\n\n"
            "**Output Parameters**:\n"
            "- Library Name: Name of the library.\n"
            "- Library Type: Type of library (e.g., SCSI, SHARED).\n"
            "- Device: Device identifier."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "library_name": {"type": "string", "description": "Name of the library."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY LIBRARY"
        if arguments.get("library_name"):
            cmd += f" {arguments['library_name']}"
        return self._execute_simple_query(cmd)

class QueryLibraryVolume(BaseCommand):
    @property
    def name(self) -> str:
        return "query_library_volume"

    @property
    def description(self) -> str:
        return (
            "Query specific volumes physically located within a tape library.\n\n"
            "**Input Parameters**:\n"
            "- library_name (Optional): Library name.\n"
            "- volume_name (Optional): Volume name.\n\n"
            "**Output Parameters**:\n"
            "- Library Name: Name of the library.\n"
            "- Volume Name: Name of the volume.\n"
            "- Status: Current status (e.g., Private, Scratch).\n"
            "- Owner: Owner of the volume (for private volumes)."
        )

    @property
    def args_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "library_name": {"type": "string", "description": "Library name."},
                "volume_name": {"type": "string", "description": "Volume name."}
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        cmd = "QUERY LIBVOLUME"
        if arguments.get("library_name"):
            cmd += f" {arguments['library_name']}"
        if arguments.get("volume_name"):
            cmd += f" {arguments['volume_name']}"
        return self._execute_simple_query(cmd)
