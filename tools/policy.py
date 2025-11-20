"""
Refund Policy Engine
Evaluates refund eligibility based on policy rules (time window, condition, channel, etc.).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

from tools.orders import _sample_orders


class RefundPolicyEngine:
    """Evaluates refund eligibility based on business rules."""
    
    def __init__(self):
        # Policy configuration
        self.policy = {
            "refund_window_days": 30,
            "allowed_conditions": ["unopened", "defective", "wrong_item"],
            "restocking_fee_percent": 10,  # For opened items
            "excluded_categories": ["digital_goods", "gift_cards"],
            "min_refund_amount": 0.01,
            "policy_version": "1.0",
            "effective_date": "2025-01-01"
        }
    
    async def check_eligibility(
        self,
        order_id: str,
        customer_id: str,
        item_ids: Optional[List[str]] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check refund eligibility for an order or specific items.
        
        Args:
            order_id: Order ID - accepts both ORD-001 and ORD001 formats
            customer_id: Verified customer ID - accepts both CUST-001 and CUST001 formats
            item_ids: Specific item IDs to refund (optional)
            reason: Customer-provided reason
        
        Returns:
            Dict with eligibility status, checks performed, and suggested action
        """
        # Normalize IDs (remove hyphens) to handle both formats
        normalized_order_id = order_id.replace("-", "")
        normalized_customer_id = customer_id.replace("-", "")
        
        # Try to find order with normalized ID first, then original
        order = _sample_orders.get(normalized_order_id) or _sample_orders.get(order_id)
        
        if not order:
            return {
                "eligible": False,
                "error": "Order not found",
                "order_id": order_id
            }
        
        # Verify customer ownership (check normalized or original)
        order_customer_id = order["customer_id"]
        if order_customer_id != normalized_customer_id and order_customer_id != customer_id:
            return {
                "eligible": False,
                "error": "Unauthorized: Order does not belong to customer",
                "order_id": order_id
            }
        
        # Perform policy checks
        checks = []
        eligible = True
        issues = []
        
        # Check 1: Time window
        order_date = datetime.fromisoformat(order["order_date"].replace("Z", "+00:00"))
        days_since_order = (datetime.now(order_date.tzinfo) - order_date).days
        within_window = days_since_order <= self.policy["refund_window_days"]
        
        checks.append({
            "check": "time_window",
            "passed": within_window,
            "details": {
                "order_date": order["order_date"],
                "days_since_order": days_since_order,
                "window_days": self.policy["refund_window_days"]
            }
        })
        
        if not within_window:
            eligible = False
            issues.append(f"Order is {days_since_order} days old, exceeds {self.policy['refund_window_days']}-day window")
        
        # Check 2: Order status
        order_delivered = order["status"] == "delivered"
        checks.append({
            "check": "order_status",
            "passed": order_delivered,
            "details": {
                "status": order["status"]
            }
        })
        
        if not order_delivered:
            eligible = False
            issues.append(f"Order status is {order['status']}, must be delivered")
        
        # Check 3: Item-level checks
        items_to_check = order["items"]
        if item_ids:
            # Normalize item IDs to handle both ITEM-001 and ITEM001 formats
            normalized_item_ids = [item_id.replace("-", "") for item_id in item_ids]
            items_to_check = [
                item for item in items_to_check
                if item["item_id"] in item_ids or item["item_id"] in normalized_item_ids
            ]
        
        item_checks = []
        total_refund_amount = 0.0
        partial_eligible = False
        
        for item in items_to_check:
            item_eligible = True
            item_issues = []
            
            # Condition check
            condition = item.get("condition", "unknown")
            condition_allowed = condition in self.policy["allowed_conditions"] or condition == "unopened"
            
            if not condition_allowed and condition == "used":
                # Used items may be eligible with restocking fee
                partial_eligible = True
                restocking_fee = item["price"] * (self.policy["restocking_fee_percent"] / 100)
                refund_amount = item["price"] - restocking_fee
                item_issues.append(f"Item is used, {self.policy['restocking_fee_percent']}% restocking fee applies")
            elif condition_allowed:
                refund_amount = item["price"] * item["quantity"]
            else:
                item_eligible = False
                item_issues.append(f"Item condition '{condition}' not eligible for refund")
            
            item_checks.append({
                "item_id": item["item_id"],
                "product_name": item["product_name"],
                "condition": condition,
                "eligible": item_eligible or partial_eligible,
                "refund_amount": refund_amount if (item_eligible or partial_eligible) else 0,
                "issues": item_issues
            })
            
            if item_eligible or partial_eligible:
                total_refund_amount += refund_amount
        
        checks.append({
            "check": "item_eligibility",
            "passed": any(check["eligible"] for check in item_checks),
            "details": {
                "item_checks": item_checks
            }
        })
        
        # Determine final eligibility
        if not eligible:
            final_eligible = False
        elif any(check["eligible"] for check in item_checks):
            final_eligible = True
        else:
            final_eligible = False
            issues.append("No eligible items found")
        
        # Determine suggested action
        if final_eligible:
            if partial_eligible and not all(check["eligible"] for check in item_checks):
                suggested_action = "partial_refund"
            else:
                suggested_action = "full_refund"
        else:
            if days_since_order > self.policy["refund_window_days"]:
                suggested_action = "exchange_or_store_credit"
            else:
                suggested_action = "escalate"
        
        return {
            "eligible": final_eligible,
            "order_id": order_id,
            "customer_id": customer_id,
            "policy_version": self.policy["policy_version"],
            "checks": checks,
            "total_refund_amount": total_refund_amount,
            "currency": order["currency"],
            "suggested_action": suggested_action,
            "issues": issues,
            "item_details": item_checks,
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }


