import os
from typing import Dict, Optional, Callable
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from app.services.whatsapp_service import WhatsAppService
from app.services.database import db_service

class SchedulerService:
    """Service for scheduling jobs and notifications."""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.whatsapp_service = WhatsAppService()
        self.start()
    
    def start(self):
        """Start the scheduler."""
        try:
            self.scheduler.start()
            print("Scheduler started successfully")
        except Exception as e:
            print(f"Failed to start scheduler: {str(e)}")
    
    def stop(self):
        """Stop the scheduler."""
        try:
            self.scheduler.shutdown()
            print("Scheduler stopped")
        except Exception as e:
            print(f"Failed to stop scheduler: {str(e)}")
    
    def schedule_inspection_reminder(self, inspection_data: Dict) -> bool:
        """Schedule an inspection reminder."""
        try:
            # Parse inspection date and time
            inspection_date_str = inspection_data.get('inspection_date', inspection_data.get('date'))
            inspection_time_str = inspection_data.get('inspection_time', '00:00')
            
            # Create datetime object
            inspection_datetime = datetime.fromisoformat(f"{inspection_date_str} {inspection_time_str}")
            
            # Schedule reminder 30 minutes before inspection (for testing, we'll use 1 minute)
            reminder_time = inspection_datetime - timedelta(minutes=1)
            
            if reminder_time > datetime.now():
                job_id = f"inspection_reminder_{inspection_data.get('job_id', 'unknown')}"
                
                self.scheduler.add_job(
                    func=self._send_inspection_reminder,
                    trigger=DateTrigger(run_date=reminder_time),
                    args=[inspection_data],
                    id=job_id,
                    replace_existing=True
                )
                
                print(f"Scheduled inspection reminder for {reminder_time}")
                return True
            else:
                print("Inspection time has already passed")
                return False
                
        except Exception as e:
            print(f"Failed to schedule inspection reminder: {str(e)}")
            return False
    
    def schedule_job_follow_up(self, job_data: Dict, follow_up_hours: int = 48) -> bool:
        """Schedule a job follow-up reminder."""
        try:
            follow_up_time = datetime.now() + timedelta(hours=follow_up_hours)
            job_id = f"job_followup_{job_data.get('id', 'unknown')}"
            
            self.scheduler.add_job(
                func=self._send_job_follow_up,
                trigger=DateTrigger(run_date=follow_up_time),
                args=[job_data],
                id=job_id,
                replace_existing=True
            )
            
            print(f"Scheduled job follow-up for {follow_up_time}")
            return True
            
        except Exception as e:
            print(f"Failed to schedule job follow-up: {str(e)}")
            return False
    
    def schedule_recurring_notifications(self, job_data: Dict, interval_hours: int = 24) -> bool:
        """Schedule recurring notifications for a job."""
        try:
            job_id = f"recurring_notification_{job_data.get('id', 'unknown')}"
            
            self.scheduler.add_job(
                func=self._send_job_status_update,
                trigger=IntervalTrigger(hours=interval_hours),
                args=[job_data],
                id=job_id,
                replace_existing=True
            )
            
            print(f"Scheduled recurring notifications every {interval_hours} hours")
            return True
            
        except Exception as e:
            print(f"Failed to schedule recurring notifications: {str(e)}")
            return False
    
    def schedule_daily_report(self, phone_number: str, time: str = "09:00") -> bool:
        """Schedule a daily report at a specific time."""
        try:
            job_id = f"daily_report_{phone_number}"
            
            self.scheduler.add_job(
                func=self._send_daily_report,
                trigger=CronTrigger(hour=time.split(':')[0], minute=time.split(':')[1]),
                args=[phone_number],
                id=job_id,
                replace_existing=True
            )
            
            print(f"Scheduled daily report for {time}")
            return True
            
        except Exception as e:
            print(f"Failed to schedule daily report: {str(e)}")
            return False
    
    def schedule_inspection_start_prompt(self, inspection_data: Dict) -> bool:
        """Schedule an inspection start prompt."""
        try:
            # Parse inspection date and time
            inspection_date_str = inspection_data.get('inspection_date', inspection_data.get('date'))
            inspection_time_str = inspection_data.get('inspection_time', '00:00')
            
            # Create datetime object
            inspection_datetime = datetime.fromisoformat(f"{inspection_date_str} {inspection_time_str}")
            
            # Schedule start prompt at inspection time
            if inspection_datetime > datetime.now():
                job_id = f"inspection_start_{inspection_data.get('job_id', 'unknown')}"
                
                self.scheduler.add_job(
                    func=self._send_inspection_start_prompt,
                    trigger=DateTrigger(run_date=inspection_datetime),
                    args=[inspection_data],
                    id=job_id,
                    replace_existing=True
                )
                
                print(f"Scheduled inspection start prompt for {inspection_datetime}")
                return True
            else:
                print("Inspection time has already passed")
                return False
                
        except Exception as e:
            print(f"Failed to schedule inspection start prompt: {str(e)}")
            return False
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled job."""
        try:
            self.scheduler.remove_job(job_id)
            print(f"Cancelled job: {job_id}")
            return True
        except Exception as e:
            print(f"Failed to cancel job {job_id}: {str(e)}")
            return False
    
    def get_scheduled_jobs(self) -> list:
        """Get all scheduled jobs."""
        try:
            return self.scheduler.get_jobs()
        except Exception as e:
            print(f"Failed to get scheduled jobs: {str(e)}")
            return []
    
    def _send_inspection_reminder(self, inspection_data: Dict):
        """Send inspection reminder message to both agent and client."""
        try:
            agent_phone = inspection_data.get('agent_phone')
            client_phone = inspection_data.get('client_details', {}).get('phone')
            property_details = inspection_data.get('property_details', {})
            client_details = inspection_data.get('client_details', {})
            
            # Send reminder to agent
            if agent_phone:
                message = f"""
