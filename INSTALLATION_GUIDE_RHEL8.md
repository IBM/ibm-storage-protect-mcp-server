# IBM Storage Protect MCP Server - RHEL 8 Installation Guide

This guide provides step-by-step instructions for installing the IBM Storage Protect MCP Server on Red Hat Enterprise Linux 8.

## Prerequisites Verification

Before starting, verify your system meets these requirements:

### 1. Verify RHEL Version
```bash
cat /etc/redhat-release
# Expected output: Red Hat Enterprise Linux release 8.x
```

### 2. Verify Root/Sudo Access
```bash
sudo whoami
# Expected output: root
```

### 3. Verify dsmadmc Installation
```bash
which dsmadmc
# Should return path like: /usr/bin/dsmadmc or /opt/tivoli/tsm/client/ba/bin/dsmadmc

dsmadmc -help
# Should display help information
```

---

## Step 1: Install Python 3.10 or Higher

RHEL 8 comes with Python 3.6 by default, but this MCP server requires Python 3.10+.

### Option A: Install Python 3.11 from AppStream (Recommended)

```bash
# Enable the required module
sudo dnf module list python3*

# Install Python 3.11
sudo dnf install python3.11 python3.11-pip python3.11-devel -y

# Verify installation
python3.11 --version
# Expected output: Python 3.11.x
```

### Option B: Install Python 3.10 from EPEL

```bash
# Enable EPEL repository
sudo dnf install epel-release -y

# Install Python 3.10
sudo dnf install python310 python310-pip python310-devel -y

# Verify installation
python3.10 --version
# Expected output: Python 3.10.x
```

### Set Python 3.11 as Default (Optional)

```bash
# Create alternatives
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.11 1

# Verify
python3 --version
pip3 --version
```

---

## Step 2: Install pip Package Manager

If pip is not already installed with Python:

```bash
# For Python 3.11
sudo dnf install python3.11-pip -y

# Or for Python 3.10
sudo dnf install python310-pip -y

# Upgrade pip to latest version
python3.11 -m pip install --upgrade pip

# Verify pip installation
pip3.11 --version
# or
python3.11 -m pip --version
```

---

## Step 3: Install Git (if not present)

```bash
# Check if git is installed
git --version

# If not installed, install it
sudo dnf install git -y

# Verify installation
git --version
# Expected output: git version 2.x.x
```

---

## Step 4: Install Additional Build Tools

Some Python packages may require compilation tools:

```bash
# Install development tools
sudo dnf groupinstall "Development Tools" -y

# Install additional required packages
sudo dnf install gcc gcc-c++ make openssl-devel bzip2-devel libffi-devel -y
```

---

## Step 5: Transfer MCP Server Project to RHEL Machine

### Option A: Clone from Git Repository (if available)

```bash
# Navigate to desired installation directory
cd /opt

# Clone the repository (replace with actual repository URL)
sudo git clone <repository-url> sp-mcp-server

# Change ownership to your user
sudo chown -R $USER:$USER sp-mcp-server

cd sp-mcp-server
```

### Option B: Transfer Files Manually

```bash
# On your local machine, create a tarball
tar -czf sp-mcp-server.tar.gz sp-mcp-server_admin_cli_capabilities/

# Transfer to RHEL machine using scp
scp sp-mcp-server.tar.gz user@rhel-server:/tmp/

# On RHEL machine, extract
cd /opt
sudo tar -xzf /tmp/sp-mcp-server.tar.gz
sudo mv sp-mcp-server_admin_cli_capabilities sp-mcp-server
sudo chown -R $USER:$USER sp-mcp-server
cd sp-mcp-server
```

### Option C: Use rsync

```bash
# From your local machine
rsync -avz --progress sp-mcp-server_admin_cli_capabilities/ user@rhel-server:/opt/sp-mcp-server/
```

---

## Step 6: Create pyproject.toml in Project Root

