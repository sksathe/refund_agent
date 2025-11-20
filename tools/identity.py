"""
Identity Verification Tools
Handles customer authentication via order ID, email/phone, OTP, and payment verification.
"""

import asyncio
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import json

# In-memory storage for demo (replace with actual database in production)
_otp_storage: Dict[str, Dict[str, Any]] = {}
_customer_db: Dict[str, Dict[str, Any]] = {}


class IdentityVerifier:
    """Handles customer identity verification."""
    
    def __init__(self):
        # Load sample customer data
        self._load_sample_customers()
    
    def _load_sample_customers(self):
        """Load sample customer data for PoC."""
        global _customer_db
        _customer_db = {
            "CUST001": {
                "customer_id": "CUST001",
                "email": "michael.chen@email.com",
                "phone": "+1-555-0123",
                "name": "Michael Chen",
                "orders": ["ORD001", "ORD002", "ORD004"],
                "last_four": "4532"
            },
            "CUST002": {
                "customer_id": "CUST002",
                "email": "sarah.johnson@gmail.com",
                "phone": "+1-555-0456",
                "name": "Sarah Johnson",
                "orders": ["ORD003", "ORD005"],
                "last_four": "7891"
            },
            "CUST003": {
                "customer_id": "CUST003",
                "email": "david.rodriguez@outlook.com",
                "phone": "+1-555-0789",
                "name": "David Rodriguez",
                "orders": ["ORD006", "ORD007"],
                "last_four": "2345"
            },
            "CUST004": {
                "customer_id": "CUST004",
                "email": "emily.williams@yahoo.com",
                "phone": "+1-555-0321",
                "name": "Emily Williams",
                "orders": ["ORD008"],
                "last_four": "6789"
            },
            "CUST005": {
                "customer_id": "CUST005",
                "email": "james.brown@email.com",
                "phone": "+1-555-0654",
                "name": "James Brown",
                "orders": ["ORD009", "ORD010", "ORD011"],
                "last_four": "1234"
            },
            "CUST006": {
                "customer_id": "CUST006",
                "email": "jessica.martinez@hotmail.com",
                "phone": "+1-555-0987",
                "name": "Jessica Martinez",
                "orders": ["ORD012"],
                "last_four": "5678"
            },
            "CUST007": {
                "customer_id": "CUST007",
                "email": "robert.taylor@gmail.com",
                "phone": "+1-555-0147",
                "name": "Robert Taylor",
                "orders": ["ORD013", "ORD014"],
                "last_four": "9012"
            },
            "CUST008": {
                "customer_id": "CUST008",
                "email": "amanda.anderson@email.com",
                "phone": "+1-555-0258",
                "name": "Amanda Anderson",
                "orders": ["ORD015"],
                "last_four": "3456"
            },
            "CUST009": {
                "customer_id": "CUST009",
                "email": "ryan.thompson@gmail.com",
                "phone": "+1-555-0369",
                "name": "Ryan Thompson",
                "orders": ["ORD016", "ORD017"],
                "last_four": "4567"
            },
            "CUST010": {
                "customer_id": "CUST010",
                "email": "lisa.garcia@yahoo.com",
                "phone": "+1-555-0741",
                "name": "Lisa Garcia",
                "orders": ["ORD018"],
                "last_four": "8901"
            },
            "CUST011": {
                "customer_id": "CUST011",
                "email": "christopher.lee@email.com",
                "phone": "+1-555-0852",
                "name": "Christopher Lee",
                "orders": ["ORD019", "ORD020"],
                "last_four": "2345"
            },
            "CUST012": {
                "customer_id": "CUST012",
                "email": "nicole.white@outlook.com",
                "phone": "+1-555-0963",
                "name": "Nicole White",
                "orders": ["ORD021"],
                "last_four": "6789"
            },
            "CUST013": {
                "customer_id": "CUST013",
                "email": "kevin.harris@hotmail.com",
                "phone": "+1-555-0147",
                "name": "Kevin Harris",
                "orders": ["ORD022"],
                "last_four": "0123"
            },
            "CUST014": {
                "customer_id": "CUST014",
                "email": "rachel.clark@gmail.com",
                "phone": "+1-555-0258",
                "name": "Rachel Clark",
                "orders": ["ORD023", "ORD024"],
                "last_four": "7890"
            }
        }
    
    async def verify(
        self,
        order_id: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        last_four_digits: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Verify customer identity using order ID and contact information.
        
        Returns:
            Dict with verification status, customer_id, and verification level
        """
        # In production, this would query a real database
        # For PoC, we'll match against sample data
        
        # Normalize order ID - remove hyphens to handle both ORD-001 and ORD001
        normalized_order_id = order_id.replace("-", "")
        
        # Find customer by order ID (check both original and normalized)
        customer_id = None
        matched_order_id = None
        for cust_id, cust_data in _customer_db.items():
            orders = cust_data.get("orders", [])
            # Check if order_id matches (with or without hyphens)
            if normalized_order_id in orders:
                customer_id = cust_id
                matched_order_id = normalized_order_id
                break
            elif order_id in orders:
                customer_id = cust_id
                matched_order_id = order_id
                break
        
        if not customer_id:
            return {
                "verified": False,
                "error": "Order not found",
                "order_id": order_id
            }
        
        customer = _customer_db[customer_id]
        
        # Email is required for verification
        if not email:
            return {
                "verified": False,
                "error": "Email address is required for verification",
                "order_id": order_id
            }
        
        # Verify email matches
        if email.lower() != customer.get("email", "").lower():
            return {
                "verified": False,
                "error": "Email address does not match the order",
                "order_id": order_id
            }
        
        # Email verification successful - no OTP required
        # Return normalized order_id for consistency
        return {
            "verified": True,
            "customer_id": customer_id,
            "order_id": normalized_order_id,  # Return normalized format (no hyphens)
            "verification_level": "verified",
            "customer_name": customer.get("name"),
            "requires_otp": False  # OTP not required - email verification is sufficient
        }
    
    async def send_otp(
        self,
        customer_id: str,
        method: str  # "email" or "sms"
    ) -> Dict[str, Any]:
        """
        Send OTP to customer's registered email or phone.
        
        Returns:
            Dict with OTP status and expiration time
        """
        if customer_id not in _customer_db:
            return {
                "success": False,
                "error": "Customer not found"
            }
        
        customer = _customer_db[customer_id]
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = datetime.now() + timedelta(minutes=10)
        
        # Store OTP
        _otp_storage[customer_id] = {
            "code": otp_code,
            "expires_at": expires_at.isoformat(),
            "method": method,
            "attempts": 0
        }
        
        # In production, send via email/SMS service
        # For PoC, we'll just return it (in production, never return OTP in response)
        contact = customer.get("email" if method == "email" else "phone", "")
        
        return {
            "success": True,
            "message": f"OTP sent to {method}: {contact}",
            "expires_in_minutes": 10,
            # Remove this in production - OTP should never be returned
            "_debug_otp": otp_code if method == "email" else None
        }
    
    async def verify_otp(
        self,
        customer_id: str,
        otp_code: str
    ) -> Dict[str, Any]:
        """
        Verify OTP code provided by customer.
        
        Returns:
            Dict with verification status
        """
        if customer_id not in _otp_storage:
            return {
                "verified": False,
                "error": "No OTP found. Please request a new OTP."
            }
        
        otp_data = _otp_storage[customer_id]
        expires_at = datetime.fromisoformat(otp_data["expires_at"])
        
        # Check expiration
        if datetime.now() > expires_at:
            del _otp_storage[customer_id]
            return {
                "verified": False,
                "error": "OTP expired. Please request a new OTP."
            }
        
        # Check attempts
        if otp_data["attempts"] >= 3:
            del _otp_storage[customer_id]
            return {
                "verified": False,
                "error": "Too many failed attempts. Please request a new OTP."
            }
        
        # Verify code
        if otp_code != otp_data["code"]:
            otp_data["attempts"] += 1
            return {
                "verified": False,
                "error": "Invalid OTP code",
                "attempts_remaining": 3 - otp_data["attempts"]
            }
        
        # Success - remove OTP
        del _otp_storage[customer_id]
        
        return {
            "verified": True,
            "verification_level": "enhanced",
            "customer_id": customer_id
        }

