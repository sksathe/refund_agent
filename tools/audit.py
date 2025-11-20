"""
Audit Logging and Artifact Storage
Handles decision logging and storage of audio, transcripts, decision logs, and receipts.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
import os

# Storage directory for artifacts
STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)

# Subdirectories for different artifact types
AUDIO_DIR = STORAGE_DIR / "audio"
TRANSCRIPT_DIR = STORAGE_DIR / "transcripts"
LOG_DIR = STORAGE_DIR / "decision_logs"
RECEIPT_DIR = STORAGE_DIR / "receipts"

for dir_path in [AUDIO_DIR, TRANSCRIPT_DIR, LOG_DIR, RECEIPT_DIR]:
    dir_path.mkdir(exist_ok=True)


class AuditLogger:
    """Handles audit logging and artifact storage."""
    
    async def log_decision(
        self,
        session_id: str,
        customer_id: str,
        decision_type: str,
        outcome: Dict[str, Any],
        inputs: Optional[Dict[str, Any]] = None,
        policy_checks: Optional[List[Dict[str, Any]]] = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Log a decision event for audit purposes.
        
        Args:
            session_id: Session/Interaction ID
            customer_id: Customer ID
            decision_type: Type of decision (refund_approved, refund_denied, etc.)
            outcome: Final outcome and actions taken
            inputs: Input parameters used in decision
            policy_checks: Policy evaluation results
            tool_calls: Tool calls made during decision process
        
        Returns:
            Dict with log record details
        """
        decision_log = {
            "session_id": session_id,
            "customer_id": customer_id,
            "decision_type": decision_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "inputs": inputs or {},
            "policy_checks": policy_checks or [],
            "tool_calls": tool_calls or [],
            "outcome": outcome,
            "log_id": f"LOG{session_id}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        }
        
        # Store decision log
        log_file = LOG_DIR / f"{decision_log['log_id']}.json"
        with open(log_file, "w") as f:
            json.dump(decision_log, f, indent=2)
        
        return {
            "success": True,
            "log_id": decision_log["log_id"],
            "log_path": str(log_file),
            "timestamp": decision_log["timestamp"]
        }
    
    async def store_artifact(
        self,
        session_id: str,
        artifact_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store audit artifacts (audio, transcript, decision log, receipt).
        
        Args:
            session_id: Session ID
            artifact_type: Type of artifact (audio, transcript, decision_log, receipt)
            content: Artifact content (base64 for audio, JSON/text for others)
            metadata: Additional metadata
        
        Returns:
            Dict with storage details
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        if artifact_type == "audio":
            # For audio, content should be base64 encoded
            file_path = AUDIO_DIR / f"{session_id}_{timestamp}.mp3"
            # In production, decode base64 and write binary
            # For PoC, we'll store as text (base64 string)
            with open(file_path, "w") as f:
                f.write(content)
            file_extension = "mp3"
        
        elif artifact_type == "transcript":
            file_path = TRANSCRIPT_DIR / f"{session_id}_{timestamp}.json"
            # Content should be JSON string
            transcript_data = json.loads(content) if isinstance(content, str) else content
            transcript_data["session_id"] = session_id
            transcript_data["metadata"] = metadata or {}
            transcript_data["stored_at"] = datetime.utcnow().isoformat() + "Z"
            with open(file_path, "w") as f:
                json.dump(transcript_data, f, indent=2)
            file_extension = "json"
        
        elif artifact_type == "decision_log":
            file_path = LOG_DIR / f"{session_id}_{timestamp}.json"
            log_data = json.loads(content) if isinstance(content, str) else content
            log_data["session_id"] = session_id
            log_data["metadata"] = metadata or {}
            log_data["stored_at"] = datetime.utcnow().isoformat() + "Z"
            with open(file_path, "w") as f:
                json.dump(log_data, f, indent=2)
            file_extension = "json"
        
        elif artifact_type == "receipt":
            file_path = RECEIPT_DIR / f"{session_id}_{timestamp}.json"
            receipt_data = json.loads(content) if isinstance(content, str) else content
            receipt_data["session_id"] = session_id
            receipt_data["metadata"] = metadata or {}
            receipt_data["stored_at"] = datetime.utcnow().isoformat() + "Z"
            with open(file_path, "w") as f:
                json.dump(receipt_data, f, indent=2)
            file_extension = "json"
        
        else:
            return {
                "success": False,
                "error": f"Unknown artifact type: {artifact_type}"
            }
        
        return {
            "success": True,
            "artifact_type": artifact_type,
            "session_id": session_id,
            "file_path": str(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "stored_at": datetime.utcnow().isoformat() + "Z"
        }


