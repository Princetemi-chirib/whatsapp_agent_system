import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.services.database import db_service
from app.services.whatsapp_service import WhatsAppService
from app.services.scheduler import scheduler_service

class JobService:
    """Service class for managing real estate inspection jobs with WhatsApp integration."""
    
    def __init__(self):
        self.whatsapp_service = WhatsAppService()
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all inspection jobs from database."""
        try:
            jobs = db_service.find_documents('jobs')
            # Convert ObjectId to string for JSON serialization
            for job in jobs:
                if '_id' in job:
                    job['id'] = str(job['_id'])
                    del job['_id']
                # Ensure job_id is present for API response
                if 'job_id' in job and 'id' not in job:
                    job['id'] = job['job_id']
            return jobs
        except Exception as e:
            print(f"Error getting all jobs: {str(e)}")
            return []
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Get a job by its ID from database."""
        try:
            job = db_service.find_document_by_id('jobs', job_id)
            if job and '_id' in job:
                job['id'] = str(job['_id'])
                del job['_id']
            # Ensure job_id is present for API response
            if job and 'job_id' in job and 'id' not in job:
                job['id'] = job['job_id']
            return job
        except Exception as e:
            print(f"Error getting job by ID: {str(e)}")
            return None
    
    def create_inspection_request(self, data: Dict) -> Dict:
        """Create a new inspection request and notify all agents."""
        try:
            job_id = str(uuid.uuid4())
            job = {
                'job_id': job_id,  # Changed from 'id' to 'job_id' to match database schema
                'property_id': data.get('property_id'),
                'client_id': data.get('client_id'),
                'inspection_date': data.get('inspection_date'),
                'inspection_time': data.get('inspection_time'),
                'status': 'pending',
                'assigned_agent': None,
                'notes': data.get('notes'),
                'property_details': data.get('property_details'),
                'client_details': data.get('client_details'),
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            
            # Save to database
            db_id = db_service.insert_document('jobs', job)
            if db_id:
                job['_id'] = db_id
            
            # Get all active agents
            agents = self.get_active_agents()
            agent_numbers = [agent.get('phone') for agent in agents if agent.get('phone')]
            
            # Send inspection request to all agents
            if agent_numbers:
                self.whatsapp_service.send_inspection_request_to_agents(
                    job['property_details'],
                    job['inspection_date'],
                    job['inspection_time'],
                    agent_numbers
                )
            
            # Ensure the response has the correct id field for API
            response_job = job.copy()
            response_job['id'] = job['job_id']
            return response_job
        except Exception as e:
            print(f"Error creating inspection request: {str(e)}")
            raise
    
    def handle_agent_response(self, job_id: str, agent_phone: str, response: str) -> Dict:
        """Handle agent response to inspection request."""
        try:
            job = self.get_job_by_id(job_id)
            if not job:
                return {"success": False, "error": "Inspection job not found"}
            
            if job['status'] != 'pending':
                # Job already assigned, notify agent
                self.whatsapp_service.send_job_already_assigned(
                    agent_phone, 
                    job['property_details']
                )
                return {"success": False, "error": "Job already assigned"}
            
            if response.upper() == 'YES':
                # Assign job to this agent
                update_data = {
                    'status': 'assigned',
                    'assigned_agent': agent_phone,
                    'assigned_at': datetime.now(timezone.utc).isoformat()
                }
                
                success = db_service.update_document('jobs', job_id, update_data)
                if success:
                    # Get agent details for client notification
                    agent_details = self.get_agent_details(agent_phone)
                    
                    # Send confirmation to assigned agent
                    self.whatsapp_service.send_job_assigned_confirmation(
                        agent_phone,
                        job['property_details'],
                        job['client_details'],
                        job['inspection_date'],
                        job['inspection_time']
                    )
                    
                    # Send notification to client about assigned agent
                    if job['client_details'].get('phone'):
                        self.whatsapp_service.send_agent_assigned_to_client(
                            job['client_details']['phone'],
                            agent_details,
                            job['property_details'],
                            job['inspection_date'],
                            job['inspection_time']
                        )
                    
                    # Notify other agents that the job is taken
                    self.notify_other_agents_job_taken(job, agent_phone)
                    
                    # Schedule inspection reminder
                    self.schedule_inspection_reminder(job)
                    
                    return {
                        "success": True,
                        "message": "Job assigned successfully",
                        "assigned_agent": agent_phone
                    }
                else:
                    return {"success": False, "error": "Failed to assign job"}
            else:
                return {"success": False, "error": "Invalid response"}
                
        except Exception as e:
            print(f"Error handling agent response: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def approve_inspection_schedule(self, job_id: str) -> Dict:
        """Approve inspection schedule by assigned agent."""
        try:
            job = self.get_job_by_id(job_id)
            if not job:
                return {"success": False, "error": "Inspection job not found"}
            
            if job['status'] != 'assigned':
                return {"success": False, "error": "Job not in assigned status"}
            
            update_data = {
                'status': 'approved',
                'approved_at': datetime.now(timezone.utc).isoformat()
            }
            
            success = db_service.update_document('jobs', job_id, update_data)
            if success:
                # Get agent details for client notification
                agent_details = self.get_agent_details(job['assigned_agent'])
                
                # Send schedule confirmation to agent
                self.whatsapp_service.send_schedule_confirmation(
                    job['assigned_agent'],
                    job['property_details'],
                    job['inspection_date'],
                    job['inspection_time']
                )
                
                # Send notification to client about schedule confirmation
                if job['client_details'].get('phone'):
                    self.whatsapp_service.send_schedule_confirmed_to_client(
                        job['client_details']['phone'],
                        agent_details,
                        job['property_details'],
                        job['inspection_date'],
                        job['inspection_time']
                    )
                
                return {
                    "success": True,
                    "message": "Inspection schedule approved"
                }
            else:
                return {"success": False, "error": "Failed to approve schedule"}
                
        except Exception as e:
            print(f"Error approving inspection schedule: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def start_inspection(self, job_id: str) -> Dict:
        """Start an inspection."""
        try:
            job = self.get_job_by_id(job_id)
            if not job:
                return {"success": False, "error": "Inspection job not found"}
            
            update_data = {
                'status': 'in_progress',
                'started_at': datetime.now(timezone.utc).isoformat()
            }
            
            success = db_service.update_document('jobs', job_id, update_data)
            if success:
                # Get agent details for client notification
                agent_details = self.get_agent_details(job['assigned_agent'])
                
                # Send start confirmation to agent
                self.whatsapp_service.send_inspection_started_confirmation(
                    job['assigned_agent'],
                    job['property_details']
                )
                
                # Send notification to client that inspection has started
                if job['client_details'].get('phone'):
                    self.whatsapp_service.send_inspection_started_to_client(
                        job['client_details']['phone'],
                        agent_details,
                        job['property_details']
                    )
                
                return {
                    "success": True,
                    "message": "Inspection started successfully"
                }
            else:
                return {"success": False, "error": "Failed to start inspection"}
                
        except Exception as e:
            print(f"Error starting inspection: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def complete_inspection(self, job_id: str) -> Dict:
        """Mark inspection as completed."""
        try:
            job = self.get_job_by_id(job_id)
            if not job:
                return {"success": False, "error": "Inspection job not found"}
            
            update_data = {
                'status': 'completed',
                'completed_at': datetime.now(timezone.utc).isoformat()
            }
            
            success = db_service.update_document('jobs', job_id, update_data)
            if success:
                # Get agent details for client notification
                agent_details = self.get_agent_details(job['assigned_agent'])
                
                # Send completion confirmation to agent
                self.whatsapp_service.send_inspection_completed_confirmation(
                    job['assigned_agent'],
                    job['property_details']
                )
                
                # Send notification to client that inspection is completed
                if job['client_details'].get('phone'):
                    self.whatsapp_service.send_inspection_completed_to_client(
                        job['client_details']['phone'],
                        agent_details,
                        job['property_details']
                    )
                
                return {
                    "success": True,
                    "message": "Inspection marked as completed"
                }
            else:
                return {"success": False, "error": "Failed to complete inspection"}
                
        except Exception as e:
            print(f"Error completing inspection: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def update_job(self, job_id: str, data: Dict) -> Optional[Dict]:
        """Update an existing job and send status update."""
        try:
            # Get existing job
            existing_job = self.get_job_by_id(job_id)
            if not existing_job:
                return None
            
            # Update fields
            for key, value in data.items():
                if key in existing_job:
                    existing_job[key] = value
            
            existing_job['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            # Update in database
            success = db_service.update_document('jobs', job_id, existing_job)
            if success:
                return existing_job
            return None
        except Exception as e:
            print(f"Error updating job: {str(e)}")
            return None
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job from database."""
        try:
            success = db_service.delete_document('jobs', job_id)
            if success:
                # Cancel any scheduled jobs for this job
                scheduler_service.cancel_job(f"inspection_reminder_{job_id}")
            return success
        except Exception as e:
            print(f"Error deleting job: {str(e)}")
            return False
    
    def get_jobs_by_agent(self, agent_phone: str) -> List[Dict]:
        """Get all jobs assigned to a specific agent."""
        try:
            jobs = db_service.find_documents('jobs', {'assigned_agent': agent_phone})
            for job in jobs:
                if '_id' in job:
                    job['id'] = str(job['_id'])
                    del job['_id']
                # Ensure job_id is present for API response
                if 'job_id' in job and 'id' not in job:
                    job['id'] = job['job_id']
            return jobs
        except Exception as e:
            print(f"Error getting jobs by agent: {str(e)}")
            return []
    
    def get_jobs_by_client(self, client_id: str) -> List[Dict]:
        """Get all jobs for a specific client."""
        try:
            jobs = db_service.find_documents('jobs', {'client_id': client_id})
            for job in jobs:
                if '_id' in job:
                    job['id'] = str(job['_id'])
                    del job['_id']
                # Ensure job_id is present for API response
                if 'job_id' in job and 'id' not in job:
                    job['id'] = job['job_id']
            return jobs
        except Exception as e:
            print(f"Error getting jobs by client: {str(e)}")
            return []
    
    def get_jobs_by_property(self, property_id: str) -> List[Dict]:
        """Get all jobs for a specific property."""
        try:
            jobs = db_service.find_documents('jobs', {'property_id': property_id})
            for job in jobs:
                if '_id' in job:
                    job['id'] = str(job['_id'])
                    del job['_id']
                # Ensure job_id is present for API response
                if 'job_id' in job and 'id' not in job:
                    job['id'] = job['job_id']
            return jobs
        except Exception as e:
            print(f"Error getting jobs by property: {str(e)}")
            return []
    
    def get_active_agents(self) -> List[Dict]:
        """Get all active agents from database."""
        try:
            agents = db_service.find_documents('agents', {'status': 'active'})
            return agents
        except Exception as e:
            print(f"Error getting active agents: {str(e)}")
            return []
    
    def get_pending_jobs(self) -> List[Dict]:
        """Get all pending inspection jobs."""
        try:
            jobs = db_service.find_documents('jobs', {'status': 'pending'})
            for job in jobs:
                if '_id' in job:
                    job['id'] = str(job['_id'])
                    del job['_id']
                # Ensure job_id is present for API response
                if 'job_id' in job and 'id' not in job:
                    job['id'] = job['job_id']
            return jobs
        except Exception as e:
            print(f"Error getting pending jobs: {str(e)}")
            return []
    
    def schedule_inspection_reminder(self, job: Dict) -> bool:
        """Schedule inspection reminder for the assigned agent."""
        try:
            # Parse inspection date and time
            inspection_datetime = f"{job['inspection_date']} {job['inspection_time']}"
            
            # Schedule reminder 30 minutes before inspection
            reminder_data = {
                'job_id': job['id'],
                'agent_phone': job['assigned_agent'],
                'property_details': job['property_details'],
                'client_details': job['client_details'],
                'inspection_date': job['inspection_date'],
                'inspection_time': job['inspection_time']
            }
            
            # Schedule the reminder
            reminder_scheduled = scheduler_service.schedule_inspection_reminder(reminder_data)
            
            # Also schedule the inspection start prompt
            start_prompt_scheduled = scheduler_service.schedule_inspection_start_prompt(reminder_data)
            
            return reminder_scheduled and start_prompt_scheduled
        except Exception as e:
            print(f"Error scheduling inspection reminder: {str(e)}")
            return False
    
    def notify_other_agents_job_taken(self, job: Dict, assigned_agent_phone: str) -> None:
        """Notify other agents that a job has been taken."""
        try:
            # Get all active agents
            active_agents = self.get_active_agents()
            
            for agent in active_agents:
                agent_phone = agent.get('phone')
                if agent_phone and agent_phone != assigned_agent_phone:
                    # Send notification that job is taken
                    self.whatsapp_service.send_job_taken_notification(
                        agent_phone,
                        job['property_details']
                    )
        except Exception as e:
            print(f"Error notifying other agents: {str(e)}")
    
    def handle_multiple_property_request(self, client_id: str, new_property_data: Dict) -> Dict:
        """Handle additional property inspection request for existing client."""
        try:
            # Get the agent currently assigned to this client
            client_jobs = self.get_jobs_by_client(client_id)
            if not client_jobs:
                return {"success": False, "error": "No existing agent found for client"}
            
            # Find the most recent active job for this client
            active_jobs = [job for job in client_jobs if job['status'] in ['assigned', 'approved']]
            if not active_jobs:
                return {"success": False, "error": "No active agent found for client"}
            
            # Get the agent from the most recent job
            agent_phone = active_jobs[0]['assigned_agent']
            client_name = active_jobs[0]['client_details'].get('name', 'Client')
            
            # Send notification to the agent
            result = self.whatsapp_service.send_multiple_property_notification(
                agent_phone,
                client_name,
                new_property_data
            )
            
            return {
                "success": True,
                "message": "Multiple property notification sent",
                "agent_phone": agent_phone,
                "result": result
            }
            
        except Exception as e:
            print(f"Error handling multiple property request: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_agent_details(self, agent_phone: str) -> Dict:
        """Get agent details by phone number."""
        try:
            agents = db_service.find_documents('agents', {'phone': agent_phone})
            if agents:
                agent = agents[0]
                return {
                    'name': agent.get('name', 'Unknown Agent'),
                    'phone': agent.get('phone', agent_phone),
                    'email': agent.get('email', 'N/A'),
                    'rating': agent.get('rating', 'N/A'),
                    'zone': agent.get('zone', 'N/A'),
                    'experience_years': agent.get('experience_years', 'N/A'),
                    'specializations': agent.get('specializations', [])
                }
            else:
                # Return basic info if agent not found in database
                return {
                    'name': 'Unknown Agent',
                    'phone': agent_phone,
                    'email': 'N/A',
                    'rating': 'N/A',
                    'zone': 'N/A',
                    'experience_years': 'N/A',
                    'specializations': []
                }
        except Exception as e:
            print(f"Error getting agent details: {str(e)}")
            return {
                'name': 'Unknown Agent',
                'phone': agent_phone,
                'email': 'N/A',
                'rating': 'N/A',
                'zone': 'N/A',
                'experience_years': 'N/A',
                'specializations': []
            }
