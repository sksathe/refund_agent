# ngrok Setup Guide for ElevenLabs Integration

This guide explains how to expose your MCP server to ElevenLabs using ngrok.

## Overview

Instead of using stdio transport, we'll run the MCP server as an HTTP server and expose it via ngrok. This allows ElevenLabs to connect to your server over the internet.

```
ElevenLabs → ngrok (public URL) → Your Local MCP Server (HTTP)
```

## Prerequisites

- ✅ Python 3.9+ installed
- ✅ MCP server dependencies installed
- ✅ ngrok account (free tier works)
- ✅ ElevenLabs account with Conversational AI access

## Step 1: Install ngrok

### Windows

1. Download ngrok from https://ngrok.com/download
2. Extract `ngrok.exe` to a folder (e.g., `C:\ngrok\`)
3. Add to PATH or use full path

### macOS

```bash
brew install ngrok/ngrok/ngrok
```

### Linux

```bash
# Download and install
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
```

## Step 2: Authenticate ngrok

1. **Sign up for ngrok account:**
   - Go to https://dashboard.ngrok.com/signup
   - Create a free account

2. **Get your auth token:**
   - Go to https://dashboard.ngrok.com/get-started/your-authtoken
   - Copy your authtoken

3. **Authenticate ngrok:**
   ```bash
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

## Step 3: Install HTTP Server Dependencies

```bash
pip install fastapi uvicorn[standard]
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

## Step 4: Start the HTTP MCP Server

### Option A: Direct Start

```bash
cd S:\R-Spike-5-1
python mcp_server_http.py
```

The server will start on `http://localhost:8000` by default.

### Option B: Custom Port

```bash
# Windows PowerShell
$env:PORT=8080
python mcp_server_http.py

# Or Linux/Mac
PORT=8080 python mcp_server_http.py
```

### Verify Server is Running

Open a browser and visit:
- Health check: http://localhost:8000/health
- Tools list: http://localhost:8000/tools
- Root: http://localhost:8000/

You should see JSON responses.

## Step 5: Expose Server with ngrok

### Start ngrok Tunnel

Open a **new terminal** and run:

```bash
ngrok http 8000
```

**Important:** Keep this terminal open! ngrok must stay running.

### Get Your Public URL

ngrok will display something like:

```
Forwarding   https://abc123.ngrok-free.app -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

### Test the Public URL

Open in browser:
- https://abc123.ngrok-free.app/health
- https://abc123.ngrok-free.app/tools

You should see the same responses as localhost.

## Step 6: Configure ElevenLabs

### In ElevenLabs Dashboard

1. **Navigate to your agent:**
   - Go to Conversational AI → Agents → Your Agent → Settings

2. **Enable Tools/Function Calling:**
   - Enable "Tools" or "Function Calling" feature

3. **Add MCP Server (HTTP):**
   - Click "Add MCP Server" or "Connect Custom Tools"
   - Configure:
     - **Transport**: `http` or `https`
     - **Server URL**: `https://abc123.ngrok-free.app` (your ngrok URL)
     - **Endpoint**: `/mcp` or `/tools/call`
     - **Authentication**: None (or add if required)

4. **Verify Connection:**
   - ElevenLabs should discover tools automatically
   - Check that 11 tools are listed

### Alternative: Direct Tool Endpoints

If ElevenLabs supports direct tool endpoints:

- **List Tools**: `https://abc123.ngrok-free.app/tools`
- **Call Tool**: `https://abc123.ngrok-free.app/tools/call`
- **MCP Endpoint**: `https://abc123.ngrok-free.app/mcp`

## Step 7: Test the Integration

1. **Keep both running:**
   - Terminal 1: `python mcp_server_http.py` (MCP server)
   - Terminal 2: `ngrok http 8000` (ngrok tunnel)

2. **Test in ElevenLabs:**
   - Start a test conversation
   - Try: "I'd like a refund for order ORD-001"
   - Watch the MCP server terminal for tool calls
   - Check ngrok terminal for HTTP requests

3. **Verify Tool Calls:**
   - Check `storage/decision_logs/` for decision logs
   - Review server console for tool execution logs

## Step 8: Production Considerations

### ngrok Limitations (Free Tier)

- **Session timeout**: Free tier sessions expire after 2 hours
- **Random URLs**: URL changes each time you restart ngrok
- **Request limits**: Limited requests per minute
- **Not for production**: Use only for development/testing

### Solutions for Production

1. **ngrok Paid Plan:**
   - Fixed domain names
   - No session timeouts
   - Higher request limits

2. **Deploy to Cloud:**
   - Deploy MCP server to AWS, Azure, or GCP
   - Use proper domain and SSL
   - No ngrok needed

3. **Self-Hosted Tunnel:**
   - Use Cloudflare Tunnel
   - Or deploy behind a reverse proxy

## Troubleshooting

### Issue: ngrok URL Not Accessible

**Solution:**
1. Verify ngrok is running: Check terminal
2. Check ngrok status: Visit http://localhost:4040 (ngrok web interface)
3. Verify MCP server is running on port 8000
4. Check firewall settings

### Issue: "Connection Refused"

**Solution:**
1. Ensure MCP server is running: `python mcp_server_http.py`
2. Verify port matches: Check ngrok command uses same port
3. Test localhost first: http://localhost:8000/health

### Issue: Tools Not Discovered

**Solution:**
1. Test tools endpoint: `https://your-ngrok-url.ngrok-free.app/tools`
2. Check JSON response format
3. Verify ElevenLabs endpoint configuration
4. Check CORS headers (server allows all origins)

### Issue: ngrok Session Expired

**Solution:**
1. Restart ngrok: `ngrok http 8000`
2. Get new URL
3. Update ElevenLabs configuration with new URL
4. Consider ngrok paid plan for fixed domains

### Issue: "ngrok: command not found"

**Solution:**
1. Verify ngrok is installed: `ngrok version`
2. Add to PATH or use full path
3. Reinstall ngrok if needed

## Monitoring

### ngrok Web Interface

Visit http://localhost:4040 to see:
- Request/response logs
- Request details
- Replay requests
- Inspect headers

### MCP Server Logs

Watch the server terminal for:
- Tool calls
- Request logs
- Error messages

### Check Storage

Monitor `storage/` directory:
- `storage/decision_logs/` - Decision logs
- `storage/receipts/` - Refund receipts
- `storage/transcripts/` - Conversation transcripts

## Quick Reference

**Start MCP Server:**
```bash
python mcp_server_http.py
```

**Start ngrok:**
```bash
ngrok http 8000
```

**Test Endpoints:**
- Health: `https://your-url.ngrok-free.app/health`
- Tools: `https://your-url.ngrok-free.app/tools`
- MCP: `https://your-url.ngrok-free.app/mcp`

**ngrok Web UI:**
- http://localhost:4040

## Security Notes

⚠️ **For Development Only**

- ngrok free tier is not secure for production
- URLs are publicly accessible
- No authentication by default
- Consider adding API key authentication

**Add Basic Auth (Optional):**

Modify `mcp_server_http.py` to add authentication:
```python
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.post("/mcp")
async def mcp_endpoint(credentials: HTTPBasicCredentials = Security(security)):
    # Verify credentials
    ...
```

## Next Steps

1. ✅ MCP server running on HTTP
2. ✅ ngrok tunnel active
3. ✅ ElevenLabs configured
4. ⏭️ Test with real scenarios
5. ⏭️ Monitor tool usage
6. ⏭️ Plan production deployment

---

**Need Help?** Check the main `README.md` or `ELEVENLABS_SETUP.md` for more details.

