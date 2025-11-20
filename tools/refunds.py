"""
Refund Execution Tools
Handles refund creation, payment reversal, and receipt generation.
"""

from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import uuid
import json

from tools.orders import _sample_orders, _sample_transactions


class RefundExecutor:
    """Handles refund execution and receipt generation."""
    
    def __init__(self):
        # In-memory storage for refunds (replace with database in production)
        self._refunds: Dict[str, Dict[str, Any]] = {}
    
    async def execute(
        self,
        order_id: str,
        customer_id: str,
        reason: str,
        item_ids: Optional[List[str]] = None,
        refund_amount: Optional[float] = None,
        refund_method: str = "original_payment"
    ) -> Dict[str, Any]:
        """
        Execute a refund for an eligible order.
        
        Args:
            order_id: Order ID
            customer_id: Verified customer ID
            reason: Refund reason
            item_ids: Specific item IDs to refund (optional)
            refund_amount: Refund amount (optional, calculated if not provided)
            refund_method: "original_payment" or "store_credit"
        
        Returns:
            Dict with refund details and receipt
        """
        # Normalize IDs (remove hyphens) to handle both formats
        normalized_order_id = order_id.replace("-", "")
        normalized_customer_id = customer_id.replace("-", "")
        
        # Try to find order with normalized ID first, then original
        order = _sample_orders.get(normalized_order_id) or _sample_orders.get(order_id)
        
        if not order:
            return {
                "success": False,
                "error": "Order not found",
                "order_id": order_id
            }
        
        # Verify customer ownership (check normalized or original)
        order_customer_id = order["customer_id"]
        if order_customer_id != normalized_customer_id and order_customer_id != customer_id:
            return {
                "success": False,
                "error": "Unauthorized: Order does not belong to customer",
                "order_id": order_id
            }
        
        # Calculate refund amount if not provided
        if refund_amount is None:
            if item_ids:
                # Normalize item IDs to handle both ITEM-001 and ITEM001 formats
                normalized_item_ids = [item_id.replace("-", "") for item_id in item_ids]
                refund_amount = sum(
                    item["price"] * item["quantity"]
                    for item in order["items"]
                    if item["item_id"] in item_ids or item["item_id"] in normalized_item_ids
                )
            else:
                refund_amount = order["total_amount"]
        
        # Generate refund ID
        refund_id = f"REF{uuid.uuid4().hex[:8].upper()}"
        
        # Create refund record
        refund_record = {
            "refund_id": refund_id,
            "order_id": order_id,
            "customer_id": customer_id,
            "refund_amount": refund_amount,
            "currency": order["currency"],
            "refund_method": refund_method,
            "reason": reason,
            "status": "completed",
            "processed_at": datetime.utcnow().isoformat() + "Z",
            "item_ids": item_ids,
            "original_order": {
                "order_date": order["order_date"],
                "total_amount": order["total_amount"]
            }
        }
        
        # Store refund
        self._refunds[refund_id] = refund_record
        
        # In production, this would:
        # 1. Call payment processor API to reverse charge
        # 2. Update order status in database
        # 3. Send confirmation email
        # 4. Update inventory if applicable
        
        # Generate receipt
        receipt = await self.get_receipt(refund_id, order_id)
        
        return {
            "success": True,
            "refund_id": refund_id,
            "refund_amount": refund_amount,
            "currency": order["currency"],
            "refund_method": refund_method,
            "status": "completed",
            "processed_at": refund_record["processed_at"],
            "receipt": receipt
        }
    
    async def get_receipt(
        self,
        refund_id: str,
        order_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve refund receipt.
        
        Args:
            refund_id: Refund transaction ID
            order_id: Order ID (optional, for validation)
        
        Returns:
            Dict with receipt details
        """
        if refund_id not in self._refunds:
            return {
                "error": "Refund not found",
                "refund_id": refund_id
            }
        
        refund = self._refunds[refund_id]
        
        # Validate order_id if provided (normalize both for comparison)
        if order_id:
            normalized_refund_order_id = refund["order_id"].replace("-", "")
            normalized_order_id = order_id.replace("-", "")
            if normalized_refund_order_id != normalized_order_id and refund["order_id"] != order_id:
                return {
                    "error": "Order ID mismatch",
                    "refund_id": refund_id
                }
        
        # Get order details (handle both formats)
        normalized_refund_order_id = refund["order_id"].replace("-", "")
        order = _sample_orders.get(normalized_refund_order_id) or _sample_orders.get(refund["order_id"], {})
        
        receipt = {
            "refund_id": refund_id,
            "order_id": refund["order_id"],
            "customer_id": refund["customer_id"],
            "refund_amount": refund["refund_amount"],
            "currency": refund["currency"],
            "refund_method": refund["refund_method"],
            "reason": refund["reason"],
            "processed_at": refund["processed_at"],
            "estimated_credit_date": (
                datetime.fromisoformat(refund["processed_at"].replace("Z", "+00:00")) + 
                timedelta(days=5 if refund["refund_method"] == "original_payment" else 0)
            ).isoformat() + "Z",
            "reference_number": f"REF{refund_id}",
            "items_refunded": refund.get("item_ids", []),
            "original_order_total": order.get("total_amount", 0),
            "receipt_generated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        return receipt

