# Test Scenarios for RRVA MCP Server

## Scenario 1: Eligible Full Refund

### Setup
- Customer: CUST-001 (John Doe)
- Order: ORD-001 (placed 2025-01-15, within 30-day window)
- Items: Wireless Headphones (unopened), USB-C Cable (unopened)
- Total: $149.99

### Flow
1. Customer calls and provides order ID: `ORD-001`
2. Agent verifies identity: `verify_customer_identity(order_id="ORD-001", email="customer1@example.com")`
3. Agent retrieves order: `get_order_history(customer_id="CUST-001", order_id="ORD-001")`
4. Agent checks eligibility: `check_refund_eligibility(order_id="ORD-001", customer_id="CUST-001", reason="Not satisfied")`
5. Agent executes refund: `execute_refund(order_id="ORD-001", customer_id="CUST-001", reason="Not satisfied")`
6. Agent logs decision and stores artifacts

### Expected Result
- ✅ Refund approved
- ✅ Full refund amount: $149.99
- ✅ Receipt generated
- ✅ Decision log created

---

## Scenario 2: Partial Refund (Used Item)

### Setup
- Customer: CUST-001 (John Doe)
- Order: ORD-002 (placed 2025-02-01, within 30-day window)
- Items: Phone Case (used condition)
- Total: $79.99

### Flow
1. Customer calls with order ID: `ORD-002`
2. Identity verification
3. Order retrieval
4. Eligibility check (item is used)
5. Agent offers partial refund with restocking fee

### Expected Result
- ⚠️ Partial refund eligible
- ⚠️ Restocking fee: 10% = $7.99
- ✅ Refund amount: $72.00
- ✅ Store credit or original payment method

---

## Scenario 3: Ineligible (Outside Window)

### Setup
- Customer: CUST-002 (Jane Smith)
- Order: ORD-003 (placed 2025-01-20, but simulate >30 days old)

### Flow
1. Customer calls with order ID: `ORD-003`
2. Identity verification
3. Order retrieval
4. Eligibility check (order >30 days old)

### Expected Result
- ❌ Refund denied (outside window)
- 🔄 Suggested action: exchange_or_store_credit
- 📝 Escalation option offered

---

## Scenario 4: OTP Verification Flow

### Setup
- Customer: CUST-001
- Order: ORD-001
- Basic verification level (no last-4 provided)

### Flow
1. Customer provides order ID and email
2. Basic verification succeeds but recommends OTP
3. Agent sends OTP: `send_otp(customer_id="CUST-001", method="email")`
4. Customer provides OTP code
5. Agent verifies: `verify_otp(customer_id="CUST-001", otp_code="123456")`
6. Enhanced verification achieved
7. Continue with refund flow

### Expected Result
- ✅ OTP sent successfully
- ✅ OTP verified
- ✅ Enhanced verification level
- ✅ Proceed with refund processing

---

## Sample Tool Calls (JSON)

### Verify Identity
```json
{
  "tool": "verify_customer_identity",
  "arguments": {
    "order_id": "ORD-001",
    "email": "customer1@example.com"
  }
}
```

### Check Eligibility
```json
{
  "tool": "check_refund_eligibility",
  "arguments": {
    "order_id": "ORD-001",
    "customer_id": "CUST-001",
    "reason": "Product not as described"
  }
}
```

### Execute Refund
```json
{
  "tool": "execute_refund",
  "arguments": {
    "order_id": "ORD-001",
    "customer_id": "CUST-001",
    "reason": "Product not as described",
    "refund_method": "original_payment"
  }
}
```

### Log Decision
```json
{
  "tool": "log_decision",
  "arguments": {
    "session_id": "SESSION-12345",
    "customer_id": "CUST-001",
    "decision_type": "refund_approved",
    "inputs": {
      "order_id": "ORD-001",
      "reason": "Product not as described"
    },
    "policy_checks": [...],
    "outcome": {
      "refund_id": "REF-ABC123",
      "amount": 149.99,
      "status": "completed"
    }
  }
}
```

