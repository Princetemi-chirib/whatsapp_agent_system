import os
import requests
from typing import Dict, Optional, List
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

class WhatsAppService:
    """Service for handling Twilio WhatsApp API interactions."""
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not configured")
    
    def send_message(self, to_number: str, message: str) -> Dict:
        """Send a WhatsApp message using Twilio."""
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "Twilio client not configured"
                }
            
            # Format the number for WhatsApp
            if not to_number.startswith('whatsapp:'):
                to_number = f"whatsapp:{to_number}"
            
            from_number = f"whatsapp:{self.whatsapp_number}"
            
            message_obj = self.client.messages.create(
                from_=from_number,
                body=message,
                to=to_number
            )
            
            return {
                "success": True,
                "message_id": message_obj.sid,
                "timestamp": datetime.utcnow().isoformat(),
                "status": message_obj.status
            }
                
        except TwilioException as e:
            return {
                "success": False,
                "error": f"Twilio API error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send WhatsApp message: {str(e)}"
            }
    
    def send_inspection_request_to_agents(self, property_details: Dict, inspection_date: str, inspection_time: str, agent_numbers: List[str]) -> Dict:
        """Send inspection request to all available agents."""
        message = f"""
🏠 New Inspection Request

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}
Type: {property_details.get('property_type', 'N/A')}
Bedrooms: {property_details.get('bedrooms', 'N/A')}
Bathrooms: {property_details.get('bathrooms', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

Reply YES to accept this inspection request.
        """.strip()
        
        results = []
        for agent_number in agent_numbers:
            result = self.send_message(agent_number, message)
            results.append({
                "agent_number": agent_number,
                "result": result
            })
        
        return {
            "success": True,
            "message": "Inspection requests sent to all agents",
            "results": results
        }
    
    def send_job_assigned_confirmation(self, agent_number: str, property_details: Dict, client_details: Dict, inspection_date: str, inspection_time: str) -> Dict:
        """Send confirmation when job is assigned to an agent."""
        message = f"""
✅ Inspection Assigned!

You have been assigned to conduct an inspection.

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}
Client: {client_details.get('name', 'N/A')}
Client Phone: {client_details.get('phone', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

Please confirm the schedule by replying CONFIRM.
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_job_already_assigned(self, agent_number: str, property_details: Dict) -> Dict:
        """Send notification that job is already assigned."""
        message = f"""
❌ Job Already Assigned

The inspection request for {property_details.get('title', 'N/A')} has already been assigned to another agent.

Thank you for your interest!
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_job_taken_notification(self, agent_number: str, property_details: Dict) -> Dict:
        """Send notification that a job has been taken by another agent."""
        message = f"""
📢 Job Update

The inspection request for {property_details.get('title', 'N/A')} has been assigned to another agent.

Keep an eye out for new inspection requests!
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_inspection_reminder(self, agent_number: str, property_details: Dict, client_details: Dict, inspection_date: str, inspection_time: str) -> Dict:
        """Send inspection reminder to assigned agent."""
        message = f"""
🔔 Inspection Reminder

