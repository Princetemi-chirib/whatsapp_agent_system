from fastapi import APIRouter, HTTPException, Request, Form, Depends
from typing import Optional
from app.services.job_service import JobService
from app.services.confirmation_service import confirmation_service

router = APIRouter()

# Dependency injection
def get_job_service():
    return JobService()

@router.post("/twilio/whatsapp")
async def twilio_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    job_service: JobService = Depends(get_job_service)
):
    """Handle incoming WhatsApp messages from Twilio webhook."""
    try:
        # Extract phone number (remove whatsapp: prefix)
        agent_phone = From.replace('whatsapp:', '')
        
        # Parse the message body
        message_body = Body.strip().upper()
        
        # Handle different types of responses
        if message_body == 'YES':
            # Agent is accepting an inspection request
            # Find the most recent pending job that hasn't been assigned yet
            pending_jobs = job_service.get_pending_jobs()
            
            # Sort by creation date to get the most recent first
            pending_jobs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            for job in pending_jobs:
                if job['status'] == 'pending' and not job.get('assigned_agent'):
                    # Record the agent's response
                    confirmation_service.record_agent_response(job['id'], agent_phone, 'YES')
                    
                    # Try to assign this job to the agent
                    result = job_service.handle_agent_response(
                        job['id'], 
                        agent_phone, 
                        'YES'
                    )
                    if result['success']:
                        print(f"Job {job['id']} assigned to {agent_phone}")
                        # Mark confirmation as complete
                        confirmation_service.mark_confirmation_complete(job['id'], agent_phone)
                        return {"status": "success", "message": "Job assigned"}
            
            # If no pending jobs found or all are already assigned
            return {"status": "no_jobs", "message": "No available inspection requests"}
            
        elif message_body == 'CONFIRM':
            # Agent is confirming the inspection schedule
            # Find the assigned job for this agent
            agent_jobs = job_service.get_jobs_by_agent(agent_phone)
            
            for job in agent_jobs:
                if job['status'] == 'assigned':
                    # Record the agent's response
                    confirmation_service.record_agent_response(job['id'], agent_phone, 'CONFIRM')
                    
                    result = job_service.approve_inspection_schedule(job['id'])
                    if result['success']:
                        # Mark confirmation as complete
                        confirmation_service.mark_confirmation_complete(job['id'], agent_phone)
                        return {"status": "success", "message": "Schedule confirmed"}
            
            return {"status": "no_assigned_jobs", "message": "No assigned jobs found"}
            
        elif message_body == 'START':
            # Agent is starting the inspection
            agent_jobs = job_service.get_jobs_by_agent(agent_phone)
            
            for job in agent_jobs:
                if job['status'] == 'approved':
                    result = job_service.start_inspection(job['id'])
                    if result['success']:
                        return {"status": "success", "message": "Inspection started"}
            
            return {"status": "no_approved_jobs", "message": "No approved jobs found"}
            
        elif message_body == 'COMPLETE':
            # Agent is marking inspection as completed
            agent_jobs = job_service.get_jobs_by_agent(agent_phone)
            
            for job in agent_jobs:
                if job['status'] == 'in_progress':
                    result = job_service.complete_inspection(job['id'])
                    if result['success']:
                        return {"status": "success", "message": "Inspection completed"}
            
            return {"status": "no_in_progress_jobs", "message": "No in-progress jobs found"}
            
        else:
            # Unknown command
            return {
                "status": "unknown_command",
                "message": "Unknown command. Use YES to accept, CONFIRM to approve, or COMPLETE to finish."
            }
            
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/twilio/status")
async def webhook_status():
    """Check webhook endpoint status."""
    return {"status": "active", "message": "Twilio webhook endpoint is running"}

@router.post("/twilio/status-callback")
async def twilio_status_callback(
    request: Request,
    MessageSid: str = Form(...),
    MessageStatus: str = Form(...),
    To: str = Form(...),
    From: str = Form(...)
):
    """Handle Twilio message status callbacks."""
    try:
        print(f"Message Status Update:")
        print(f"  MessageSid: {MessageSid}")
        print(f"  Status: {MessageStatus}")
        print(f"  To: {To}")
        print(f"  From: {From}")
        
        # You can store message status in database if needed
        # For now, just log it
        
        return {"status": "success", "message": "Status callback received"}
        
    except Exception as e:
        print(f"Error processing status callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
