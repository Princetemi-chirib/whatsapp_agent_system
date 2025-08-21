"""
Test Client Notifications Script

This script tests the new client notification functionality that sends WhatsApp messages
to clients when agents accept, confirm, start, and complete inspections.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"  # Change this to your deployed URL

def test_client_notifications():
    """Test the complete client notification flow."""
    
    print("🧪 Testing Client Notifications")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # Create inspection job data
    tomorrow = datetime.now() + timedelta(days=1)
    inspection_date = tomorrow.strftime("%Y-%m-%d")
    
    job_data = {
        "property": {
            "property_id": "test_client_001",
            "title": "4-Bedroom Villa in Victoria Island",
            "address": "456 Victoria Island, Lagos",
            "property_type": "Villa",
            "bedrooms": 4,
            "bathrooms": 3,
            "price": 75000000,
            "area": "250 sqm"
        },
        "client": {
            "client_id": "test_client_001",
            "name": "Sarah Johnson",
            "phone": "+2349069208467",  # Using the provided customer number
            "email": "sarah.johnson@email.com"
        },
        "inspection_date": inspection_date,
        "inspection_time": "15:00",
        "notes": "Testing client notification system"
    }
    
    try:
        print("\n📋 Step 1: Creating inspection job...")
        response = requests.post(f"{BASE_URL}/api/jobs/", json=job_data, timeout=30)
        
        if response.status_code == 201:
            job_response = response.json()
            job_id = job_response.get("job_id")
            print(f"✅ Job created successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {job_response.get('status')}")
            print(f"   Client: {job_data['client']['name']} ({job_data['client']['phone']})")
            
            print("\n📱 Step 2: Simulating agent acceptance...")
            print("   Agent should reply 'YES' to accept the job")
            print("   Client should receive agent details notification")
            
            print("\n📅 Step 3: Simulating schedule confirmation...")
            print("   Agent should reply 'CONFIRM' to confirm schedule")
            print("   Client should receive schedule confirmation")
            
            print("\n🔔 Step 4: Testing reminders...")
            print("   Reminders will be sent 1 minute before inspection time")
            print("   Both agent and client will receive reminders")
            
            print("\n🚀 Step 5: Testing start notification...")
            print("   Start prompt will be sent at exact inspection time")
            print("   Both agent and client will receive start notifications")
            
            print("\n✅ Step 6: Testing completion...")
            print("   Agent should reply 'COMPLETE' to finish inspection")
            print("   Client should receive completion notification")
            
            print(f"\n🎯 Test Job Details:")
            print(f"   Property: {job_data['property']['title']}")
            print(f"   Address: {job_data['property']['address']}")
            print(f"   Date: {inspection_date}")
            print(f"   Time: 15:00")
            print(f"   Client: {job_data['client']['name']} ({job_data['client']['phone']})")
            
            print(f"\n📞 To test manually:")
            print(f"   1. Send 'YES' from agent WhatsApp to accept job")
            print(f"   2. Send 'CONFIRM' from agent WhatsApp to confirm schedule")
            print(f"   3. Wait for reminders and start prompts")
            print(f"   4. Send 'START' then 'COMPLETE' from agent WhatsApp")
            
            return job_id
        else:
            print(f"❌ Job creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing client notifications: {str(e)}")
        return None

def test_webhook_simulation():
    """Simulate webhook calls for testing."""
    
    print("\n🔗 Testing Webhook Simulations")
    print("=" * 40)
    
    # Simulate agent accepting job
    print("\n📱 Simulating agent acceptance...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",  # Agent phone number
        "Body": "YES"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Agent acceptance webhook processed successfully")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error simulating webhook: {str(e)}")

def test_complete_flow():
    """Test the complete flow with webhook simulations."""
    
    print("\n🔄 Testing Complete Flow with Webhook Simulations")
    print("=" * 60)
    
    # Step 1: Create job
    job_id = test_client_notifications()
    
    if not job_id:
        print("❌ Failed to create job. Cannot proceed with flow test.")
        return
    
    # Step 2: Simulate agent accepting job
    print(f"\n📱 Step 2: Simulating agent acceptance for job {job_id}...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",  # Agent phone number
        "Body": "YES"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Agent acceptance processed successfully")
            print("   Client should have received agent details notification")
        else:
            print(f"❌ Agent acceptance failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error simulating agent acceptance: {str(e)}")
    
    # Step 3: Simulate agent confirming schedule
    print(f"\n📅 Step 3: Simulating schedule confirmation...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",  # Agent phone number
        "Body": "CONFIRM"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Schedule confirmation processed successfully")
            print("   Client should have received schedule confirmation")
        else:
            print(f"❌ Schedule confirmation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error simulating schedule confirmation: {str(e)}")
    
    # Step 4: Simulate agent starting inspection
    print(f"\n🚀 Step 4: Simulating inspection start...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",  # Agent phone number
        "Body": "START"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Inspection start processed successfully")
            print("   Client should have received start notification")
        else:
            print(f"❌ Inspection start failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error simulating inspection start: {str(e)}")
    
    # Step 5: Simulate agent completing inspection
    print(f"\n✅ Step 5: Simulating inspection completion...")
    webhook_data = {
        "From": "whatsapp:+2347055699437",  # Agent phone number
        "Body": "COMPLETE"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/webhooks/twilio/whatsapp",
            data=webhook_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Inspection completion processed successfully")
            print("   Client should have received completion notification")
        else:
            print(f"❌ Inspection completion failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error simulating inspection completion: {str(e)}")
    
    print(f"\n🎉 Complete flow test finished!")
    print(f"Check WhatsApp messages for customer: +2349069208467")
    print(f"They should have received notifications at each step!")

if __name__ == "__main__":
    print("🧪 Client Notification System Test")
    print("=" * 50)
    print("This test will create an inspection job and demonstrate")
    print("the new client notification functionality.")
    print("Customer Phone: +2349069208467")
    print("=" * 50)
    
    # Test the complete flow with webhook simulations
    test_complete_flow()
    
    print(f"\n📱 Summary:")
    print(f"Customer +2349069208467 should have received:")
    print(f"   1. ✅ Agent assignment notification with agent details")
    print(f"   2. 📅 Schedule confirmation notification")
    print(f"   3. 🔔 Reminder notification (if scheduled)")
    print(f"   4. 🚀 Start notification")
    print(f"   5. ✅ Completion notification")
    
    print(f"\n🔍 To verify:")
    print(f"   - Check WhatsApp messages on +2349069208467")
    print(f"   - Each notification should include agent details")
    print(f"   - Messages should be professional and informative")
