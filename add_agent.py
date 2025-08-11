"""
Add Agent Script for WhatsApp Agent Dispatch System

This script adds a new agent to the database with the specified phone number.
"""

import os
import sys
from datetime import datetime, timezone

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.database import db_service

def add_agent():
    """Add a new agent to the database."""
    
    # Agent data
    agent_data = {
        "agent_id": "agent_003",
        "name": "Michael Johnson",
        "phone": "+2347055699437",
        "email": "michael.johnson@realestate.com",
        "status": "active",
        "zone": "Ikeja",
        "specializations": ["Apartments", "Commercial Properties"],
        "experience_years": 6,
        "rating": 4.7,
        "total_inspections": 180,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    print("Adding new agent to the database...")
    print(f"Agent: {agent_data['name']}")
    print(f"Phone: {agent_data['phone']}")
    print(f"Zone: {agent_data['zone']}")
    
    try:
        # Add agent to database
        result = db_service.insert_document("agents", agent_data)
        
        if result:
            print("✅ Agent added successfully!")
            print(f"Agent ID: {result}")
            
            # Verify the agent was added
            agents = db_service.find_documents("agents", {"phone": "+2347055699437"})
            if agents:
                print(f"✅ Verification: Found {len(agents)} agent(s) with phone +2347055699437")
                for agent in agents:
                    print(f"   - {agent.get('name', 'Unknown')} ({agent.get('phone', 'No phone')})")
            else:
                print("❌ Verification failed: Agent not found in database")
        else:
            print("❌ Failed to add agent to database")
            
    except Exception as e:
        print(f"❌ Error adding agent: {str(e)}")

if __name__ == "__main__":
    add_agent()
