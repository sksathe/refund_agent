# ElevenLabs MCP Server Configuration Examples

## Configuration File Format

If ElevenLabs uses a configuration file, here are examples:

### JSON Configuration

```json
{
  "agent": {
    "name": "Refund Resolution Agent",
    "voice_id": "your-voice-id",
    "system_prompt": "You are a professional customer service agent handling refund requests..."
  },
  "mcp_servers": [
    {
      "name": "rrva-mcp-server",
      "command": "python",
      "args": [
        "S:\\R-Spike-5-1\\mcp_server.py"
      ],
      "cwd": "S:\\R-Spike-5-1",
      "transport": "stdio",
      "env": {}
    }
  ],
  "tool_settings": {
    "approval_mode": "always_ask",
    "timeout": 30
  }
}
```

### YAML Configuration

```yaml
agent:
  name: "Refund Resolution Agent"
  voice_id: "your-voice-id"
  system_prompt: |
    You are a professional customer service agent handling refund requests.
    Always verify identity first, check eligibility, then process refunds.

mcp_servers:
  - name: rrva-mcp-server
    command: python
    args:
      - S:\R-Spike-5-1\mcp_server.py
    cwd: S:\R-Spike-5-1
    transport: stdio

tool_settings:
  approval_mode: always_ask
  timeout: 30
```

### Environment Variables

If configuring via environment variables:

```bash
# Windows PowerShell
$env:MCP_SERVER_COMMAND="python"
$env:MCP_SERVER_ARGS="S:\R-Spike-5-1\mcp_server.py"
$env:MCP_SERVER_CWD="S:\R-Spike-5-1"
$env:MCP_TRANSPORT="stdio"
```

```bash
# Linux/Mac
export MCP_SERVER_COMMAND="python"
export MCP_SERVER_ARGS="S:\R-Spike-5-1\mcp_server.py"
export MCP_SERVER_CWD="S:\R-Spike-5-1"
export MCP_TRANSPORT="stdio"
```

## Windows Batch Script

Create `start_mcp_for_elevenlabs.bat`:

```batch
@echo off
echo Starting RRVA MCP Server for ElevenLabs...
cd /d S:\R-Spike-5-1
python mcp_server.py
pause
```

## PowerShell Script

Create `start_mcp_for_elevenlabs.ps1`:

```powershell
# Start RRVA MCP Server for ElevenLabs
Write-Host "Starting RRVA MCP Server..." -ForegroundColor Green
Set-Location "S:\R-Spike-5-1"
python mcp_server.py
```

## Verification Script

Create `verify_mcp_setup.py`:

```python
"""Verify MCP server is ready for ElevenLabs integration."""

import sys
import subprocess
import json
from pathlib import Path

def test_server_imports():
    """Test that server can be imported."""
    try:
        import mcp_server
        print("✅ MCP server imports successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_tools_import():
    """Test that tools can be imported."""
    try:
        from tools.identity import IdentityVerifier
        from tools.orders import OrderHistoryService
        from tools.policy import RefundPolicyEngine
        from tools.refunds import RefundExecutor
        from tools.audit import AuditLogger
        print("✅ All tool modules import successfully")
        return True
    except Exception as e:
        print(f"❌ Tool import failed: {e}")
        return False

def test_python_version():
    """Test Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version too old: {version.major}.{version.minor}")
        return False

def test_dependencies():
    """Test that dependencies are installed."""
    try:
        import mcp
        print("✅ MCP SDK installed")
        return True
    except ImportError:
        print("❌ MCP SDK not installed. Run: pip install -r requirements.txt")
        return False

def test_storage_dirs():
    """Test that storage directories exist or can be created."""
    storage = Path("storage")
    dirs = ["audio", "transcripts", "decision_logs", "receipts"]
    
    for dir_name in dirs:
        dir_path = storage / dir_name
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Storage directory ready: {dir_path}")
        except Exception as e:
            print(f"❌ Cannot create storage directory {dir_path}: {e}")
            return False
    return True

def main():
    """Run all verification tests."""
    print("=" * 50)
    print("RRVA MCP Server - Setup Verification")
    print("=" * 50)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Server Imports", test_server_imports),
        ("Tool Imports", test_tools_import),
        ("Storage Directories", test_storage_dirs),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All checks passed! MCP server is ready for ElevenLabs integration.")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Run verification:
```bash
python verify_mcp_setup.py
```

## Testing Connection

Once configured in ElevenLabs, test the connection:

1. **Start MCP Server:**
   ```bash
   python mcp_server.py
   ```

2. **In ElevenLabs Dashboard:**
   - Go to your agent
   - Check "Tools" section
   - You should see 11 tools listed
   - Try a test conversation

3. **Monitor Tool Calls:**
   - Watch the MCP server terminal for tool call logs
   - Check `storage/decision_logs/` for decision logs
   - Verify responses are returned correctly

## Common Path Issues (Windows)

If you encounter path issues:

**Use forward slashes:**
```
S:/R-Spike-5-1/mcp_server.py
```

**Or escape backslashes:**
```
S:\\R-Spike-5-1\\mcp_server.py
```

**Or use raw string:**
```python
r"S:\R-Spike-5-1\mcp_server.py"
```

**Or use Path object:**
```python
from pathlib import Path
path = Path("S:/R-Spike-5-1/mcp_server.py")
str(path)  # Use this in configuration
```

