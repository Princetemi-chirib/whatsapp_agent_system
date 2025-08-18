#!/usr/bin/env python3
"""
Add Timileyin Abdulazeez Agent Script
"""

import os
import sys
from datetime import datetime, timezone

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.database import db_service

def add_timileyin_agent():
    """Add Timileyin Abdulazeez as a new agent to the database."""
    
    # Agent data for Timileyin Abdulazeez
    agent_data = {
        "agent_id": "agent_004",
        "name": "Timileyin Abdulazeez",
        "phone": "+2347083321894",
        "email": "timileyin.abdulazeez@realestate.com",
        "status": "active",
        "zone": "Lagos",
        "specializations": ["Residential Properties", "Commercial Properties", "Luxury Homes"],
        "experience_years": 4,
        "rating": 4.8,
        "total_inspections": 120,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    print("Adding Timileyin Abdulazeez as a new agent...")
    print(f"Agent: {agent_data['name']}")
    print(f"Phone: {agent_data['phone']}")
    print(f"Zone: {agent_data['zone']}")
    print(f"Specializations: {', '.join(agent_data['specializations'])}")
    
    try:
        # Add agent to database
        result = db_service.insert_document("agents", agent_data)
        
        if result:
            print("✅ Timileyin Abdulazeez added successfully!")
            print(f"Agent ID: {result}")
            
            # Verify the agent was added
            agents = db_service.find_documents("agents", {"phone": "+2347083321894"})
            if agents:
                print(f"✅ Verification: Found {len(agents)} agent(s) with phone +2347083321894")
                for agent in agents:
                    print(f"   - {agent.get('name', 'Unknown')} ({agent.get('phone', 'No phone')})")
            else:
                print("❌ Verification failed: Agent not found in database")
        else:
            print("❌ Failed to add agent to database")
            
    except Exception as e:
        print(f"❌ Error adding agent: {str(e)}")

if __name__ == "__main__":
    add_timileyin_agent()
