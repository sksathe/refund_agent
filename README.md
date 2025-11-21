# Refund Resolution Voice Agent (RRVA)

A comprehensive MCP (Model Context Protocol) server for handling customer refund requests via voice AI. This system provides secure identity verification, order management, refund policy evaluation, and automated refund processing.

## Architecture

### System Overview

RRVA is built as an MCP server that integrates with voice AI platforms (like ElevenLabs) to provide a conversational refund processing system. The architecture follows a modular design with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                    Voice AI Platform                        │
│                  (ElevenLabs, etc.)                         │
└──────────────────────┬──────────────────────────────────────┘
                        │
                        │ MCP Protocol (HTTP/SSE or stdio)
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                   MCP Server Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ mcp_server.py│  │mcp_server_   │  │  Tool        │    │
│  │  (stdio)     │  │  http.py     │  │  Registry    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└───────────────────────┬──────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│   Identity   │ │   Orders    │ │  Policy    │
│  Verifier    │ │  Service    │ │  Engine    │
└──────────────┘ └─────────────┘ └────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│   Refunds    │ │    Audit    │ │  Resend    │
│  Executor    │ │   Logger    │ │   API      │
└──────────────┘ └─────────────┘ └────────────┘
```

### Core Components

#### 1. **MCP Server Layer**
- **`mcp_server.py`**: stdio-based server for local integrations
- **`mcp_server_http.py`**: HTTP/SSE server for remote access (via ngrok)

Both servers expose the same set of tools via the MCP protocol.

#### 2. **Tool Modules** (`tools/`)

- **`identity.py`** - `IdentityVerifier`
  - Customer identity verification via order ID and name
  - OTP generation and email delivery via Resend API
  - OTP verification with expiration and attempt limits

- **`orders.py`** - `OrderHistoryService`
  - Order history retrieval
  - Transaction history lookup
  - Order status and fulfillment tracking

- **`policy.py`** - `RefundPolicyEngine`
  - Refund eligibility evaluation
  - Policy rule enforcement (30-day window, item condition, etc.)
  - Restocking fee calculation

- **`refunds.py`** - `RefundExecutor`
  - Refund transaction creation
  - Payment reversal processing
  - Receipt generation

- **`audit.py`** - `AuditLogger`
  - Decision logging for compliance
  - Artifact storage (transcripts, receipts, audio)
  - Session tracking

### Verification Flow

The system uses a secure multi-step verification process:

```
1. Customer provides order ID
   ↓
2. verify_by_order_and_name(order_id, name)
   → Validates name matches order
   → Returns customer_id and email
   ↓
3. send_otp(customer_id, method="email")
   → Generates 6-digit OTP
   → Sends email via Resend API
   → Stores OTP with 10-minute expiration
   ↓
4. verify_otp(customer_id, otp_code)
   → Validates OTP code
   → Checks expiration and attempt limits
   → Returns verification status
   ↓
5. verify_customer_identity(order_id, customer_id, otp_code)
   → Final verification step
   → Enables access to order/refund operations
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Resend API account (for OTP emails)
- (Optional) ElevenLabs account for voice AI integration

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd refund_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   RESEND_API_KEY=re_your_api_key_here
   RESEND_FROM_EMAIL=noreply@yourdomain.com  # Optional, defaults to onboarding@resend.dev
   ```
   
   Get your Resend API key from [resend.com](https://resend.com)

### Running the Server

#### Option 1: HTTP Server (for remote access via ngrok)

```bash
python mcp_server_http.py
```

The server will start on `http://localhost:8000` by default.

**Endpoints:**
- Health check: `http://localhost:8000/health`
- List tools: `http://localhost:8000/tools`
- MCP endpoint: `http://localhost:8000/mcp`
- Tool call: `http://localhost:8000/tools/call`

#### Option 2: stdio Server (for local integrations)

```bash
python mcp_server.py
```

This server communicates via stdin/stdout, suitable for local MCP clients.

### Testing

Run the test suite to verify everything works:

```bash
python test_server.py
```

This will test:
- Identity verification flow
- Order history retrieval
- Refund eligibility checking
- Refund execution
- Audit logging

## 📡 API Reference

### Available Tools

The server exposes 11 tools via the MCP protocol:

#### Identity Verification

1. **`verify_by_order_and_name`**
   - Verifies customer by order ID and name
   - Returns customer_id and email if match found
   ```json
   {
     "order_id": "ORD-001",
     "name": "Sanjyot Sathe"
   }
   ```

2. **`send_otp`**
   - Sends OTP to customer's registered email
   - Uses Resend API for email delivery
   ```json
   {
     "customer_id": "CUST001",
     "method": "email"
   }
   ```

3. **`verify_otp`**
   - Verifies OTP code provided by customer
   ```json
   {
     "customer_id": "CUST001",
     "otp_code": "123456"
   }
   ```

4. **`verify_customer_identity`**
   - Final verification step requiring OTP
   ```json
   {
     "order_id": "ORD-001",
     "customer_id": "CUST001",
     "otp_code": "123456"
   }
   ```

#### Order Management

5. **`get_order_history`**
   - Retrieves order history for a customer
   ```json
   {
     "customer_id": "CUST001",
     "order_id": "ORD-001",  // Optional
     "limit": 10  // Optional
   }
   ```

