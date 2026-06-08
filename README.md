# IBM Storage Protect MCP Server

The IBM Storage Protect Model Context Protocol (MCP) server enables natural language administration of IBM Storage Protect systems through AI-powered automation. Transform complex command-line operations into simple conversational interactions.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)

---

## Overview

The IBM Storage Protect MCP server transforms traditional command-line administration into conversational interactions. Instead of memorizing complex command syntax, you can use natural language to:

- Manage backup and restore operations
- Configure storage resources and policies
- Monitor system health and performance
- Troubleshoot issues and analyze capacity

**Example:**
```
You: "Show me all failed operations from the last 24 hours"
MCP: [Executes query and returns formatted results]
```

### Why Use MCP Server?

- ✅ **Faster Onboarding** - New administrators become productive immediately
- ✅ **Reduced Errors** - Command validation prevents common mistakes
- ✅ **Increased Productivity** - Automate routine administrative tasks
- ✅ **Better Accessibility** - Makes storage management accessible to all skill levels

---

## Prerequisites

- IBM Storage Protect server
- Administrator credentials with appropriate permissions
- Access to the server instance user account (typically `tsmsvr01`)

---

## Configuration

### Environment Variables

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

## Architecture

The MCP server consists of modular components:

- **Client Management** - Manages client nodes and configurations
- **Storage Management** - Controls storage pools and device classes
- **Policy Management** - Administers retention policies and lifecycle rules
- **System Management** - Handles monitoring and performance optimization
- **Operations** - Manages backup, restore, and archive operations

For detailed architecture documentation, see the [official product documentation](https://www.ibm.com/docs/en/storage-protect).

---

---

## Troubleshooting

### Common Issues

#### Library Loading Error

**Error:**
```
/usr/bin/dsmserv: error while loading shared libraries: libdb2.so.1: cannot open shared object file
```

**Solution:**
Set the `SP_INSTANCE_USER` environment variable:
```bash
export SP_INSTANCE_USER=tsmsvr01
```

The `dsmserv` executable must run as the IBM Storage Protect instance user to properly load required shared libraries.


---

## Documentation

- Refer **[IBM Storage Protect Documentation](https://www.ibm.com/docs/en/storage-protect)** for complete IBM Storage Protect documentation.
