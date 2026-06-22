# IBM Storage Protect MCP Server

The IBM Storage Protect Model Context Protocol (MCP) server enables natural language administration of IBM Storage Protect systems through AI-powered automation. Transform complex command-line operations into simple conversational interactions.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation and configuration](#installation-and-configuration)
  - [Linux/Unix installation](#linuxunix-installation)
  - [Windows installation](#windows-installation)
- [Environment variables ](#environment-variables)
- [Usage Examples](#usage-examples)
- [Reporting Issues and Feedback](#reporting-issues-and-feedback)
- [Contributing Code](#contributing-code)
- [Disclaimer](#disclaimer)

---

## Prerequisites

- IBM Storage Protect server
- Administrator credentials with appropriate permissions
- Access to the server instance user account (typically `tsmsvr01`)
- Python 3.11 and pip package manager
- Git for cloning the repository

---

## Installation

You can install the IBM Storage Protect MCP server on Linux/Unix systems or Windows systems. Choose the appropriate installation guide for your environment.

### Linux/Unix installation

Complete the following steps to install the MCP server on a Linux or Unix system.

#### Step 1: Install Python 3.11 and pip package manager

Ensure that Python 3.11 and pip are installed on your system. Verify the installation by running the following commands:

```python3 --version
pip3 --version
```

#### Step 2: Clone the repository

Navigate to `/opt` and clone the IBM Storage Protect MCP server repository:

```cd /opt
git clone https://github.com/IBM/ibm-storage-protect-mcp-server
cd ibm-storage-protect-mcp-server
git checkout dev
```

#### Step 3: Create pyproject.toml in the project root

Copy the configuration file from `util/` to the project root and verify:

```mkdir /opt/ibm-storage-protect-mcp-server
cd /opt/ibm-storage-protect-mcp-server
cp util/pyproject.toml .
ls -la pyproject.toml
```

#### Step 4: Create a virtual environment

Create and activate a Python 3.11 virtual environment, and then upgrade pip:

```python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

#### Step 5: Install the MCP server package

Install the package in editable mode and verify the installation:

```pip install -e .
pip list | grep -E "mcp|ibm-sp"
```

#### Step 6: Verify MCP server commands

Confirm that all MCP server commands are accessible:

```which mcp-server-clients-core
which mcp-server-system-admin
which mcp-server-storage-pools
```

Test the help output for one of the commands:

```mcp-server-clients-core --help
```

#### Step 7: Configure environment variables

Create a `.env` file in the project directory:

```cd /opt/ibm-storage-protect-mcp-server
vi .env
```

Add the following environment variables to the `.env` file:

```SP_ADMIN_ID="<admin_user_of_dsmadmc>"
SP_ADMIN_PASSWORD="<dsmadmc_admin_password>"
SP_INSTANCE_USER="tsm_instance_name_eg_tmsint1"
SP_SERVERMON_XML_DIR="<instance_home_path>/srvmon"
```

Restrict file permissions for security:

```chmod 600 .env
```

#### Step 8: Configure the MCP client

Add the following JSON configuration to your MCP client (Examples: Bob, Claude, or Cursor). Replace the placeholders with your actual host name and root password:

```json
{
  "mcpServers": {
    "<host_of_sp-mcp-server-name>": {
      "command": "sshpass",
      "args": [
        "-p",
        "<root_password>",
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        "root@<host_of_sp-mcp-server-name>",
        "cd /opt/ibm-storage-protect-mcp-server && source venv/bin/activate && python3 -m sp_mcp_server.main --mode full --enable-servers system,operations,clients,policy,storage"
      ],
      "disabled": false,
      "alwaysAllow": []
    }
  },
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "sidebarMode": "chat",
    "coworkWebSearchEnabled": true,
    "ccdScheduledTasksEnabled": false
  }
}
```

**Installation complete.** The MCP server is now ready to handle storage protection operations.

---

### Windows installation

Complete the following steps to install the MCP server on a Windows system that is `dsmadmc` is installed on Windows machine.

**Note:** The ability to login to the Storage Protect server with a dsmadmc client works regardless of the SP server platform (Linux/Windows/AIX). The SP MCP server (Python code) works on Windows as well. While the dsmadmc client can be on Windows, the Storage Protect server itself can be on Windows, Linux, or AIX.

#### Step 1: Install Python 3.11 and pip package manager

Ensure that Python 3.11 and pip are installed on your Windows system. Verify the installation by running the following commands:

```python3 --version
pip3 --version
```

#### Step 2: Clone the repository

Navigate to `C:\src\` and clone the IBM Storage Protect MCP server repository:

```cd C:\src\
git clone https://github.com/IBM/ibm-storage-protect-mcp-server
cd ibm-storage-protect-mcp-server
git checkout dev
```

#### Step 3: Create pyproject.toml in the project root

If needed, copy the configuration file from `util/` to the project root:

```cd C:\src\ibm-storage-protect-mcp-server
# cp util/pyproject.toml . (if needed)
ls -la pyproject.toml
```

#### Step 4: Create a virtual environment

Create and activate a Python 3.11 virtual environment:

```
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 5: Install the MCP server package

Install the package in editable mode:

```pip install -e .
```

#### Step 6: Verify all micro-MCP server commands

Confirm that all MCP server commands are accessible:

```where mcp-server-clients-core
where mcp-server-system-admin
where mcp-server-storage-pools
```

Example output:
```
C:\src\ibm-storage-protect-mcp-server>where mcp-server-system-admin
C:\Program Files\Python311\Scripts\mcp-server-system-admin.exe
```

Test the help output for one of the commands:

```powershell
mcp-server-clients-core --help
```

#### Step 7: Configure environment variables

Create a `.env` file in the project directory:

```cd C:\src\ibm-storage-protect-mcp-server
notepad .env
```

Add the following environment variables to the `.env` file:

```bash
SP_ADMIN_ID="<admin_user_of_dsmadmc>"
SP_ADMIN_PASSWORD="<dsmadmc_admin_password>"
SP_INSTANCE_USER="tsm_instance_name_eg_tmsint1"
SP_SERVERMON_XML_DIR="<instance_home_path>/srvmon"
```

#### Step 8: Set up SSH for remote connection

Complete the following steps to enable SSH access.

##### Generate an SSH key pair if not already generated

Run the following command to generate an SSH key pair:

```ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_windows
```

This command creates the following files:
- Private key: `~/.ssh/id_rsa_windows`
- Public key: `~/.ssh/id_rsa_windows.pub`

##### Copy the public key to the Windows machine

Run the following command to copy your public key to the Windows machine:

```ssh-copy-id -i ~/.ssh/id_rsa_windows.pub SPuser@<windows-machine-ip>
```

Alternatively, you can manually copy the public key:
1. Copy the content of `~/.ssh/id_rsa_windows.pub`
2. On the Windows machine, append the content to `C:\Users\SPuser\.ssh\authorized_keys`

##### Test the SSH connection

Verify that you can connect to the Windows machine without a password prompt:

```ssh -i ~/.ssh/id_rsa_windows SPuser@<windows-machine-ip>
```
Should connect without password prompt.
If the connection is successful, you can proceed to configure the MCP settings.

##### Configure MCP settings on Mac

Create or update the `~/.bob/settings/mcp_settings.json` file with the following configuration:

```{
  "mcpServers": {
    "sp-mcp-server-remote-windows": {
      "command": "ssh",
      "args": [
        "-i",
        "/Users/<your-username>/.ssh/id_rsa_windows",
        "SPuser@<windows-machine-ip>",
        "powershell",
        "-NoProfile",
        "-Command",
        "cd C:\\src\\ibm-storage-protect-mcp-server; $env:SP_MASTER_PASSWORD='Welcome1#'; python -m sp_mcp_server.main --mode full --enable-servers system,operations,clients,policy,storage"
      ],
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

#### Verify the installation

After you complete the installation, test the MCP server by running the following command:

```
"get list of mcp-servers and tools in sp-mcp-server-remote-windows"
```

You should see 195+ tools listed with explanations, confirming that the MCP server is running correctly.

---

## Environment variables 

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SP_ADMIN_ID` | IBM Storage Protect administrator ID | `admin` |
| `SP_ADMIN_PASSWORD` | IBM Storage Protect administrator password | `password123` |

#### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TCPSERVERADDRESS` | Storage Protect server address | - | `sp-server.example.com` |
| `SP_SERVER_PORT` or `TCPPORT` | Server port number | `1500` | `1500` |
| `SP_DSMSERV_PATH` | Path to `dsmserv` executable | - | `/opt/tivoli/tsm/server/bin/dsmserv` |
| `SP_SERVER_INSTANCE_DIR` | Server instance directory | - | `/tsminst1` |
| `SP_SERVERMON_PATH` | Path to servermon executable | - | `/opt/tivoli/tsm/server/bin/servermon` |
| `SP_SERVERMON_XML_DIR` | Directory for servermon XML files | - | `/tmp/servermon` |
| `SP_INSTANCE_USER` | TSM instance user (required for `dsmserv` commands) | - | `tsmsvr01` |

### IBM Storage Protect instance user configuration

The `SP_INSTANCE_USER` environment variable is **critical** for running `dsmserv` commands. This variable specifies the IBM Storage Protect instance user account that the MCP server uses to execute `dsmserv` commands.

**Why it's required:**
Without the `SP_INSTANCE_USER` variable, `dsmserv` commands fail with library loading errors. You must run the `dsmserv` executable as the IBM Storage Protect instance user (typically `tsmsvr01`) to properly load required shared libraries. The MCP server wrapper uses the `su` command to switch to the specified instance user when executing `dsmserv` commands.

**Example error when `SP_INSTANCE_USER` is not set:**
```
/usr/bin/dsmserv: error while loading shared libraries: libdb2.so.1: cannot open shared object file: No such file or directory
```

### Configuration Example

```bash
# Required variables
export SP_ADMIN_ID=admin
export SP_ADMIN_PASSWORD=mypassword

# Optional variables
export TCPSERVERADDRESS=sp-server.example.com
export SP_SERVER_PORT=1500
export SP_DSMSERV_PATH=/opt/tivoli/tsm/server/bin/dsmserv
export SP_SERVER_INSTANCE_DIR=/tsminst1
export SP_SERVERMON_PATH=/opt/tivoli/tsm/server/bin/servermon
export SP_SERVERMON_XML_DIR=/tmp/servermon
export SP_INSTANCE_USER=tsmsvr01
```

---

## Usage Examples

### Basic Queries

```bash
# Query system status
"What is the database status?"

# List active clients
"Show me all active clients"

# Check failed operations
"Show me all failed operations from the last 24 hours"
```

### Configuration Tasks

```bash
# Create storage resources
"Create a device class named file_class of type file"

# Configure tiering
"Tell me the steps to tier data from container storage pool to cloud storage pool"
```

### Monitoring and Diagnostics

```bash
# System monitoring
"How many threads are running?"

# Capacity analysis
"Analyze current capacity utilization and forecast storage exhaustion"
```

---

## Reporting Issues and Feedback

For issues, questions, or feature requests, open an issue in the repository.

---

## Contributing Code

Contributions are welcome through Pull Requests. Complete the following steps to contribute:

1. Fork the repository and create a new branch for your feature or bug fix
2. Make your changes by following the existing code style and conventions
3. Test your changes thoroughly to ensure that they work as expected
4. Submit a pull request with a clear description of your changes
5. Sign the Developer's Certificate of Origin (DCO) by adding your name and email address to the `DCO.md` file in your pull request

**Note:** Submit your first Pull Request against the Developer's Certificate of Origin (DCO) located at `DCO.md` by using your name and email address.

---

## Disclaimer

This software is provided "as is" without any warranties of any kind, including, but not limited to, warranties related to installation, use, or performance. IBM is not responsible for any damage, charges, or data loss incurred with the use of this software. You are responsible for reviewing and testing any scripts you run thoroughly before you use them in any production environment. This content is subject to change without notice.

