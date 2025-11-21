# Resend API Setup Guide

This guide explains how to set up Resend API for OTP email verification in the RRVA system.

## Overview

The verification flow has been updated to require OTP verification:

1. **Step 1**: Verify customer by order ID and name (`verify_by_order_and_name`)
2. **Step 2**: Send OTP to customer's email (`send_otp`)
3. **Step 3**: Verify OTP code (`verify_otp`)
4. **Step 4**: Final verification (`verify_customer_identity`)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the `resend` package (version 2.0.0 or higher).

### 2. Get Resend API Key

1. Sign up for a free account at [resend.com](https://resend.com)
2. Navigate to **API Keys** in your dashboard
3. Create a new API key
4. Copy the API key (starts with `re_`)

### 3. Configure Environment Variables

Set the following environment variables:

**Windows PowerShell:**
```powershell
$env:RESEND_API_KEY="re_your_api_key_here"
$env:RESEND_FROM_EMAIL="noreply@yourdomain.com"  # Optional, defaults to onboarding@resend.dev
```

**Windows Command Prompt:**
```cmd
set RESEND_API_KEY=re_your_api_key_here
set RESEND_FROM_EMAIL=noreply@yourdomain.com
```

**Linux/Mac:**
```bash
export RESEND_API_KEY="re_your_api_key_here"
export RESEND_FROM_EMAIL="noreply@yourdomain.com"
```

**Using .env file (recommended):**
Create a `.env` file in the project root:
```
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

Then load it before running:
```bash
# Using python-dotenv (install with: pip install python-dotenv)
python -m dotenv run python mcp_server_http.py
```

### 4. Domain Setup (Optional but Recommended)

For production use, you should:

1. Add your domain in Resend dashboard
2. Verify domain ownership (add DNS records)
3. Use a verified domain email for `RESEND_FROM_EMAIL`

For testing, you can use `onboarding@resend.dev` (default), but emails will be limited.

## Verification Flow

### New Flow (Required)

```python
# Step 1: Verify order and name
result1 = await identity_verifier.verify_by_order_and_name(
    order_id="ORD-001",
    name="Sanjyot Sathe"
)

if result1.get("verified"):
    customer_id = result1["customer_id"]
    email = result1["email"]
    
    # Step 2: Send OTP
    result2 = await identity_verifier.send_otp(
        customer_id=customer_id,
        method="email"
    )
    
    # Step 3: Customer provides OTP, verify it
    result3 = await identity_verifier.verify_otp(
        customer_id=customer_id,
        otp_code="123456"  # OTP from email
    )
    
    # Step 4: Final verification
    if result3.get("verified"):
        result4 = await identity_verifier.verify(
            order_id="ORD-001",
            customer_id=customer_id,
            otp_code="123456"
        )
```

### API Endpoints

**Step 1: Verify by Order and Name**
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

**Step 2: Send OTP**
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "send_otp",
    "arguments": {
      "customer_id": "CUST001",
      "method": "email"
    }
  }'
```

**Step 3: Verify OTP**
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "verify_otp",
    "arguments": {
      "customer_id": "CUST001",
      "otp_code": "123456"
    }
  }'
```

**Step 4: Final Verification**
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "verify_customer_identity",
    "arguments": {
      "order_id": "ORD-001",
      "customer_id": "CUST001",
      "otp_code": "123456"
    }
  }'
```

## Troubleshooting

### OTP Not Being Sent

1. **Check API Key**: Ensure `RESEND_API_KEY` is set correctly
2. **Check Email**: Verify the customer email exists in the database
3. **Check Logs**: Look for Resend API errors in console output
4. **Fallback Mode**: If Resend fails, the system will return `_debug_otp` in the response (for testing only)

### Resend API Errors

- **401 Unauthorized**: Invalid API key
- **422 Unprocessable Entity**: Invalid email address or domain not verified
- **429 Too Many Requests**: Rate limit exceeded (free tier: 100 emails/day)

### Testing Without Resend

If Resend is not configured, the system will:
- Still generate OTP codes
- Return `_debug_otp` in the response for testing
- Show a warning message

**Note**: Never use `_debug_otp` in production. Always configure Resend properly.

## Security Notes

1. **Never expose API keys** in code or version control
2. **Use environment variables** for sensitive configuration
3. **Verify domains** in production to avoid spam filters
4. **Rate limiting**: Resend free tier allows 100 emails/day
5. **OTP expiration**: OTPs expire after 10 minutes
6. **Max attempts**: 3 failed attempts invalidate the OTP

## Production Checklist

- [ ] Resend API key configured via environment variable
- [ ] Domain verified in Resend dashboard
- [ ] `RESEND_FROM_EMAIL` set to verified domain email
- [ ] Test email delivery works
- [ ] OTP expiration and retry limits tested
- [ ] Error handling tested for API failures
- [ ] Monitoring set up for email delivery failures

