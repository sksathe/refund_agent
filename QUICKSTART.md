# Quick Start Guide

Get the RRVA MCP Server running in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test the tools (optional)
python test_server.py

# 3. Start the MCP server
python mcp_server.py
```

## Sample Customer Data

The PoC includes sample data:

**Customer 1:**
- Customer ID: `CUST-001`
- Email: `customer1@example.com`
- Phone: `+1234567890`
- Orders: `ORD-001`, `ORD-002`
- Last 4: `1234`

**Customer 2:**
- Customer ID: `CUST-002`
- Email: `customer2@example.com`
- Phone: `+1987654321`
- Orders: `ORD-003`
- Last 4: `5678`

## Quick Test

```python
# Test identity verification
from tools.identity import IdentityVerifier
import asyncio

verifier = IdentityVerifier()
result = asyncio.run(verifier.verify(
    order_id="ORD-001",
    email="customer1@example.com"
))
print(result)
```

## Integration with ElevenLabs

1. Configure your ElevenLabs agent to use this MCP server
2. Set transport to `stdio`
3. Point to: `python mcp_server.py`
4. The agent will auto-discover all 11 tools

See `INTEGRATION.md` for detailed integration steps.

## Available Tools

1. `verify_customer_identity` - Verify customer with order ID
2. `send_otp` - Send OTP for enhanced verification
3. `verify_otp` - Verify OTP code
4. `get_order_history` - Get customer orders
5. `get_transaction_history` - Get payment transactions
6. `check_refund_eligibility` - Check if refund is allowed
7. `execute_refund` - Process refund
8. `get_refund_receipt` - Get refund receipt
9. `log_decision` - Log decision for audit
10. `store_artifact` - Store audio/transcript/logs
11. `get_refund_receipt` - Retrieve receipt

## Storage

Artifacts are stored in `storage/`:
- `storage/audio/` - Audio recordings
- `storage/transcripts/` - Conversation transcripts
- `storage/decision_logs/` - Decision logs
- `storage/receipts/` - Refund receipts

## Next Steps

- Review `README.md` for full documentation
- Check `INTEGRATION.md` for ElevenLabs setup
- See `samples/test_scenarios.md` for test cases
- Run `python test_server.py` to test all tools

## Troubleshooting

**Server won't start:**
- Check Python version: `python --version` (needs 3.9+)
- Install dependencies: `pip install -r requirements.txt`

**Tools not working:**
- Verify sample data is loaded (check `tools/identity.py` and `tools/orders.py`)
- Check error messages in console

**Storage errors:**
- Ensure `storage/` directory is writable
- Check disk space

---

**Ready to integrate!** 🚀