It's time to start your inspection!

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}
Client: {client_details.get('name', 'N/A')}
Client Phone: {client_details.get('phone', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

Please proceed to the property location.
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_schedule_confirmation(self, agent_number: str, property_details: Dict, inspection_date: str, inspection_time: str) -> Dict:
        """Send confirmation when agent confirms inspection schedule."""
        message = f"""
✅ Schedule Confirmed!

Your inspection has been confirmed.

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

You will receive a reminder at the scheduled time.
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_inspection_started_confirmation(self, agent_number: str, property_details: Dict) -> Dict:
        """Send confirmation when inspection is started."""
        message = f"""
🚀 Inspection Started!

You have successfully started your inspection.

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Please conduct a thorough inspection and reply COMPLETE when finished.
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_inspection_completed_confirmation(self, agent_number: str, property_details: Dict) -> Dict:
        """Send confirmation when inspection is completed."""
        message = f"""
✅ Inspection Completed!

Thank you for completing the inspection for {property_details.get('title', 'N/A')}.

Your report has been submitted successfully.
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_multiple_property_notification(self, agent_number: str, client_name: str, new_property_details: Dict) -> Dict:
        """Send notification for additional property inspection for same client."""
        message = f"""
🏠 Additional Inspection Request

Your client {client_name} has requested an inspection for another property.

Property: {new_property_details.get('title', 'N/A')}
Address: {new_property_details.get('address', 'N/A')}
Type: {new_property_details.get('property_type', 'N/A')}

Reply YES to accept this additional inspection.
        """.strip()
        
        return self.send_message(agent_number, message)
    
    def send_daily_summary(self, agent_number: str, summary_data: Dict) -> Dict:
        """Send daily summary to agent."""
        message = f"""
📊 Daily Summary - {datetime.now().strftime('%Y-%m-%d')}

Total Inspections: {summary_data.get('total', 0)}
Completed: {summary_data.get('completed', 0)}
Pending: {summary_data.get('pending', 0)}
In Progress: {summary_data.get('in_progress', 0)}

Have a great day!
        """.strip()
        
        return self.send_message(agent_number, message)

    # New methods for client notifications
    
    def send_agent_assigned_to_client(self, client_phone: str, agent_details: Dict, property_details: Dict, inspection_date: str, inspection_time: str) -> Dict:
        """Send notification to client when agent is assigned."""
        message = f"""
✅ Agent Assigned!

Great news! An agent has been assigned to your inspection.

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Agent Details:
👤 Name: {agent_details.get('name', 'N/A')}
📞 Phone: {agent_details.get('phone', 'N/A')}
📧 Email: {agent_details.get('email', 'N/A')}
⭐ Rating: {agent_details.get('rating', 'N/A')}/5
🏢 Zone: {agent_details.get('zone', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

The agent will contact you shortly to confirm the schedule.
        """.strip()
        
        return self.send_message(client_phone, message)
    
    def send_schedule_confirmed_to_client(self, client_phone: str, agent_details: Dict, property_details: Dict, inspection_date: str, inspection_time: str) -> Dict:
        """Send notification to client when agent confirms schedule."""
        message = f"""
📅 Schedule Confirmed!

Your inspection schedule has been confirmed by the agent.

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Agent: {agent_details.get('name', 'N/A')}
Phone: {agent_details.get('phone', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

You will receive a reminder 30 minutes before the inspection.
        """.strip()
        
        return self.send_message(client_phone, message)
    
    def send_inspection_reminder_to_client(self, client_phone: str, agent_details: Dict, property_details: Dict, inspection_date: str, inspection_time: str) -> Dict:
        """Send inspection reminder to client."""
        message = f"""
🔔 Inspection Reminder

Your inspection is scheduled to start in 30 minutes!

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Agent: {agent_details.get('name', 'N/A')}
Phone: {agent_details.get('phone', 'N/A')}

Inspection Date: {inspection_date}
Inspection Time: {inspection_time}

Please ensure someone is available at the property for the inspection.
        """.strip()
        
        return self.send_message(client_phone, message)
    
    def send_inspection_started_to_client(self, client_phone: str, agent_details: Dict, property_details: Dict) -> Dict:
        """Send notification to client when inspection starts."""
        message = f"""
🚀 Inspection Started!

Your inspection has begun!

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Agent: {agent_details.get('name', 'N/A')}
Phone: {agent_details.get('phone', 'N/A')}

The agent is now conducting the inspection. You will be notified when it's completed.
        """.strip()
        
        return self.send_message(client_phone, message)
    
    def send_inspection_completed_to_client(self, client_phone: str, agent_details: Dict, property_details: Dict) -> Dict:
        """Send notification to client when inspection is completed."""
        message = f"""
✅ Inspection Completed!

Your inspection has been completed successfully!

Property: {property_details.get('title', 'N/A')}
Address: {property_details.get('address', 'N/A')}

Agent: {agent_details.get('name', 'N/A')}
Phone: {agent_details.get('phone', 'N/A')}

The inspection report will be available shortly. Thank you for choosing our service!
        """.strip()
        
        return self.send_message(client_phone, message)