6. **`get_transaction_history`**
   - Retrieves transaction/payment history for an order
   ```json
   {
     "order_id": "ORD-001",
     "customer_id": "CUST001"
   }
   ```

#### Refund Processing

7. **`check_refund_eligibility`**
   - Evaluates refund eligibility based on policy rules
   ```json
   {
     "order_id": "ORD-001",
     "customer_id": "CUST001",
     "reason": "Product defect",
     "item_ids": ["ITEM001"]  // Optional
   }
   ```

8. **`execute_refund`**
   - Executes refund for eligible orders
   ```json
   {
     "order_id": "ORD-001",
     "customer_id": "CUST001",
     "reason": "Product defect",
     "refund_method": "original_payment",  // or "store_credit"
     "item_ids": ["ITEM001"],  // Optional
     "refund_amount": 99.99  // Optional, calculated if not provided
   }
   ```

9. **`get_refund_receipt`**
   - Retrieves refund receipt
   ```json
   {
     "refund_id": "REF123456"
   }
   ```

#### Audit & Logging

10. **`log_decision`**
    - Logs decision events for audit purposes
    ```json
    {
      "session_id": "SESSION123",
      "customer_id": "CUST001",
      "decision_type": "refund_approved",
      "inputs": {...},
      "policy_checks": [...],
      "outcome": {...}
    }
    ```

11. **`store_artifact`**
    - Stores audit artifacts (transcripts, receipts, etc.)
    ```json
    {
      "session_id": "SESSION123",
      "artifact_type": "transcript",
      "content": "...",
      "metadata": {...}
    }
    ```

### Example API Call

Using curl to call a tool:

```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "verify_by_order_and_name",
    "arguments": {
      "order_id": "ORD-001",
      "name": "Sanjyot Sathe"
    }
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `RESEND_API_KEY` | Yes | Resend API key for sending OTP emails | - |
| `RESEND_FROM_EMAIL` | No | Sender email address | `onboarding@resend.dev` |
| `PORT` | No | HTTP server port | `8000` |
| `HOST` | No | HTTP server host | `0.0.0.0` |

### Policy Configuration

Refund policies are configured in `mcp_config.json`:

```json
{
  "policy": {
    "refund_window_days": 30,
    "restocking_fee_percent": 10,
    "allowed_conditions": ["unopened", "defective", "wrong_item"],
    "excluded_categories": ["digital_goods", "gift_cards"]
  },
  "otp": {
    "expiration_minutes": 10,
    "max_attempts": 3,
    "code_length": 6
  }
}
```

## 📁 Project Structure

```
refund_agent/
├── tools/                  # Core business logic modules
│   ├── identity.py        # Identity verification & OTP
│   ├── orders.py          # Order & transaction management
│   ├── policy.py           # Refund policy engine
│   ├── refunds.py         # Refund execution
│   └── audit.py           # Audit logging
├── storage/               # Persistent storage
│   ├── audio/             # Audio recordings
│   ├── transcripts/       # Conversation transcripts
│   ├── decision_logs/     # Audit decision logs
│   └── receipts/          # Refund receipts
├── mcp_server.py          # stdio MCP server
├── mcp_server_http.py     # HTTP MCP server
├── test_server.py         # Test suite
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` files to version control
2. **OTP Security**: OTPs expire after 10 minutes and have 3 attempt limit
3. **Domain Verification**: Use verified domains for production email sending
4. **CORS**: Restrict CORS origins in production (currently allows all)
5. **Rate Limiting**: Implement rate limiting for production use

## 🧪 Testing

### Test Sample Customer

Use this sample customer for testing:

- **Order ID**: `ORD-001`
- **Name**: `Sanjyot Sathe`
- **Email**: `sanjyot.sathe@gmail.com`
- **Customer ID**: `CUST001`

See `SAMPLE_CUSTOMERS.md` for more test scenarios.

### Manual Testing

1. **Verify identity**:
   ```bash
   curl -X POST http://localhost:8000/tools/call \
     -H "Content-Type: application/json" \
     -d '{"name": "verify_by_order_and_name", "arguments": {"order_id": "ORD-001", "name": "Sanjyot Sathe"}}'
   ```

2. **Send OTP**:
   ```bash
   curl -X POST http://localhost:8000/tools/call \
     -H "Content-Type: application/json" \
     -d '{"name": "send_otp", "arguments": {"customer_id": "CUST001", "method": "email"}}'
   ```

3. **Check email** for OTP code, then verify it.

## 📚 Additional Documentation

- **[RESEND_SETUP.md](RESEND_SETUP.md)** - Detailed Resend API setup guide
- **[ELEVENLABS_SETUP.md](ELEVENLABS_SETUP.md)** - ElevenLabs integration guide
- **[NGROK_SETUP.md](NGROK_SETUP.md)** - ngrok setup for remote access
- **[SAMPLE_CUSTOMERS.md](SAMPLE_CUSTOMERS.md)** - Test customer data
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## 🚧 Production Considerations

Before deploying to production:

- [ ] Replace in-memory storage with a database
- [ ] Set up proper domain verification for Resend
- [ ] Configure CORS to restrict origins
- [ ] Implement rate limiting
- [ ] Set up monitoring and alerting
- [ ] Configure proper logging
- [ ] Use HTTPS for all connections
- [ ] Set up backup and recovery procedures

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Support

For issues and questions, please [open an issue](link-to-issues) or contact [your contact info].
