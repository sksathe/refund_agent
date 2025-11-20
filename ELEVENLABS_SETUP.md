# ElevenLabs MCP Server Configuration Guide

Step-by-step guide to connect your RRVA MCP Server with ElevenLabs Conversational AI.

## Prerequisites

- ✅ Python 3.9+ installed
- ✅ ElevenLabs account with Conversational AI access
- ✅ MCP server code installed and tested

## Step 1: Prepare Your MCP Server

### 1.1 Install Dependencies

```bash
cd S:\R-Spike-5-1
pip install -r requirements.txt
```

### 1.2 Test the Server

```bash
# Test that tools work
python test_server.py

# Test that server starts (will wait for input via stdio)
python mcp_server.py
```

Press `Ctrl+C` to stop the test. The server is ready if it starts without errors.

## Step 2: Choose Transport Method

### Option A: HTTP/SSE Transport (via ngrok) - Recommended for Remote Access

**📘 See [`NGROK_SETUP.md`](NGROK_SETUP.md) for detailed ngrok setup instructions.**

Quick setup:
1. Start HTTP server: `python mcp_server_http.py`
2. Start ngrok: `ngrok http 8000`
3. Use ngrok URL in ElevenLabs configuration

### Option B: stdio Transport (Local Only)

Use this if ElevenLabs is running on the same machine.

## Step 3: Configure ElevenLabs Conversational AI

### Option A: Using ElevenLabs Dashboard (Recommended)

1. **Log in to ElevenLabs Dashboard**
   - Go to https://elevenlabs.io
   - Navigate to **Conversational AI** or **Agents** section

2. **Create or Edit Your Agent**
   - Click "Create Agent" or select an existing agent
   - Go to **Settings** or **Configuration**

3. **Enable Function Calling / Tools**
   - Look for **"Tools"**, **"Functions"**, or **"MCP"** section
   - Enable the feature if it's disabled

4. **Add MCP Server Connection**
   - Click **"Add MCP Server"** or **"Connect Custom Tools"**
   - Configure as follows:

   **For HTTP/ngrok:**
   ```
   Server Name: RRVA Refund Resolution Server
   Transport: https
   Server URL: https://your-ngrok-url.ngrok-free.app
   Endpoint: /mcp
   ```

   **For stdio (local):**
   ```
   Server Name: RRVA Refund Resolution Server
   Transport: stdio
   Command: python
   Arguments: S:\R-Spike-5-1\mcp_server.py
   Working Directory: S:\R-Spike-5-1
   ```

5. **Verify Connection**
   - ElevenLabs should automatically discover tools via `list_tools()`
   - You should see 11 tools listed:
     - verify_customer_identity
     - send_otp
     - verify_otp
     - get_order_history
     - get_transaction_history
     - check_refund_eligibility
     - execute_refund
     - get_refund_receipt
     - log_decision
     - store_artifact

### Option B: Using ElevenLabs API

If configuring via API, use this configuration:

```json
{
  "agent_id": "your-agent-id",
  "tools": {
    "mcp_servers": [
      {
        "name": "rrva-mcp-server",
        "command": "python",
        "args": ["S:\\R-Spike-5-1\\mcp_server.py"],
        "cwd": "S:\\R-Spike-5-1",
        "transport": "stdio"
      }
    ]
  }
}
```

## Step 3: Configure Agent System Prompt

Add this to your agent's system prompt or instructions:

```
You are a professional customer service agent handling refund requests.

WORKFLOW:
1. When a customer requests a refund, first verify their identity using verify_customer_identity with their order ID
2. If basic verification succeeds but recommends OTP, offer to send OTP for enhanced security
3. Retrieve their order history using get_order_history
4. Check refund eligibility using check_refund_eligibility
5. If eligible, execute the refund using execute_refund
6. Always log decisions using log_decision after processing
7. Store conversation artifacts using store_artifact

IMPORTANT:
- Always confirm order details back to the customer
- Explain each step clearly
- If refund is not eligible, explain why and offer alternatives (exchange, store credit, escalation)
- Be empathetic and professional
- Never process refunds without verifying identity first
```

## Step 4: Test the Integration

### 4.1 Start Your MCP Server

