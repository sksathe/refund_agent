# How to Add MCP Server to ElevenLabs Agent

Step-by-step guide to connect your RRVA MCP Server to an ElevenLabs Conversational AI agent.

## Quick Start

1. **Start your MCP server** (HTTP via ngrok or stdio)
2. **Go to ElevenLabs Dashboard** → Conversational AI → Your Agent
3. **Enable Tools/Function Calling**
4. **Add MCP Server** with your server URL
5. **Verify tools are discovered** (should see 11 tools)

## Method 1: HTTP/ngrok (Recommended)

### Step 1: Start Your MCP Server

**Terminal 1 - Start HTTP Server:**
```bash
cd S:\R-Spike-5-1
python mcp_server_http.py
```

**Terminal 2 - Start ngrok:**
```bash
ngrok http 8000
```

**Copy your ngrok URL** (e.g., `https://abc123.ngrok-free.app`)

### Step 2: Add MCP Server in ElevenLabs Dashboard

1. **Log in to ElevenLabs**
   - Go to https://elevenlabs.io
   - Navigate to **Conversational AI** → **Agents**

2. **Select Your Agent**
   - Click on your agent
   - Go to **Settings** or **Configuration** tab

3. **Enable Function Calling / Tools**
   - Look for **"Tools"**, **"Functions"**, **"Function Calling"**, or **"MCP"** section
   - Toggle it **ON** if disabled

4. **Add MCP Server**
   - Click **"Add MCP Server"**, **"Connect Tools"**, or **"Add Custom Tools"**
   - You may see options like:
     - "Add MCP Server"
     - "Connect External Tools"
     - "Custom Functions"
     - "MCP Integration"

5. **Configure MCP Server Connection**
   
   Fill in the following fields:
   
   ```
   Name: RRVA Refund Resolution Server
   Server Type: HTTP/HTTPS or Custom MCP Server
   Server URL: https://abc123.ngrok-free.app
   Endpoint: /mcp
   ```
   
   **Alternative endpoints to try:**
   - `/mcp` (MCP JSON-RPC endpoint)
   - `/tools` (Direct tools list)
   - `/tools/call` (Direct tool call endpoint)

6. **Optional Settings**
   - **Secret Token**: Leave empty (unless you added auth)
   - **HTTP Headers**: Usually not needed
   - **Approval Mode**: Choose "Always Ask" or "Fine-Grained"

7. **Save Configuration**
   - Click **"Save"**, **"Connect"**, or **"Add Integration"**
   - Wait for ElevenLabs to discover tools (may take 10-30 seconds)

8. **Verify Tools Are Discovered**
   - You should see a list of 11 tools:
     - ✅ verify_customer_identity
     - ✅ send_otp
     - ✅ verify_otp
     - ✅ get_order_history
     - ✅ get_transaction_history
     - ✅ check_refund_eligibility
     - ✅ execute_refund
     - ✅ get_refund_receipt
     - ✅ log_decision
     - ✅ store_artifact

### Step 3: Test the Connection

1. **Test Tool Discovery**
   - In ElevenLabs dashboard, check the tools list
   - You should see all 11 tools with their descriptions

2. **Test with a Conversation**
   - Go to **"Test"** or **"Try Agent"** section
   - Start a conversation: "I'd like a refund for order ORD-001"
   - The agent should call `verify_customer_identity` tool
   - Check your MCP server terminal for tool call logs

## Method 2: stdio Transport (Local Only)

Use this if ElevenLabs is running on the same machine.

### Step 1: Start MCP Server

```bash
cd S:\R-Spike-5-1
python mcp_server.py
```

**Important:** Keep this terminal open! The server must stay running.

### Step 2: Configure in ElevenLabs

1. **Navigate to Agent Settings**
   - Go to your agent → Settings → Tools/MCP section

2. **Add MCP Server (stdio)**
   - Click **"Add MCP Server"**
   - Select **"stdio"** or **"Local Process"** transport

3. **Configure Command**
   ```
   Server Name: RRVA Refund Resolution Server
   Transport: stdio
   Command: python
   Arguments: S:\R-Spike-5-1\mcp_server.py
   Working Directory: S:\R-Spike-5-1
   ```

4. **Save and Verify**
   - Save configuration
   - Verify tools are discovered

## ElevenLabs Dashboard Navigation

The exact location may vary by UI version. Look for:

### Option A: Agent Settings
1. **Conversational AI** → **Agents** → **Your Agent**
2. **Settings** tab → **Tools** or **Functions** section
3. **Enable Function Calling** toggle
4. **Add MCP Server** button

### Option B: Integrations Section
1. **Conversational AI** → **Integrations** or **Connections**
2. **MCP Servers** or **Custom Tools**
3. **Add MCP Server** or **Connect External Tools**

### Option C: Advanced Settings
1. **Your Agent** → **Advanced** or **Configuration**
2. **Function Calling** or **Tools** section
3. **MCP Integration** option

## Configuration Details

