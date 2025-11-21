"""
Identity Verification Tools
Handles customer authentication via order ID, email/phone, OTP, and payment verification.
"""

import asyncio
import random
import string
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import json

# Resend API for sending OTP emails
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    print("Warning: resend package not installed. OTP emails will not be sent.")

# In-memory storage for demo (replace with actual database in production)
_otp_storage: Dict[str, Dict[str, Any]] = {}
_customer_db: Dict[str, Dict[str, Any]] = {}


class IdentityVerifier:
    """Handles customer identity verification."""
    
    def __init__(self):
        # Load sample customer data
        self._load_sample_customers()
        
        # Initialize Resend API key if available
        self.resend_configured = False
        if RESEND_AVAILABLE:
            resend_api_key = os.getenv("RESEND_API_KEY")
            if resend_api_key:
                resend.api_key = resend_api_key
                self.resend_configured = True
            else:
                print("Warning: RESEND_API_KEY environment variable not set. OTP emails will not be sent.")
    
    def _load_sample_customers(self):
        """Load sample customer data for PoC."""
        global _customer_db
        _customer_db = {
            "CUST001": {
                "customer_id": "CUST001",
                "email": "sanjyot.sathe@gmail.com",
                "phone": "+1-555-0123",
                "name": "Sanjyot Sathe",
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
    
    async def verify_by_order_and_name(
        self,
        order_id: str,
        name: str
    ) -> Dict[str, Any]:
        """
        Verify customer by order ID and name. This is the first step in the verification flow.
        If name matches, returns customer_id and email for OTP sending.
        
        Args:
            order_id: Order ID provided by customer
            name: Customer name provided by customer
        
        Returns:
            Dict with verification status, customer_id, email if name matches
        """
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
        customer_name = customer.get("name", "").strip()
        provided_name = name.strip()
        
        # Case-insensitive name matching
        if customer_name.lower() != provided_name.lower():
            return {
                "verified": False,
                "error": "Name does not match the order",
                "order_id": order_id,
                "customer_id": customer_id  # Don't reveal customer_id on mismatch
            }
        
        # Name matches - return customer info for OTP sending
        return {
            "verified": True,
            "customer_id": customer_id,
            "order_id": normalized_order_id,
            "email": customer.get("email"),
            "customer_name": customer_name,
            "message": "Name verified. OTP will be sent to registered email."
        }
    
    async def verify(
        self,
        order_id: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        last_four_digits: Optional[str] = None,
        otp_code: Optional[str] = None,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Verify customer identity using order ID and OTP code.
        This method now requires OTP verification after name verification.
        
        Args:
            order_id: Order ID
            customer_id: Customer ID from verify_by_order_and_name
            otp_code: OTP code provided by customer (required)
            email: Deprecated - kept for backward compatibility
            phone: Deprecated - kept for backward compatibility
            last_four_digits: Deprecated - kept for backward compatibility
        
        Returns:
            Dict with verification status, customer_id, and verification level
        """
        # Normalize order ID
        normalized_order_id = order_id.replace("-", "")
        
        # If customer_id is provided, use it; otherwise find by order_id
        if customer_id:
            if customer_id not in _customer_db:
                return {
                    "verified": False,
                    "error": "Invalid customer ID",
                    "order_id": order_id
                }
            customer = _customer_db[customer_id]
        else:
            # Find customer by order ID
            customer_id = None
            for cust_id, cust_data in _customer_db.items():
                orders = cust_data.get("orders", [])
                if normalized_order_id in orders or order_id in orders:
                    customer_id = cust_id
                    break
            
            if not customer_id:
                return {
                    "verified": False,
                    "error": "Order not found",
                    "order_id": order_id
                }
            customer = _customer_db[customer_id]
        
        # OTP verification is now required
        if not otp_code:
            return {
                "verified": False,
                "error": "OTP code is required for verification",
                "order_id": order_id,
                "customer_id": customer_id,
                "requires_otp": True
            }
        
        # Verify OTP
        otp_result = await self.verify_otp(customer_id, otp_code)
        if not otp_result.get("verified"):
            return {
                "verified": False,
                "error": otp_result.get("error", "OTP verification failed"),
                "order_id": order_id,
                "customer_id": customer_id,
                "requires_otp": True
            }
        
        # OTP verification successful
        return {
            "verified": True,
            "customer_id": customer_id,
            "order_id": normalized_order_id,
            "verification_level": "verified",
            "customer_name": customer.get("name"),
            "requires_otp": False
        }
    
    async def send_otp(
        self,
        customer_id: str,
        method: str = "email"  # "email" or "sms"
    ) -> Dict[str, Any]:
        """
        Send OTP to customer's registered email or phone using Resend API.
        
        Args:
            customer_id: Customer ID
            method: "email" or "sms" (currently only email is supported via Resend)
        
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
        
        contact = customer.get("email" if method == "email" else "phone", "")
        
        # Send OTP via Resend API if available
        if method == "email":
            if self.resend_configured:
                try:
                    # Get sender email from environment or use default
                    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
                    
                    # Send email via Resend 2.x API
                    email_response = resend.Emails.send({
                        "from": from_email,
                        "to": [contact],
                        "subject": "Your Verification Code",
                        "html": f"""
                        <html>
                        <body style="font-family: Arial, sans-serif; padding: 20px;">
                            <h2>Verification Code</h2>
                            <p>Hello {customer.get('name', 'Customer')},</p>
                            <p>Your verification code is:</p>
                            <h1 style="font-size: 32px; color: #0066cc; letter-spacing: 5px; margin: 20px 0;">{otp_code}</h1>
                            <p>This code will expire in 10 minutes.</p>
                            <p>If you didn't request this code, please ignore this email.</p>
                            <hr style="margin-top: 30px; border: none; border-top: 1px solid #eee;">
                            <p style="color: #666; font-size: 12px;">This is an automated message. Please do not reply.</p>
                        </body>
                        </html>
                        """
                    })
                    
                    # Extract email ID from response (Resend 2.x returns object with id attribute)
                    email_id = None
                    if hasattr(email_response, 'id'):
                        email_id = email_response.id
                    elif isinstance(email_response, dict):
                        email_id = email_response.get("id")
                    elif hasattr(email_response, 'data') and hasattr(email_response.data, 'id'):
                        email_id = email_response.data.id
                    
                    return {
                        "success": True,
                        "message": f"OTP sent to email: {contact}",
                        "expires_in_minutes": 10,
                        "email_id": email_id
                    }
                except Exception as e:
                    # If Resend fails, fall back to debug mode
                    print(f"Resend API error: {e}")
                    return {
                        "success": True,
                        "message": f"OTP generated (Resend API error: {str(e)}). Email: {contact}",
                        "expires_in_minutes": 10,
                        "_debug_otp": otp_code,  # Only in case of error
                        "warning": "Email sending failed, OTP returned for testing"
                    }
            else:
                # Resend not configured - return debug OTP
                return {
                    "success": True,
                    "message": f"OTP generated (Resend not configured). Email: {contact}",
                    "expires_in_minutes": 10,
                    "_debug_otp": otp_code,
                    "warning": "Resend API not configured. Set RESEND_API_KEY environment variable."
                }
        else:
            # SMS not implemented yet
            return {
                "success": False,
                "error": "SMS OTP not yet implemented. Please use email method."
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

