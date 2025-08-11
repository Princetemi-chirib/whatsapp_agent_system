"""
Check Agents Script for WhatsApp Agent Dispatch System

This script checks what agents are currently in the database.
"""

import os
import sys
from datetime import datetime, timezone

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.database import db_service

def check_agents():
    """Check all agents in the database."""
    
    print("Checking agents in the database...")
    
    try:
        # Get all agents
        agents = db_service.find_documents("agents", {})
        
        if agents:
            print(f"✅ Found {len(agents)} agent(s) in the database:")
            print("-" * 60)
            for i, agent in enumerate(agents, 1):
                print(f"{i}. {agent.get('name', 'Unknown')}")
                print(f"   Phone: {agent.get('phone', 'No phone')}")
                print(f"   Email: {agent.get('email', 'No email')}")
                print(f"   Zone: {agent.get('zone', 'No zone')}")
                print(f"   Status: {agent.get('status', 'Unknown')}")
                print(f"   Experience: {agent.get('experience_years', 0)} years")
                print(f"   Rating: {agent.get('rating', 0)}")
                print(f"   Total Inspections: {agent.get('total_inspections', 0)}")
                print("-" * 60)
        else:
            print("❌ No agents found in the database")
            
    except Exception as e:
        print(f"❌ Error checking agents: {str(e)}")

if __name__ == "__main__":
    check_agents()
