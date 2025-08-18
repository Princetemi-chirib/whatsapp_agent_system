#!/usr/bin/env python3
"""
Add Agent via Railway App
"""

import requests
import json
from datetime import datetime, timezone

def add_agent_via_railway():
    """Add Timileyin Abdulazeez via Railway app."""
    
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
    
    print("Adding Timileyin Abdulazeez via Railway app...")
    print(f"Agent: {agent_data['name']}")
    print(f"Phone: {agent_data['phone']}")
    
    try:
        # Try to add agent via a custom endpoint (we'll create this)
        # For now, let's create a test inspection that will trigger the agent addition
        inspection_data = {
            "property": {
                "property_id": "agent_add_test_001",
                "title": "Agent Addition Test Property",
                "address": "Test Address for Agent Addition",
                "property_type": "Test",
                "bedrooms": 1,
                "bathrooms": 1,
                "price": 1000000,
                "area": "50 sqm"
            },
            "client": {
                "client_id": "agent_add_client_001",
                "name": "Agent Add Test Client",
                "phone": "+2348012345678",
                "email": "agentadd@test.com"
            },
            "inspection_date": datetime.now().strftime("%Y-%m-%d"),
            "inspection_time": datetime.now().strftime("%H:%M"),
            "notes": "Testing agent addition"
        }
        
        # Create inspection to trigger agent lookup
        response = requests.post(
            f"{railway_url}/api/jobs/",
            headers={"Content-Type": "application/json"},
            json=inspection_data
        )
        
        if response.status_code == 201:
            print("✅ Inspection created successfully!")
            print("Now the Railway app will look for agents in its database.")
            print("Since Timileyin Abdulazeez is not in the database, only existing agents will receive the message.")
            
            # Now let's manually add the agent by creating a simple script that Railway can execute
            print("\n🔧 To add the agent to Railway database, you need to:")
            print("1. Go to Railway Dashboard")
            print("2. Open your project's shell/terminal")
            print("3. Run the agent addition script")
            
        else:
            print(f"❌ Failed to create inspection. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    add_agent_via_railway()