The project needs a `pyproject.toml` file in the root directory:

```bash
cd /opt/sp-mcp-server

# Copy the pyproject.toml from util directory to root
cp util/pyproject.toml .

# Verify the file exists
ls -la pyproject.toml
```

---

## Step 7: Install Python Dependencies

### Create a Virtual Environment (Recommended)

```bash
cd /opt/sp-mcp-server

# Create virtual environment using Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip in virtual environment
pip install --upgrade pip
```

### Install the MCP Server Package

```bash
# Install in development mode (editable install)
pip install -e .

# Or install normally
pip install .

# Verify installation
pip list | grep -E "mcp|ibm-sp"
# Should show: ibm-sp-mcp-server, mcp, python-dotenv
```

### Verify All Micro-MCP-Server Commands

```bash
# Check that all micro-mcp-server commands are available
which mcp-server-clients-core
which mcp-server-system-admin
which mcp-server-storage-pools

# Test help for one of them
mcp-server-clients-core --help
```

---

## Step 8: Configure Environment Variables

### Option A: Create .env File (Development)

```bash
cd /opt/sp-mcp-server

# Create .env file
cat > .env << 'EOF'
SP_SERVER_ADDRESS=your.isp.server.com
SP_ADMIN_ID=admin
SP_ADMIN_PASSWORD=your_secure_password
EOF

# Secure the .env file
chmod 600 .env
```

### Option B: Set System Environment Variables (Production)

```bash
# Add to user's profile
cat >> ~/.bashrc << 'EOF'

# IBM Storage Protect MCP Server Configuration
export SP_SERVER_ADDRESS="your.isp.server.com"
export SP_ADMIN_ID="admin"
export SP_ADMIN_PASSWORD="your_secure_password"
EOF

# Reload profile
source ~/.bashrc

# Verify
echo $SP_SERVER_ADDRESS
```

### Option C: Create Systemd Environment File (Production Service)

```bash
# Create environment file
sudo mkdir -p /etc/sp-mcp-server
sudo cat > /etc/sp-mcp-server/environment << 'EOF'
SP_SERVER_ADDRESS=your.isp.server.com
SP_ADMIN_ID=admin
SP_ADMIN_PASSWORD=your_secure_password
EOF

# Secure the file
sudo chmod 600 /etc/sp-mcp-server/environment
sudo chown root:root /etc/sp-mcp-server/environment
```

---

## Step 9: Verify dsmadmc is in System PATH

```bash
# Check if dsmadmc is in PATH
which dsmadmc

# If not found, add it to PATH
# Find dsmadmc location
find /opt /usr -name dsmadmc 2>/dev/null

# Add to PATH (example if found in /opt/tivoli/tsm/client/ba/bin/)
echo 'export PATH=$PATH:/opt/tivoli/tsm/client/ba/bin' >> ~/.bashrc
source ~/.bashrc

# Verify again
which dsmadmc
dsmadmc -help
```

---

## Step 10: Test the MCP Server Installation

### Test 1: Verify Python Package Installation

```bash
cd /opt/sp-mcp-server
source venv/bin/activate  # If using virtual environment

# Check installed packages
pip list | grep -E "mcp|ibm-sp"

# Verify all entry points
python -c "from importlib.metadata import entry_points; eps = entry_points(); print([ep.name for ep in eps.select(group='console_scripts') if 'mcp-server' in ep.name])"
```

### Test 2: Test Unified Server

```bash
# Set environment variables if not already set
export SP_SERVER_ADDRESS="your.isp.server.com"
export SP_ADMIN_ID="admin"
export SP_ADMIN_PASSWORD="your_password"

# Test in read-only mode first (safer)
python -m sp_mcp_server.main --mode read-only --enable-servers system

# The server should start and display available tools
# Press Ctrl+C to stop
```

### Test 3: Test Micro-MCP-Server

