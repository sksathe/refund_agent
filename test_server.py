"""
Simple test script for RRVA MCP Server tools.
Tests individual tool functionality without full MCP protocol.
"""

import asyncio
import json
from tools.identity import IdentityVerifier
from tools.orders import OrderHistoryService
from tools.policy import RefundPolicyEngine
from tools.refunds import RefundExecutor
from tools.audit import AuditLogger


async def test_identity_verification():
    """Test identity verification flow."""
    print("\n=== Testing Identity Verification ===")
    verifier = IdentityVerifier()
    
    # Test 1: Basic verification
    result = await verifier.verify(
        order_id="ORD001",
        email="michael.chen@email.com"
    )
    print(f"Basic verification: {json.dumps(result, indent=2)}")
    
    if result.get("verified"):
        customer_id = result["customer_id"]
        
        # Test 2: Send OTP
        otp_result = await verifier.send_otp(
            customer_id=customer_id,
            method="email"
        )
        print(f"\nOTP sent: {json.dumps(otp_result, indent=2)}")
        
        # Test 3: Verify OTP (using debug OTP from response)
        if "_debug_otp" in otp_result:
            otp_code = otp_result["_debug_otp"]
            verify_result = await verifier.verify_otp(
                customer_id=customer_id,
                otp_code=otp_code
            )
            print(f"\nOTP verification: {json.dumps(verify_result, indent=2)}")


async def test_order_history():
    """Test order history retrieval."""
    print("\n=== Testing Order History ===")
    service = OrderHistoryService()
    
    result = await service.get_order_history(
        customer_id="CUST001",
        limit=5
    )
    print(f"Order history: {json.dumps(result, indent=2)}")
    
    # Test transaction history
    tx_result = await service.get_transaction_history(
        order_id="ORD001",
        customer_id="CUST001"
    )
    print(f"\nTransaction history: {json.dumps(tx_result, indent=2)}")


async def test_refund_eligibility():
    """Test refund eligibility checking."""
    print("\n=== Testing Refund Eligibility ===")
    engine = RefundPolicyEngine()
    
    result = await engine.check_eligibility(
        order_id="ORD001",
        customer_id="CUST001",
        reason="Not satisfied with product"
    )
    print(f"Eligibility check: {json.dumps(result, indent=2)}")


async def test_refund_execution():
    """Test refund execution."""
    print("\n=== Testing Refund Execution ===")
    executor = RefundExecutor()
    
    result = await executor.execute(
        order_id="ORD001",
        customer_id="CUST001",
        reason="Customer requested refund",
        refund_method="original_payment"
    )
    print(f"Refund execution: {json.dumps(result, indent=2)}")
    
    # Get receipt
    if result.get("success"):
        receipt = await executor.get_receipt(
            refund_id=result["refund_id"]
        )
        print(f"\nReceipt: {json.dumps(receipt, indent=2)}")


async def test_audit_logging():
    """Test audit logging."""
    print("\n=== Testing Audit Logging ===")
    logger = AuditLogger()
    
    # Log decision
    log_result = await logger.log_decision(
        session_id="TESTSESSION001",
        customer_id="CUST001",
        decision_type="refund_approved",
        inputs={"order_id": "ORD001", "reason": "Test"},
        policy_checks=[{"check": "time_window", "passed": True}],
        outcome={"refund_id": "REFTEST123", "amount": 149.99}
    )
    print(f"Decision log: {json.dumps(log_result, indent=2)}")
    
    # Store artifact
    artifact_result = await logger.store_artifact(
        session_id="TESTSESSION001",
        artifact_type="transcript",
        content=json.dumps({
            "conversation": [
                {"speaker": "agent", "text": "Hello, how can I help?"},
                {"speaker": "customer", "text": "I'd like a refund"}
            ]
        }),
        metadata={"duration_seconds": 120}
    )
    print(f"\nArtifact stored: {json.dumps(artifact_result, indent=2)}")


async def main():
    """Run all tests."""
    print("RRVA MCP Server - Tool Testing")
    print("=" * 50)
    
    try:
        await test_identity_verification()
        await test_order_history()
        await test_refund_eligibility()
        await test_refund_execution()
        await test_audit_logging()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

