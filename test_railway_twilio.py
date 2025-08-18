#!/usr/bin/env python3
"""
Test Railway Twilio Service
"""

import requests
import json

def test_railway_twilio():
    """Test Railway app's Twilio service."""
    
    print("🧪 Testing Railway app's Twilio service...")
    
    # Test data
    test_data = {
        "to_number": "+2347055699437",
        "message": "🧪 Railway Twilio Test: Testing if Railway can send WhatsApp messages"
    }
    
    try:
        # Make a request to Railway app to test Twilio
        response = requests.post(
            "https://web-production-8cec.up.railway.app/api/test-twilio-send",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Railway Twilio test successful!")
        else:
            print("❌ Railway Twilio test failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_railway_twilio()
