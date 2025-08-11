import os
from typing import Dict, Optional
from datetime import datetime, timezone
from app.services.database import db_service

class ConfirmationService:
    """Service for managing agent confirmations and flow control."""
    
    def __init__(self):
        self.db = db_service
    
    def record_agent_response(self, job_id: str, agent_phone: str, response: str) -> Dict:
        """Record an agent's response to a job."""
        try:
            confirmation_data = {
                "job_id": job_id,
                "agent_phone": agent_phone,
                "response": response.upper(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "pending_confirmation"
            }
            
            # Check if this agent has already responded to this job
            existing = self.db.find_documents('confirmations', {
                "job_id": job_id,
                "agent_phone": agent_phone
            })
            
            if existing:
                # Update existing confirmation
                self.db.update_document('confirmations', existing[0]['_id'], confirmation_data)
            else:
                # Create new confirmation
                self.db.insert_document('confirmations', confirmation_data)
            
            return {"success": True, "message": "Response recorded"}
            
        except Exception as e:
            print(f"Error recording agent response: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_pending_confirmations(self, job_id: str) -> list:
        """Get all pending confirmations for a job."""
        try:
            confirmations = self.db.find_documents('confirmations', {
                "job_id": job_id,
                "status": "pending_confirmation"
            })
            return confirmations
        except Exception as e:
            print(f"Error getting pending confirmations: {str(e)}")
            return []
    
    def mark_confirmation_complete(self, job_id: str, agent_phone: str) -> bool:
        """Mark a confirmation as complete."""
        try:
            update_data = {
                "status": "confirmed",
                "confirmed_at": datetime.now(timezone.utc).isoformat()
            }
            
            confirmations = self.db.find_documents('confirmations', {
                "job_id": job_id,
                "agent_phone": agent_phone
            })
            
            if confirmations:
                return self.db.update_document('confirmations', confirmations[0]['_id'], update_data)
            return False
            
        except Exception as e:
            print(f"Error marking confirmation complete: {str(e)}")
            return False
    
    def can_send_next_prompt(self, job_id: str, prompt_type: str) -> bool:
        """Check if we can send the next prompt based on previous confirmations."""
        try:
            job = self.db.find_document_by_id('jobs', job_id)
            if not job:
                return False
            
            job_status = job.get('status', 'pending')
            
            # Define the flow requirements
            flow_requirements = {
                'reminder': job_status in ['assigned', 'approved'],
                'start_prompt': job_status == 'approved',
                'completion_prompt': job_status == 'in_progress'
            }
            
            return flow_requirements.get(prompt_type, False)
            
        except Exception as e:
            print(f"Error checking prompt requirements: {str(e)}")
            return False
    
    def get_next_required_action(self, job_id: str) -> Optional[str]:
        """Get the next required action for a job."""
        try:
            job = self.db.find_document_by_id('jobs', job_id)
            if not job:
                return None
            
            job_status = job.get('status', 'pending')
            
            # Define the flow
            if job_status == 'pending':
                return 'wait_for_yes'
            elif job_status == 'assigned':
                return 'wait_for_confirm'
            elif job_status == 'approved':
                return 'wait_for_inspection_time'
            elif job_status == 'in_progress':
                return 'wait_for_complete'
            elif job_status == 'completed':
                return 'completed'
            
            return None
            
        except Exception as e:
            print(f"Error getting next action: {str(e)}")
            return None

# Global confirmation service instance
confirmation_service = ConfirmationService()
