# sp-mcpserver
Storage Protect MCP servers

## Configuration

### Environment Variables

The following environment variables are required or optional for proper operation:

#### Required Variables
- `SP_ADMIN_ID`: IBM Storage Protect administrator ID
- `SP_ADMIN_PASSWORD`: IBM Storage Protect administrator password

#### Optional Variables
- `TCPSERVERADDRESS`: Storage Protect server address
- `SP_SERVER_PORT` or `TCPPORT`: Server port (default: 1500)
- `SP_DSMSERV_PATH`: Path to dsmserv executable
- `SP_SERVER_INSTANCE_DIR`: Server instance directory
- `SP_SERVERMON_PATH`: Path to servermon executable
- `SP_SERVERMON_XML_DIR`: Directory for servermon XML files
- **`SP_INSTANCE_USER`**: TSM instance user (e.g., `tsmsvr01`) - **Required for dsmserv commands**

### Important: TSM Instance User

The `SP_INSTANCE_USER` environment variable is **critical** for running `dsmserv` commands. Without it, commands will fail with library loading errors such as:

```
/usr/bin/dsmserv: error while loading shared libraries: libdb2.so.1: cannot open shared object file: No such file or directory
```

This occurs because `dsmserv` must be executed as the TSM instance user (typically `tsmsvr01`) to properly load required shared libraries. The wrapper will use `su` to switch to this user when executing commands.

**Example configuration:**
```bash
export SP_INSTANCE_USER=tsmsvr01
```
