#!/usr/bin/env python3
"""
Check and Add Agents Script
"""

import os
import sys
from datetime import datetime, timezone

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.database import db_service

def check_and_add_agent():
    """Check if agents exist and add one if needed."""
    
    print("🔍 Checking agents in database...")
    
    try:
        # Check if agents collection exists and has agents
        agents = db_service.find_documents("agents", {})
        print(f"Found {len(agents)} agents in database")
        
        if agents:
            print("📋 Existing agents:")
            for agent in agents:
                print(f"  - {agent.get('name', 'Unknown')} ({agent.get('phone', 'No phone')}) - {agent.get('status', 'Unknown status')}")
        else:
            print("❌ No agents found in database!")
            print("➕ Adding test agent...")
            
            # Add a test agent
            agent_data = {
                "agent_id": "agent_test_001",
                "name": "Test Agent",
                "phone": "+2347055699437",
                "email": "test.agent@realestate.com",
                "status": "active",
                "zone": "Lagos",
                "specializations": ["Residential", "Commercial"],
                "experience_years": 3,
                "rating": 4.5,
                "total_inspections": 50,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
            
            result = db_service.insert_document("agents", agent_data)
            if result:
                print("✅ Test agent added successfully!")
                print(f"Agent: {agent_data['name']} ({agent_data['phone']})")
            else:
                print("❌ Failed to add test agent")
        
        # Check active agents specifically
        active_agents = db_service.find_documents("agents", {"status": "active"})
        print(f"\n📱 Active agents: {len(active_agents)}")
        for agent in active_agents:
            print(f"  - {agent.get('name', 'Unknown')} ({agent.get('phone', 'No phone')})")
            
    except Exception as e:
        print(f"❌ Error checking agents: {str(e)}")

if __name__ == "__main__":
    check_and_add_agent()