### HTTP/ngrok Configuration

```
Field                  Value
─────────────────────────────────────────────────
Name                   RRVA Refund Resolution Server
Server Type            HTTP/HTTPS or Custom MCP
Server URL             https://abc123.ngrok-free.app
Endpoint               /mcp
Secret Token           (leave empty)
Approval Mode          Always Ask (recommended)
```

### stdio Configuration

```
Field                  Value
─────────────────────────────────────────────────
Name                   RRVA Refund Resolution Server
Transport              stdio
Command                python
Arguments              S:\R-Spike-5-1\mcp_server.py
Working Directory      S:\R-Spike-5-1
```

## Troubleshooting

### Tools Not Appearing

**Check 1: Server is Running**
```bash
# Test HTTP server
curl http://localhost:8000/health

# Test via ngrok
curl https://your-url.ngrok-free.app/health
```

**Check 2: Endpoint is Correct**
```bash
# Test tools endpoint
curl https://your-url.ngrok-free.app/tools

# Should return JSON with 11 tools
```

**Check 3: ElevenLabs Discovery**
- Wait 30-60 seconds after saving
- Refresh the agent settings page
- Check browser console for errors (F12)
- Look for error messages in ElevenLabs dashboard

**Check 4: CORS Issues**
- The HTTP server has CORS enabled for all origins
- If still having issues, check browser console

### Tool Calls Failing

**Check 1: Server Logs**
- Watch your MCP server terminal
- Look for incoming HTTP requests
- Check for error messages

**Check 2: Tool Arguments**
- Verify tool is called with correct arguments
- Check tool schema in `/tools` endpoint
- Compare with what ElevenLabs is sending

**Check 3: Response Format**
- Tools should return JSON
- Format: `{"content": [{"type": "text", "text": "..."}]}`
- Check server logs for actual responses

### Connection Timeout

**For HTTP/ngrok:**
- ✅ Ensure both server and ngrok are running
- ✅ Check ngrok URL is still active (free tier expires)
- ✅ Verify firewall isn't blocking
- ✅ Test URL in browser first

**For stdio:**
- ✅ Ensure Python is in PATH
- ✅ Verify file paths are correct
- ✅ Check file permissions
- ✅ Ensure server process is running

## Testing Your Setup

### Test 1: Health Check

```bash
# Local
curl http://localhost:8000/health

# Via ngrok
curl https://your-url.ngrok-free.app/health
```

Expected: `{"status": "healthy"}`

### Test 2: List Tools

```bash
curl https://your-url.ngrok-free.app/tools
```

Should return JSON with 11 tools.

### Test 3: Call a Tool

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

### Test 4: Full Conversation

1. Start test conversation in ElevenLabs
2. Say: "I need a refund for order ORD-001"
3. Watch MCP server terminal for tool calls
4. Verify agent responds appropriately

## Approval Modes

ElevenLabs offers different approval modes:

### Always Ask (Recommended)
- Agent requests permission before each tool use
- Most secure option
- Good for testing and production

### Fine-Grained Tool Approval
- Pre-select which tools can run automatically
- Some tools require approval, others don't
- Good for production with trusted tools

### No Approval
- All tools run automatically
- Use only with trusted MCP servers
- Not recommended for production

## Next Steps After Adding MCP

1. **Configure Agent Prompt**
   - Add instructions for tool usage
   - See `INTEGRATION.md` for prompt examples

2. **Test Scenarios**
   - Try different refund scenarios
   - See `samples/test_scenarios.md`

3. **Monitor Usage**
   - Check `storage/decision_logs/` for audit logs
   - Review tool call patterns
   - Monitor ngrok web UI: http://localhost:4040

4. **Production Setup**
   - Consider ngrok paid plan for fixed domains
   - Or deploy to cloud (AWS, Azure, GCP)
   - Add authentication/security
   - Set up monitoring

## Quick Reference

**Start HTTP Server:**
```bash
python mcp_server_http.py
```

**Start ngrok:**
```bash
ngrok http 8000
```

**Test Endpoints:**
- Health: `/health`
- Tools: `/tools`
- MCP: `/mcp`
- Call Tool: `/tools/call`

**Sample Customer:**
- Order ID: `ORD-001`
- Email: `customer1@example.com`
- Customer ID: `CUST-001`

**ngrok Web UI:**
- http://localhost:4040 (inspect requests)

---

## Still Having Issues?

1. **Check Documentation:**
   - `NGROK_SETUP.md` - Detailed ngrok setup
   - `ELEVENLABS_SETUP.md` - Comprehensive guide
   - `INTEGRATION.md` - Integration patterns

2. **Verify Server:**
   - Run `python test_server.py` to test tools
   - Check server logs for errors
   - Test endpoints manually with curl

3. **Check ElevenLabs:**
   - Review agent settings
   - Check for error messages
   - Try refreshing the page
   - Contact ElevenLabs support if needed

---

**Ready to go!** Your MCP server should now be connected to your ElevenLabs agent. 🚀
