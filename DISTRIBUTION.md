# Distribution Guide

This document provides instructions for distributing and installing the IBM Storage Protect MCP Server package.

## Package Information

- **Package Name**: `ibm-sp-mcp-server`
- **Version**: 0.1.0
- **Distribution Files**:
  - `ibm_sp_mcp_server-0.1.0-py3-none-any.whl` (Wheel - recommended)
  - `ibm_sp_mcp_server-0.1.0.tar.gz` (Source distribution)

## Built Packages

The distributable packages are located in the `dist/` directory:

```
dist/
├── ibm_sp_mcp_server-0.1.0-py3-none-any.whl
└── ibm_sp_mcp_server-0.1.0.tar.gz
```

## Installation Methods

### Method 1: Install from Wheel (Recommended)

The wheel format is the preferred installation method as it's faster and doesn't require build tools.

```bash
pip install dist/ibm_sp_mcp_server-0.1.0-py3-none-any.whl
```

### Method 2: Install from Source Distribution

```bash
pip install dist/ibm_sp_mcp_server-0.1.0.tar.gz
```

### Method 3: Install with Optional Dependencies

For SSE (Server-Sent Events) support:

```bash
pip install dist/ibm_sp_mcp_server-0.1.0-py3-none-any.whl[sse]
```

For development tools:

```bash
pip install dist/ibm_sp_mcp_server-0.1.0-py3-none-any.whl[dev]
```

For testing tools:

```bash
pip install dist/ibm_sp_mcp_server-0.1.0-py3-none-any.whl[test]
```

### Method 4: Install All Optional Dependencies

```bash
pip install dist/ibm_sp_mcp_server-0.1.0-py3-none-any.whl[sse,dev,test]
```

## Verification

After installation, verify the package is installed correctly:

```bash
# Check installed version
pip show ibm-sp-mcp-server

# Verify command-line tools are available
sp-mcp-server --help
mcp-server-clients-core --help
mcp-server-system-admin --help
```

## Available Command-Line Tools

The package installs the following command-line tools:

### Main Server
- `sp-mcp-server` - Unified MCP server (all modules)

### Micro-MCP-Servers
- `mcp-server-clients-core` - Client node lifecycle management
- `mcp-server-clients-config` - Client options and associations
- `mcp-server-storage-pools` - Storage pools and volumes
- `mcp-server-storage-hardware` - Libraries, drives, and paths
- `mcp-server-storage-device` - Device classes and data movers
- `mcp-server-policies-lifecycle` - Policy domains and sets
- `mcp-server-policies-management` - Management classes and copy groups
- `mcp-server-system-admin` - Admin users and privileges
- `mcp-server-system-config` - Server configuration and monitoring
- `mcp-server-ops-protection` - DR, DB backup, and replication
- `mcp-server-ops-maintenance` - Data movement and reclamation
- `mcp-server-ops-rules` - Automation, alerts, and triggers

## Publishing to PyPI

### Prerequisites

1. Install publishing tools:
   ```bash
   pip install twine
   ```

2. Create accounts on:
   - [PyPI](https://pypi.org/) (production)
   - [TestPyPI](https://test.pypi.org/) (testing)

### Test Upload (TestPyPI)

First, test your package on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ ibm-sp-mcp-server
```

### Production Upload (PyPI)

Once tested, upload to production PyPI:

```bash
# Upload to PyPI
python -m twine upload dist/*

# Users can then install with:
pip install ibm-sp-mcp-server
```

### Using API Tokens (Recommended)

For secure uploads, use API tokens instead of passwords:

1. Generate an API token from PyPI/TestPyPI account settings
2. Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-testpypi-token-here
```

## Rebuilding the Package

To rebuild the distribution packages after making changes:

```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info

# Build new distributions
python -m build
```

Or use the installed build tool:

```bash
pyproject-build
```

## Package Contents

The distribution includes:

### Python Package
- All source code from `src/sp_mcp_server/`
- All command modules and subpackages

### Documentation
- `README.md` - Main documentation
- `LICENSE` - MIT License
- `docs/` - Module-specific documentation
- `tests/docs/` - Usage scenarios and examples

### Scripts
- `scripts/` - Helper scripts for running services

### Configuration
- `pyproject.toml` - Package metadata and build configuration
- `requirements-mcp-server.txt` - Runtime dependencies

## System Requirements

- Python 3.10 or higher
- IBM Storage Protect Administrative Client (`dsmadmc`) installed and in PATH
- Network access to IBM Storage Protect Server

## Environment Variables

Required environment variables for operation:

- `SP_SERVER_ADDRESS` - IBM Storage Protect server address
- `SP_ADMIN_ID` - Administrator user ID
- `SP_ADMIN_PASSWORD` - Administrator password

## Uninstallation

To remove the package:

```bash
pip uninstall ibm-sp-mcp-server
```

## Troubleshooting

### Import Errors

If you encounter import errors after installation:

```bash
# Verify installation
pip list | grep ibm-sp-mcp-server

# Reinstall if necessary
pip install --force-reinstall dist/ibm_sp_mcp_server-0.1.0-py3-none-any.whl
```

### Command Not Found

If command-line tools are not found:

```bash
# Check if scripts directory is in PATH
python -m site --user-base

# Add to PATH if needed (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$(python -m site --user-base)/bin"
```

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/yourusername/sp-mcp-server/issues
- Documentation: https://github.com/yourusername/sp-mcp-server/tree/main/docs

## License

This package is distributed under the MIT License. See LICENSE file for details.