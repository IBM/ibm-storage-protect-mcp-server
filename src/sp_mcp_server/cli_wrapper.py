import subprocess
import shutil
import os
import glob
from typing import List, Tuple, Dict, Any, Optional
import logging

from .config import ServerConfig

logger = logging.getLogger(__name__)

class DsmAdmcWrapper:
    def __init__(self, config: ServerConfig):
        self.config = config
        self.executable = shutil.which("dsmadmc")
        
        if not self.executable:
            # Fallback for common paths or assume it's in path even if which fails
            self.executable = "dsmadmc"

    def execute(self, command: str) -> Tuple[str, str, int]:
        """
        Execute a dsmadmc command.
        Returns (stdout, stderr, return_code).
        """
        if not self.config.validate():
            return "", "Configuration incomplete. Missing required environment variables.", 1

        # Base arguments for non-interactive authentication and formatting
        args = [
            self.executable,
            "-NOConfirm",
            "-DATAONLY=YES",
            f"-ID={self.config.admin_id}",
            f"-PA={self.config.admin_password}",
            "-COMMAdelimited" # Use comma delimited for easier parsing
        ]

        # Append the actual query command
        # command should be something like "QUERY SESSION" or "QUERY STATUS"
        # We split it into parts to pass as separate arguments
        cmd_parts = command.split()
        args.extend(cmd_parts)

        try:
            logger.info(f"Executing command: {command}")
            # Run the command
            process = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=False # We don't want to raise on non-zero exit, we handle it
            )
            
            return process.stdout, process.stderr, process.returncode
            
        except FileNotFoundError:
            return "", "dsmadmc executable not found. Please ensure it is in your PATH.", 127
        except Exception as e:
            return "", str(e), 1

class DsmServWrapper:
    """Wrapper for the offline dsmserv server utility."""
    def __init__(self, config: ServerConfig):
        self.config = config
        self.executable = self.config.dsmserv_path or shutil.which("dsmserv") or "dsmserv"

    def execute(self, command: str) -> Tuple[str, str, int]:
        """
        Execute a dsmserv command as the TSM instance user.
        Returns (stdout, stderr, return_code).
        """
        # dsmserv commands must be run as the TSM instance user (e.g., tsmsvr01)
        # to properly load shared libraries like libdb2.so.1
        
        args = [self.executable]
        
        # If instance directory is configured, add -i flag
        if self.config.server_instance_dir:
            args.extend(["-i", self.config.server_instance_dir])
            
        cmd_parts = command.split()
        args.extend(cmd_parts)
        
        try:
            # If instance user is configured, run command as that user
            if self.config.instance_user:
                # Use 'su' to switch to the instance user
                # Format: su - <user> -c "<command>"
                full_command = " ".join(args)
                su_args = ["su", "-", self.config.instance_user, "-c", full_command]
                logger.info(f"Executing offline command as {self.config.instance_user}: {full_command}")
                process = subprocess.run(
                    su_args,
                    capture_output=True,
                    text=True,
                    check=False
                )
            else:
                # Fallback to running as current user (may fail with library errors)
                logger.warning("SP_INSTANCE_USER not configured. Running dsmserv as current user may fail.")
                logger.info(f"Executing offline command: {' '.join(args)}")
                process = subprocess.run(
                    args,
                    capture_output=True,
                    text=True,
                    check=False
                )
            
            return process.stdout, process.stderr, process.returncode
        except FileNotFoundError:
            return "", f"dsmserv executable not found at '{self.executable}'. Please configure SP_DSMSERV_PATH.", 127
        except Exception as e:
            return "", str(e), 1

