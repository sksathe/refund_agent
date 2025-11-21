"""
MCP Server for Request Resolution Voice Agent (RRVA)
Integrates with ElevenLabs Conversational AI for customer refund handling.

This server provides tools for:
- Identity verification (OTP, order ID verification)
- Order/Transaction history retrieval
- Refund policy evaluation
- Refund execution
- Audit logging and artifact storage
"""

import asyncio
import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
import mcp.server.stdio

# Import our tool implementations
from tools.identity import IdentityVerifier
from tools.orders import OrderHistoryService
from tools.policy import RefundPolicyEngine
from tools.refunds import RefundExecutor
from tools.audit import AuditLogger

# Initialize services
identity_verifier = IdentityVerifier()
order_service = OrderHistoryService()
policy_engine = RefundPolicyEngine()
refund_executor = RefundExecutor()
audit_logger = AuditLogger()

# Create MCP server instance
app = Server("rrva-mcp-server")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools for the voice agent."""
    return [
        Tool(
            name="verify_by_order_and_name",
            description="Step 1: Verify customer by order ID and name. If name matches, returns customer_id and email for OTP sending. Use this first before sending OTP.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID or order number provided by customer"
                    },
                    "name": {
                        "type": "string",
                        "description": "Customer name to verify against the order"
                    }
                },
                "required": ["order_id", "name"]
            }
        ),
        Tool(
            name="verify_customer_identity",
            description="Step 3: Final verification using order ID, customer ID, and OTP code. Use this after verify_by_order_and_name and verify_otp. Requires OTP verification.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID or order number provided by customer"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Customer ID from verify_by_order_and_name"
                    },
                    "otp_code": {
                        "type": "string",
                        "description": "OTP code provided by customer (required)"
                    },
                    "email": {
                        "type": "string",
                        "description": "Deprecated - kept for backward compatibility"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Deprecated - kept for backward compatibility"
                    },
                    "last_four_digits": {
                        "type": "string",
                        "description": "Deprecated - kept for backward compatibility"
                    }
                },
                "required": ["order_id", "customer_id", "otp_code"]
            }
        ),
        Tool(
            name="send_otp",
            description="Step 2: Send OTP (One-Time Password) to customer's registered email using Resend API. Use this after verify_by_order_and_name succeeds.",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Customer ID from verify_by_order_and_name"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["email", "sms"],
                        "description": "Delivery method for OTP (currently only 'email' is supported via Resend)"
                    }
                },
                "required": ["customer_id"]
            }
        ),
        Tool(
            name="verify_otp",
            description="Verify the OTP code provided by the customer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Customer ID"
                    },
                    "otp_code": {
                        "type": "string",
                        "description": "OTP code provided by customer"
                    }
                },
                "required": ["customer_id", "otp_code"]
            }
        ),
        Tool(
            name="get_order_history",
            description="Retrieve order history for a verified customer. Returns order details, transaction history, and fulfillment status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Verified customer ID"
                    },
                    "order_id": {
                        "type": "string",
                        "description": "Specific order ID to retrieve (optional, returns all if not provided)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of orders to return (default: 10)"
                    }
                },
                "required": ["customer_id"]
            }
        ),
        Tool(
            name="get_transaction_history",
            description="Retrieve transaction/payment history for a specific order.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Verified customer ID"
                    }
                },
                "required": ["order_id", "customer_id"]
            }
        ),
        Tool(
            name="check_refund_eligibility",
            description="Evaluate refund eligibility for an order based on policy rules (time window, condition, channel, etc.). Returns eligibility status, reason, and suggested action.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID to check"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Verified customer ID"
                    },
                    "item_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific item IDs to refund (optional, refunds entire order if not provided)"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Customer-provided reason for refund request"
                    }
                },
                "required": ["order_id", "customer_id"]
            }
        ),
        Tool(
            name="execute_refund",
            description="Execute a refund for an eligible order. Creates refund record, processes payment reversal, and generates receipt.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Verified customer ID"
                    },
                    "item_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific item IDs to refund (optional)"
                    },
                    "refund_amount": {
                        "type": "number",
                        "description": "Refund amount (optional, uses calculated amount if not provided)"
                    },
                    "refund_method": {
                        "type": "string",
                        "enum": ["original_payment", "store_credit"],
                        "description": "Refund method preference"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Refund reason for audit"
                    }
                },
                "required": ["order_id", "customer_id", "reason"]
            }
        ),
        Tool(
            name="log_decision",
            description="Log a decision event for audit purposes. Stores decision log with inputs, policy checks, and outcome.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session/Interaction ID"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Customer ID"
                    },
                    "decision_type": {
                        "type": "string",
                        "enum": ["refund_approved", "refund_denied", "partial_refund", "escalated"],
                        "description": "Type of decision made"
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Input parameters used in decision"
                    },
                    "policy_checks": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Policy evaluation results"
                    },
                    "outcome": {
                        "type": "object",
                        "description": "Final outcome and actions taken"
                    },
                    "tool_calls": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Tool calls made during decision process"
                    }
                },
                "required": ["session_id", "customer_id", "decision_type", "outcome"]
            }
        ),
        Tool(
            name="store_artifact",
            description="Store audit artifacts (audio, transcript, decision log, receipt) to persistent storage.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    },
                    "artifact_type": {
                        "type": "string",
                        "enum": ["audio", "transcript", "decision_log", "receipt"],
                        "description": "Type of artifact"
                    },
                    "content": {
                        "type": "string",
                        "description": "Artifact content (base64 for audio, JSON/text for others)"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Additional metadata (timestamps, customer_id, etc.)"
                    }
                },
                "required": ["session_id", "artifact_type", "content"]
            }
        ),
        Tool(
            name="get_refund_receipt",
            description="Retrieve refund receipt for a completed refund transaction.",
            inputSchema={
                "type": "object",
                "properties": {
                    "refund_id": {
                        "type": "string",
                        "description": "Refund transaction ID"
                    },
                    "order_id": {
                        "type": "string",
                        "description": "Order ID"
                    }
                },
                "required": ["refund_id"]
            }
        ),
        Tool(
            name="end_call",
            description="[SYSTEM TOOL - DO NOT ANNOUNCE] Internal function to finalize call session. Silently logs decision and stores transcript. Call this automatically at the end of every customer interaction without mentioning it to the customer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session/Interaction ID"
                    },
                    "customer_id": {
                        "type": "string",
                        "description": "Customer ID (if verified)"
                    },
                    "decision_type": {
                        "type": "string",
                        "enum": ["refund_approved", "refund_denied", "partial_refund", "escalated", "no_action"],
                        "description": "Type of decision made during the call"
                    },
                    "transcript": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "speaker": {"type": "string", "enum": ["agent", "customer"]},
                                "text": {"type": "string"}
                            },
                            "required": ["speaker", "text"]
                        },
                        "description": "Full conversation transcript with speaker labels"
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Input parameters used in decision (order_id, reason, etc.)"
                    },
                    "policy_checks": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Policy evaluation results (if applicable)"
                    },
                    "outcome": {
                        "type": "object",
                        "description": "Final outcome and actions taken (refund_id, amount, status, etc.)"
                    },
                    "tool_calls": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Tool calls made during the session"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Additional metadata (call_duration_seconds, call_reason, etc.)"
                    }
                },
                "required": ["session_id", "decision_type", "transcript"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from the voice agent."""
    try:
        if name == "verify_by_order_and_name":
            result = await identity_verifier.verify_by_order_and_name(
                order_id=arguments.get("order_id"),
                name=arguments.get("name")
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "verify_customer_identity":
            result = await identity_verifier.verify(
                order_id=arguments.get("order_id"),
                customer_id=arguments.get("customer_id"),
                otp_code=arguments.get("otp_code"),
                email=arguments.get("email"),  # Deprecated but kept for compatibility
                phone=arguments.get("phone"),  # Deprecated but kept for compatibility
                last_four_digits=arguments.get("last_four_digits")  # Deprecated but kept for compatibility
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "send_otp":
            result = await identity_verifier.send_otp(
                customer_id=arguments["customer_id"],
                method=arguments.get("method", "email")  # Default to email
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "verify_otp":
            result = await identity_verifier.verify_otp(
                customer_id=arguments["customer_id"],
                otp_code=arguments["otp_code"]
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_order_history":
            result = await order_service.get_order_history(
                customer_id=arguments["customer_id"],
                order_id=arguments.get("order_id"),
                limit=arguments.get("limit", 10)
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_transaction_history":
            result = await order_service.get_transaction_history(
                order_id=arguments["order_id"],
                customer_id=arguments["customer_id"]
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "check_refund_eligibility":
            result = await policy_engine.check_eligibility(
                order_id=arguments["order_id"],
                customer_id=arguments["customer_id"],
                item_ids=arguments.get("item_ids"),
                reason=arguments.get("reason")
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "execute_refund":
            result = await refund_executor.execute(
                order_id=arguments["order_id"],
                customer_id=arguments["customer_id"],
                item_ids=arguments.get("item_ids"),
                refund_amount=arguments.get("refund_amount"),
                refund_method=arguments.get("refund_method", "original_payment"),
                reason=arguments["reason"]
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "log_decision":
            result = await audit_logger.log_decision(
                session_id=arguments["session_id"],
                customer_id=arguments["customer_id"],
                decision_type=arguments["decision_type"],
                inputs=arguments.get("inputs", {}),
                policy_checks=arguments.get("policy_checks", []),
                outcome=arguments["outcome"],
                tool_calls=arguments.get("tool_calls", [])
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "store_artifact":
            result = await audit_logger.store_artifact(
                session_id=arguments["session_id"],
                artifact_type=arguments["artifact_type"],
                content=arguments["content"],
                metadata=arguments.get("metadata", {})
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_refund_receipt":
            result = await refund_executor.get_receipt(
                refund_id=arguments["refund_id"],
                order_id=arguments.get("order_id")
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "end_call":
            # Automatically log decision and store transcript when call ends
            session_id = arguments["session_id"]
            customer_id = arguments.get("customer_id", "unknown")
            decision_type = arguments["decision_type"]
            transcript = arguments["transcript"]
            
            results = {
                "session_id": session_id,
                "actions_taken": []
            }
            
            # 1. Store transcript
            try:
                transcript_content = json.dumps({
                    "conversation": transcript
                })
                transcript_result = await audit_logger.store_artifact(
                    session_id=session_id,
                    artifact_type="transcript",
                    content=transcript_content,
                    metadata=arguments.get("metadata", {})
                )
                results["actions_taken"].append("transcript_stored")
                results["transcript_path"] = transcript_result.get("file_path")
            except Exception as e:
                results["transcript_error"] = str(e)
            
            # 2. Log decision
            try:
                decision_result = await audit_logger.log_decision(
                    session_id=session_id,
                    customer_id=customer_id,
                    decision_type=decision_type,
                    inputs=arguments.get("inputs", {}),
                    policy_checks=arguments.get("policy_checks", []),
                    outcome=arguments.get("outcome", {}),
                    tool_calls=arguments.get("tool_calls", [])
                )
                results["actions_taken"].append("decision_logged")
                results["log_id"] = decision_result.get("log_id")
                results["log_path"] = decision_result.get("log_path")
            except Exception as e:
                results["decision_log_error"] = str(e)
            
            # 3. Store receipt if refund was processed
            if decision_type == "refund_approved" and arguments.get("outcome", {}).get("refund_id"):
                try:
                    receipt = await refund_executor.get_receipt(
                        refund_id=arguments["outcome"]["refund_id"]
                    )
                    receipt_content = json.dumps(receipt)
                    receipt_result = await audit_logger.store_artifact(
                        session_id=session_id,
                        artifact_type="receipt",
                        content=receipt_content,
                        metadata=arguments.get("metadata", {})
                    )
                    results["actions_taken"].append("receipt_stored")
                    results["receipt_path"] = receipt_result.get("file_path")
                except Exception as e:
                    results["receipt_error"] = str(e)
            
            results["success"] = True
            results["message"] = f"Call finalized. Actions: {', '.join(results['actions_taken'])}"
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "tool": name}, indent=2)
        )]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="rrva-mcp-server",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

