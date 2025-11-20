# Troubleshooting Guide

Common issues and solutions for the RRVA MCP Server.

## Error: "Unexpected ExceptionGroup occurred while connecting to MCP server"

This error typically occurs when ElevenLabs tries to use `STREAMABLE_HTTP` transport but the server doesn't support it properly.

### Solution 1: Use SSE Endpoint

The server now supports SSE (Server-Sent Events). Try these endpoints:

**In ElevenLabs configuration:**
- **Server URL**: `https://your-ngrok-url.ngrok-free.app`
- **Endpoint**: `/sse` (instead of `/mcp`)

Or try:
- **Endpoint**: `/mcp` (standard JSON-RPC)

### Solution 2: Check Server Logs

1. **Watch your server terminal** for incoming requests
2. **Check for error messages** when ElevenLabs connects
3. **Verify the endpoint** is being called correctly

### Solution 3: Test Endpoints Manually

```bash
# Test health
curl https://your-url.ngrok-free.app/health

# Test tools list
curl https://your-url.ngrok-free.app/tools

# Test SSE endpoint
curl -N https://your-url.ngrok-free.app/sse

# Test MCP endpoint
curl -X POST https://your-url.ngrok-free.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### Solution 4: Verify ngrok is Active

```bash
# Check ngrok status
# Visit http://localhost:4040 in browser
# Or check ngrok terminal for active connection
```

### Solution 5: Try Different Endpoints

In ElevenLabs, try these endpoint variations:
- `/mcp`
- `/sse`
- `/tools`
- `/tools/call`

## Error: "Connection Refused"

### Check 1: Server is Running

```bash
# Verify server is running
curl http://localhost:8000/health
```

### Check 2: ngrok is Running

```bash
# Check ngrok status
# Visit http://localhost:4040
```

### Check 3: Port is Correct

- Server should be on port 8000
- ngrok should forward to port 8000
- Check for port conflicts

## Error: "Tools Not Discovered"

### Solution 1: Wait for Discovery

- ElevenLabs may take 30-60 seconds to discover tools
- Refresh the agent settings page
- Check browser console (F12) for errors

### Solution 2: Verify Tools Endpoint

```bash
curl https://your-url.ngrok-free.app/tools
```

Should return JSON with 11 tools.

### Solution 3: Check CORS

The server has CORS enabled, but verify:
- Browser console shows no CORS errors
- Server logs show incoming requests

## Error: "Tool Calls Failing"

### Solution 1: Check Server Logs

Watch your server terminal for:
- Incoming tool call requests
- Error messages
- Response format

### Solution 2: Verify Tool Arguments

Check that tool is called with correct arguments:
- Required fields are present
- Data types match schema
- Values are valid

### Solution 3: Test Tool Manually

```bash
curl -X POST https://your-url.ngrok-free.app/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "verify_customer_identity",
    "arguments": {
      "order_id": "ORD-001",
      "email": "customer1@example.com"
    }
  }'
```

## Error: "ngrok Session Expired"

### Solution

1. Restart ngrok: `ngrok http 8000`
2. Get new URL
3. Update ElevenLabs configuration with new URL
4. Consider ngrok paid plan for fixed domains

## Error: "Internal Server Error"

### Check 1: Server Logs

Look for Python errors in server terminal:
- Import errors
- Syntax errors
- Runtime exceptions

### Check 2: Dependencies

```bash
pip install -r requirements.txt
```

### Check 3: Python Version

```bash
python --version
# Should be 3.9 or higher
```

## Debugging Steps

### Step 1: Enable Verbose Logging

Add to `mcp_server_http.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In endpoints, add:
logger.debug(f"Received request: {body}")
logger.debug(f"Response: {response}")
```

### Step 2: Monitor ngrok Traffic

Visit http://localhost:4040 to see:
- All HTTP requests
- Request/response details
- Headers and body

### Step 3: Test Each Endpoint

```bash
# Health
curl https://your-url.ngrok-free.app/health

# Tools list
curl https://your-url.ngrok-free.app/tools

# MCP initialize
curl -X POST https://your-url.ngrok-free.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'

# MCP tools/list
curl -X POST https://your-url.ngrok-free.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

### Step 4: Check ElevenLabs Console

1. Open browser developer tools (F12)
2. Go to Network tab
3. Try connecting in ElevenLabs
4. Look for failed requests
5. Check request/response details

## Common Configuration Issues

### Issue: Wrong Endpoint

**Symptoms:** Connection fails immediately

**Solution:** Try different endpoints:
- `/mcp` (standard)
- `/sse` (streaming)
- `/tools` (direct)

### Issue: CORS Errors

**Symptoms:** Browser console shows CORS errors

**Solution:** Server already has CORS enabled. If still issues:
- Check browser console for specific error
- Verify server is returning CORS headers
- Try different browser

### Issue: Timeout

**Symptoms:** Connection times out

**Solution:**
- Check server is running
- Check ngrok is active
- Verify firewall settings
- Test URL in browser first

## Getting Help

If issues persist:

1. **Collect Information:**
   - Server logs
   - ngrok web UI screenshots
   - ElevenLabs error messages
   - Browser console errors

2. **Test Endpoints:**
   - Run all test commands above
   - Document results

3. **Check Documentation:**
   - `NGROK_SETUP.md`
   - `ADD_MCP_TO_ELEVENLABS.md`
   - `ELEVENLABS_SETUP.md`

4. **Contact Support:**
   - ElevenLabs support (if ElevenLabs-specific)
   - Check server GitHub issues
   - Review MCP protocol documentation

## Quick Fixes

### Restart Everything

```bash
# 1. Stop server (Ctrl+C)
# 2. Stop ngrok (Ctrl+C)
# 3. Restart server
python mcp_server_http.py

# 4. Restart ngrok (new terminal)
ngrok http 8000

# 5. Update ElevenLabs with new URL
```

### Verify Setup

```bash
# 1. Test server locally
curl http://localhost:8000/health

# 2. Test via ngrok
curl https://your-url.ngrok-free.app/health

# 3. Test tools
curl https://your-url.ngrok-free.app/tools
```

### Check Versions

```bash
python --version  # Should be 3.9+
pip list | grep -E "(fastapi|uvicorn|mcp)"
```

---

**Still stuck?** Review the error message carefully and check the specific endpoint/transport type being used.