Keep the server running in a terminal:

```bash
python mcp_server.py
```

The server will wait for JSON-RPC messages via stdin/stdout.

### 4.2 Test via ElevenLabs Interface

1. **Open ElevenLabs Test Interface**
   - Go to your agent in the dashboard
   - Click "Test" or "Try Agent"

2. **Simulate a Customer Call**
   - Say: "I'd like a refund for order ORD-001"
   - The agent should call `verify_customer_identity`

3. **Verify Tool Calls**
   - Check the MCP server terminal for tool call logs
   - Check ElevenLabs dashboard for tool execution logs
   - Verify responses are returned correctly

### 4.3 Expected Flow

```
Customer: "I need a refund for order ORD-001"
Agent: "I can help with that. Can you confirm your email address?"
Customer: "customer1@example.com"
Agent: [Calls verify_customer_identity(order_id="ORD-001", email="customer1@example.com")]
Agent: "Thank you, I've verified your identity. Let me check your order..."
Agent: [Calls get_order_history(customer_id="CUST-001", order_id="ORD-001")]
Agent: "I see your order from January 15th for $149.99. What's the reason for the refund?"
Customer: "The product didn't work"
Agent: [Calls check_refund_eligibility(...)]
Agent: "Your refund is eligible. Processing now..."
Agent: [Calls execute_refund(...)]
Agent: "Your refund of $149.99 has been processed. You'll receive it in 5 business days."
```

## Step 5: Troubleshooting

### Issue: Tools Not Appearing

**Solution:**
1. Verify MCP server starts without errors
2. Check that `list_tools()` returns tools (test with `python test_server.py`)
3. Verify ElevenLabs can execute the Python command
4. Check file paths are correct (use absolute paths)

### Issue: Tool Calls Failing

**Solution:**
1. Check MCP server terminal for error messages
2. Verify tool arguments match the schema
3. Test tools individually: `python test_server.py`
4. Check that customer_id is verified before use

### Issue: Server Not Starting

**Solution:**
1. Verify Python is in PATH: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check for syntax errors: `python -m py_compile mcp_server.py`
4. Verify all tool modules are importable

### Issue: Connection Timeout

**Solution:**
1. Ensure MCP server is running before starting ElevenLabs agent
2. Check that stdio transport is configured correctly
3. Verify working directory is set correctly
4. Try using full absolute paths

## Step 6: Production Deployment

### 6.1 Run as a Service (Windows)

Create a batch file `start_mcp_server.bat`:

```batch
@echo off
cd /d S:\R-Spike-5-1
python mcp_server.py
pause
```

Or use Windows Task Scheduler to run it as a service.

### 6.2 Monitor Logs

Add logging to track tool usage:

```python
# In mcp_server.py, add logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In call_tool function:
logger.info(f"Tool called: {name} with args: {arguments}")
```

### 6.3 Health Check

Create a simple health check endpoint (if using HTTP transport):

```python
# For future HTTP transport support
@app.route('/health')
def health():
    return {"status": "healthy", "tools": len(available_tools)}
```

## Alternative: HTTP/SSE Transport (Future)

If ElevenLabs supports HTTP/SSE transport, you can modify the server:

```python
# Instead of stdio_server, use HTTP server
from mcp.server.sse import sse_server

async def main():
    async with sse_server(port=8000) as server:
        await server.run()
```

Then configure ElevenLabs to connect to `http://localhost:8000`.

## Quick Reference

**MCP Server Command:**
```bash
python S:\R-Spike-5-1\mcp_server.py
```

**Test Tools:**
```bash
python S:\R-Spike-5-1\test_server.py
```

**Sample Customer:**
- Order ID: `ORD-001`
- Email: `customer1@example.com`
- Customer ID: `CUST-001`

**Storage Location:**
- `S:\R-Spike-5-1\storage\`

## Next Steps

1. ✅ MCP server configured
2. ✅ ElevenLabs agent connected
3. ✅ Tools discovered
4. ⏭️ Test with real scenarios
5. ⏭️ Monitor tool usage
6. ⏭️ Review decision logs in `storage/decision_logs/`

---

**Need Help?** Check the main `README.md` or `INTEGRATION.md` for more details.

