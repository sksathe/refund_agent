# ElevenLabs Integration Guide

This guide explains how to integrate the RRVA MCP Server with ElevenLabs Conversational AI.

## Overview

The MCP server provides tools that the ElevenLabs agent can call during voice conversations to:
1. Verify customer identity
2. Retrieve order/transaction history
3. Check refund eligibility
4. Execute refunds
5. Log decisions and store artifacts

## Integration Steps

### 1. Set Up MCP Server

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the MCP server:
   ```bash
   python mcp_server.py
   ```

The server communicates via stdio (standard input/output) using JSON-RPC protocol.

### 2. Configure ElevenLabs Agent

**📋 See [`ADD_MCP_TO_ELEVENLABS.md`](ADD_MCP_TO_ELEVENLABS.md) for step-by-step instructions on adding MCP to your agent.**

**📋 See `ELEVENLABS_SETUP.md` for detailed step-by-step instructions.**

Quick setup:

1. **Enable Function Calling / Tools**
   - Navigate to your ElevenLabs dashboard → Conversational AI → Agents
   - Select your agent → Settings
   - Enable "Tools" or "Function Calling" feature

2. **Connect MCP Server**
   - Click "Add MCP Server" or "Connect Custom Tools"
   - Configure:
     - **Transport**: `stdio`
     - **Command**: `python`
     - **Arguments**: `S:\R-Spike-5-1\mcp_server.py` (or your path)
     - **Working Directory**: `S:\R-Spike-5-1`
   - The agent will automatically discover available tools via `list_tools()`

**Note**: Keep the MCP server running (`python mcp_server.py`) while using the agent.

3. **Configure Agent Prompt**
   Add instructions for the agent to use tools appropriately:

   ```
   You are a customer service agent handling refund requests.
   
   When a customer calls:
   1. First verify their identity using verify_customer_identity with their order ID
   2. If basic verification, offer to send OTP for enhanced verification
   3. Retrieve their order history using get_order_history
   4. Check refund eligibility using check_refund_eligibility
   5. If eligible, execute refund using execute_refund
   6. Always log decisions using log_decision
   7. Store conversation artifacts using store_artifact
   
   Be conversational, confirm key details back to the customer, and explain each step.
   ```

### 3. Tool Usage Patterns

#### Identity Verification Flow

```
Customer: "I'd like a refund for order ORD-001"
Agent: [Calls verify_customer_identity(order_id="ORD-001")]
Agent: "I can help with that. Can you confirm your email address?"
Customer: "customer1@example.com"
Agent: [Calls verify_customer_identity(order_id="ORD-001", email="customer1@example.com")]
Agent: "Thank you, I've verified your identity. Let me check your order..."
```

#### Refund Processing Flow

```
Agent: [Calls get_order_history(customer_id="CUST-001", order_id="ORD-001")]
Agent: "I see your order from January 15th for $149.99. What's the reason for the refund?"
Customer: "The product didn't work as expected"
Agent: [Calls check_refund_eligibility(order_id="ORD-001", customer_id="CUST-001", reason="Product didn't work")]
Agent: "Your refund is eligible. I'll process it now..."
Agent: [Calls execute_refund(order_id="ORD-001", customer_id="CUST-001", reason="Product didn't work")]
Agent: "Your refund of $149.99 has been processed. You'll receive it in 5 business days."
Agent: [Calls log_decision(...) and store_artifact(...)]
```

### 4. Error Handling

The agent should handle tool errors gracefully:

```
If verify_customer_identity returns error:
  - "I'm having trouble finding that order. Can you double-check the order number?"
  
If check_refund_eligibility returns eligible: false:
  - Explain the reason (outside window, condition, etc.)
  - Offer alternatives (exchange, store credit, escalation)
  
If execute_refund fails:
  - "I apologize, there was an issue processing the refund. Let me escalate this..."
```

### 5. Session Management

Each conversation should have a unique `session_id`:

```python
session_id = f"SESSION-{uuid.uuid4()}"
```

Use this session_id for:
- `log_decision(session_id=...)`
- `store_artifact(session_id=...)`

### 6. Testing

1. **Test Individual Tools:**
   ```bash
   python test_server.py
   ```

2. **Test Full Flow:**
   - Use ElevenLabs test interface
   - Simulate customer calls
   - Verify tool calls in logs
   - Check storage/ directory for artifacts

### 7. Production Considerations

#### Security
- Replace in-memory storage with secure database
- Implement proper authentication for MCP server
- Encrypt sensitive data in storage
- Add rate limiting

#### Monitoring
- Log all tool calls with timestamps
- Track success/failure rates
- Monitor latency
- Alert on errors

#### Compliance
- Ensure consent is captured
- Implement data retention policies
- Add redaction for sensitive information
- Maintain audit trails

## Example Agent Configuration (JSON)

```json
{
  "agent_name": "Refund Resolution Agent",
  "voice_id": "your-voice-id",
  "tools": {
    "provider": "mcp",
    "server": {
      "command": "python",
      "args": ["mcp_server.py"],
      "transport": "stdio"
    }
  },
  "system_prompt": "You are a helpful customer service agent...",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

## Troubleshooting

### Tools Not Available
- Verify MCP server is running
- Check server logs for errors
- Ensure `list_tools()` returns tools correctly

### Tool Calls Failing
- Check tool arguments match schema
- Verify customer_id is verified before use
- Review error messages in tool responses

### Storage Issues
- Ensure `storage/` directory is writable
- Check disk space
- Verify file permissions

## Support

For issues or questions:
- Review tool responses for error details
- Check `storage/decision_logs/` for decision logs
- Review server console output

---

**Note**: This is a PoC implementation. For production, add proper error handling, authentication, and monitoring.