class ServermonWrapper:
    """Wrapper for the servermon diagnostic utility."""
    def __init__(self, config: ServerConfig):
        self.config = config
        self.executable = self.config.servermon_path or shutil.which("servermon") or "servermon"

    def _check_servermon_running(self) -> bool:
        """
        Check if another servermon instance is currently running.
        Returns True if servermon is running, False otherwise.
        """
        try:
            result = subprocess.run(
                ["pgrep", "-f", "servermon"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                logger.info(f"Found {len(pids)} servermon process(es) running: {', '.join(pids)}")
                return True
            return False
        except Exception as e:
            logger.warning(f"Error checking for servermon processes: {e}")
            return False

    def _get_latest_servermon_output(self) -> Optional[str]:
        """
        Get the most recent servermon output from the XML directory.
        Servermon creates timestamped subdirectories (e.g., .20260306T1159-SERVER1)
        with XML files inside a results/ subdirectory.
        Returns the content if found, None otherwise.
        """
        if not self.config.servermon_xml_dir or not os.path.isdir(self.config.servermon_xml_dir):
            logger.info("Servermon XML directory not configured or doesn't exist")
            return None
        
        try:
            # Look for timestamped subdirectories (pattern: .YYYYMMDDTHHMM-SERVERNAME)
            subdir_pattern = os.path.join(self.config.servermon_xml_dir, ".*-*")
            subdirs = glob.glob(subdir_pattern)
            
            # Filter to only directories
            subdirs = [d for d in subdirs if os.path.isdir(d)]
            
            if not subdirs:
                logger.info(f"No timestamped subdirectories found in {self.config.servermon_xml_dir}")
                return None
            
            # Get the most recent subdirectory
            latest_subdir = max(subdirs, key=os.path.getmtime)
            logger.info(f"Found latest servermon subdirectory: {latest_subdir}")
            
            # Look for XML files in the results subdirectory
            results_dir = os.path.join(latest_subdir, "results")
            if not os.path.isdir(results_dir):
                logger.info(f"No results directory found in {latest_subdir}")
                return None
            
            xml_pattern = os.path.join(results_dir, "*.xml")
            xml_files = glob.glob(xml_pattern)
            
            if not xml_files:
                logger.info(f"No XML files found in {results_dir}")
                return None
            
            # Get the most recent XML file
            latest_file = max(xml_files, key=os.path.getmtime)
            logger.info(f"Found latest servermon XML output: {latest_file}")
            
            # Read and return the content
            with open(latest_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return f"Using existing servermon diagnostics from: {latest_file}\n\n{content}"
            
        except Exception as e:
            logger.warning(f"Error reading servermon output files: {e}")
            return None

    def execute(self, args: List[str]) -> Tuple[str, str, int]:
        """
        Execute a servermon command as the TSM instance user.
        If another servermon is running, attempts to use existing output instead.
        Returns (stdout, stderr, return_code).
        """
        # Check if servermon is already running
        if self._check_servermon_running():
            logger.info("Another servermon instance is running. Attempting to use existing diagnostics...")
            
            # Try to get existing output
            existing_output = self._get_latest_servermon_output()
            if existing_output:
                logger.info("Successfully retrieved existing servermon diagnostics")
                return existing_output, "", 0
            
            # If no existing output found, return error
            logger.warning("No existing servermon output found")
            return "", "Another servermon instance is currently running and no recent diagnostics are available. Please wait for the running instance to complete or check the servermon XML directory.", 1
        
        # No running instance, proceed with execution
        full_cmd = [self.executable] + args
        
        try:
            # If instance user is configured, run command as that user
            if self.config.instance_user:
                # Use 'su' to switch to the instance user
                # Format: su - <user> -c "<command>"
                command_str = " ".join(full_cmd)
                su_args = ["su", "-", self.config.instance_user, "-c", command_str]
                logger.info(f"Executing servermon command as {self.config.instance_user}: {command_str}")
                process = subprocess.run(
                    su_args,
                    capture_output=True,
                    text=True,
                    check=False
                )
            else:
                # Fallback to running as current user (may fail with library errors)
                logger.warning("SP_INSTANCE_USER not configured. Running servermon as current user may fail.")
                logger.info(f"Executing servermon command: {' '.join(full_cmd)}")
                process = subprocess.run(
                    full_cmd,
                    capture_output=True,
                    text=True,
                    check=False
                )
            
            return process.stdout, process.stderr, process.returncode
        except FileNotFoundError:
            return "", f"servermon executable not found at '{self.executable}'. Please configure SP_SERVERMON_PATH.", 127
        except Exception as e:
            return "", str(e), 1
