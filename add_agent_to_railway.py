#!/usr/bin/env python3
"""
Add Agent to Railway Database via API
"""

import requests
import json
from datetime import datetime, timezone

def add_agent_to_railway():
    """Add Timileyin Abdulazeez to Railway database via API."""
    
    # Railway app URL
    railway_url = "https://web-production-8cec.up.railway.app"
    
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
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    print("Adding Timileyin Abdulazeez to Railway database...")
    print(f"Agent: {agent_data['name']}")
    print(f"Phone: {agent_data['phone']}")
    
    try:
        # Add agent to Railway database
        response = requests.post(
            f"{railway_url}/api/agents/",
            headers={"Content-Type": "application/json"},
            json=agent_data
        )
        
        if response.status_code == 201:
            print("✅ Timileyin Abdulazeez added to Railway database successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Failed to add agent to Railway. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error adding agent to Railway: {str(e)}")

if __name__ == "__main__":
    add_agent_to_railway()