🔔 INSPECTION REMINDER

Your inspection is scheduled to start in 1 minute!

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}
Client: {client_details.get('name', 'N/A')}
Date: {inspection_data.get('inspection_date', 'N/A')}
Time: {inspection_data.get('inspection_time', 'N/A')}

Please prepare to start the inspection.
Reply START when you begin the inspection.
                """.strip()
                
                result = self.whatsapp_service.send_message(agent_phone, message)
                if result['success']:
                    print(f"Inspection reminder sent to agent {agent_phone}")
                else:
                    print(f"Failed to send inspection reminder to agent: {result['error']}")
            
            # Send reminder to client
            if client_phone:
                # Get agent details for client notification
                from app.services.job_service import JobService
                job_service = JobService()
                agent_details = job_service.get_agent_details(agent_phone)
                
                result = self.whatsapp_service.send_inspection_reminder_to_client(
                    client_phone,
                    agent_details,
                    property_details,
                    inspection_data.get('inspection_date', 'N/A'),
                    inspection_data.get('inspection_time', 'N/A')
                )
                if result['success']:
                    print(f"Inspection reminder sent to client {client_phone}")
                else:
                    print(f"Failed to send inspection reminder to client: {result['error']}")
                    
        except Exception as e:
            print(f"Error sending inspection reminder: {str(e)}")
    
    def _send_inspection_start_prompt(self, inspection_data: Dict):
        """Send inspection start prompt message to both agent and client."""
        try:
            agent_phone = inspection_data.get('agent_phone')
            client_phone = inspection_data.get('client_details', {}).get('phone')
            property_details = inspection_data.get('property_details', {})
            client_details = inspection_data.get('client_details', {})
            
            # Send start prompt to agent
            if agent_phone:
                message = f"""
🚀 INSPECTION START TIME!

It's time to begin your inspection!

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}
Client: {client_details.get('name', 'N/A')}
Date: {inspection_data.get('inspection_date', 'N/A')}
Time: {inspection_data.get('inspection_time', 'N/A')}

Reply START to begin the inspection process.
Reply COMPLETE when you finish the inspection.
                """.strip()
                
                result = self.whatsapp_service.send_message(agent_phone, message)
                if result['success']:
                    print(f"Inspection start prompt sent to agent {agent_phone}")
                else:
                    print(f"Failed to send inspection start prompt to agent: {result['error']}")
            
            # Send start notification to client
            if client_phone:
                # Get agent details for client notification
                from app.services.job_service import JobService
                job_service = JobService()
                agent_details = job_service.get_agent_details(agent_phone)
                
                result = self.whatsapp_service.send_inspection_started_to_client(
                    client_phone,
                    agent_details,
                    property_details
                )
                if result['success']:
                    print(f"Inspection start notification sent to client {client_phone}")
                else:
                    print(f"Failed to send inspection start notification to client: {result['error']}")
                    
        except Exception as e:
            print(f"Error sending inspection start prompt: {str(e)}")
    
    def _send_job_follow_up(self, job_data: Dict):
        """Send job follow-up message."""
        try:
            phone_number = job_data.get('assigned_to')
            if phone_number:
                message = f"""
📋 Job Follow-up

Job: {job_data.get('title', 'N/A')}
Status: {job_data.get('status', 'N/A')}

Please provide an update on the progress of this job.
                """.strip()
                
                result = self.whatsapp_service.send_message(phone_number, message)
                if result['success']:
                    print(f"Job follow-up sent to {phone_number}")
                else:
                    print(f"Failed to send job follow-up: {result['error']}")
        except Exception as e:
            print(f"Error sending job follow-up: {str(e)}")
    
    def _send_job_status_update(self, job_data: Dict):
        """Send job status update message."""
        try:
            phone_number = job_data.get('assigned_to')
            if phone_number:
                result = self.whatsapp_service.send_job_status_update(phone_number, job_data)
                if result['success']:
                    print(f"Job status update sent to {phone_number}")
                else:
                    print(f"Failed to send job status update: {result['error']}")
        except Exception as e:
            print(f"Error sending job status update: {str(e)}")
    
    def _send_daily_report(self, phone_number: str):
        """Send daily report message."""
        try:
            # Get jobs for the day
            today = datetime.now().date()
            jobs = db_service.find_documents('jobs', {
                'created_at': {
                    '$gte': today.isoformat(),
                    '$lt': (today + timedelta(days=1)).isoformat()
                }
            })
            
            if jobs:
                message = f"""
📊 Daily Report - {today.strftime('%Y-%m-%d')}

Total Jobs: {len(jobs)}
Completed: {len([j for j in jobs if j.get('status') == 'completed'])}
Pending: {len([j for j in jobs if j.get('status') == 'pending'])}
In Progress: {len([j for j in jobs if j.get('status') == 'in_progress'])}

Have a great day!
                """.strip()
            else:
                message = f"""
📊 Daily Report - {today.strftime('%Y-%m-%d')}

No jobs created today.

Have a great day!
                """.strip()
            
            result = self.whatsapp_service.send_message(phone_number, message)
            if result['success']:
                print(f"Daily report sent to {phone_number}")
            else:
                print(f"Failed to send daily report: {result['error']}")
                
        except Exception as e:
            print(f"Error sending daily report: {str(e)}")

# Global scheduler service instance
scheduler_service = SchedulerService()