```bash
# Test a specific micro-mcp-server
mcp-server-system-admin

# Should start the server and display available tools
# Press Ctrl+C to stop
```

### Test 4: Verify dsmadmc Connectivity

```bash
# Test connection to ISP server
dsmadmc -id=$SP_ADMIN_ID -password=$SP_ADMIN_PASSWORD -server=$SP_SERVER_ADDRESS "query status"

# Should return server status information
```

---

## Step 11: Configure for Production Use (Optional)

### Create Systemd Service File

```bash
# Create service file for a micro-mcp-server
sudo cat > /etc/systemd/system/mcp-server-system-admin.service << 'EOF'
[Unit]
Description=IBM Storage Protect MCP Server - System Admin
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/opt/sp-mcp-server
EnvironmentFile=/etc/sp-mcp-server/environment
ExecStart=/opt/sp-mcp-server/venv/bin/mcp-server-system-admin
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable mcp-server-system-admin
sudo systemctl start mcp-server-system-admin

# Check status
sudo systemctl status mcp-server-system-admin

# View logs
sudo journalctl -u mcp-server-system-admin -f
```

### Configure Firewall (if needed)

```bash
# If the MCP server needs to accept connections
sudo firewall-cmd --permanent --add-port=<port>/tcp
sudo firewall-cmd --reload
```

---

## Troubleshooting

### Issue: Python version too old

```bash
# Verify Python version
python3 --version

# If < 3.10, follow Step 1 to install Python 3.11
```

### Issue: pip install fails with "No module named 'hatchling'"

```bash
# Install build dependencies
pip install --upgrade pip setuptools wheel hatchling
pip install -e .
```

### Issue: dsmadmc not found

```bash
# Find dsmadmc
sudo find / -name dsmadmc 2>/dev/null

# Add to PATH
export PATH=$PATH:/path/to/dsmadmc/directory
```

### Issue: Permission denied errors

```bash
# Ensure proper ownership
sudo chown -R $USER:$USER /opt/sp-mcp-server

# Ensure virtual environment is activated
source /opt/sp-mcp-server/venv/bin/activate
```

### Issue: Connection to ISP server fails

```bash
# Test network connectivity
ping your.isp.server.com

# Test dsmadmc directly
dsmadmc -id=admin -password=password -server=your.isp.server.com "query status"

# Check firewall rules
sudo firewall-cmd --list-all
```

---

## Quick Reference Commands

```bash
# Activate virtual environment
source /opt/sp-mcp-server/venv/bin/activate

# Run unified server (all modules)
python -m sp_mcp_server.main

# Run unified server (specific modules, read-only)
python -m sp_mcp_server.main --enable-servers system,clients --mode read-only

# Run micro-mcp-servers
mcp-server-clients-core
mcp-server-system-admin
mcp-server-storage-pools
mcp-server-policies-lifecycle
mcp-server-ops-protection

# Check service status
sudo systemctl status mcp-server-system-admin

# View logs
sudo journalctl -u mcp-server-system-admin -f

# Deactivate virtual environment
deactivate
```

---

## Next Steps

1. **Configure Claude Desktop** (if using): Update `claude_desktop_config.json` with the appropriate MCP server configuration
2. **Test with AI Assistant**: Verify the server works correctly with your AI assistant
3. **Set up monitoring**: Configure logging and monitoring for production use
4. **Security hardening**: Review and implement security best practices
5. **Backup configuration**: Document and backup your configuration files

---

## Additional Resources

- **Project README**: `/opt/sp-mcp-server/README.md`
- **Module Documentation**: `/opt/sp-mcp-server/docs/`
- **Test Scenarios**: `/opt/sp-mcp-server/tests/docs/`
- **MCP Protocol**: https://modelcontextprotocol.io/

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the project documentation in `/opt/sp-mcp-server/docs/`
3. Check system logs: `sudo journalctl -xe`
4. Verify environment variables are set correctly