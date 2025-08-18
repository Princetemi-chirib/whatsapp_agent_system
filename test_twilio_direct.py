#!/usr/bin/env python3
"""
Direct Twilio WhatsApp Test
"""

import os
import requests
from twilio.rest import Client

def test_twilio_whatsapp():
    """Test direct Twilio WhatsApp message sending."""
    
    # Twilio credentials - UPDATED
    account_sid = "AC66c9a7b9f8b5ca7f1ae1eea72ee8bda2"
    auth_token = "ce4dc319eeb92f1250822f27c4b8e419"
    from_number = "+14155238886"  # WhatsApp sandbox number
    to_number = "+2347055699437"
    
    try:
        # Create Twilio client
        client = Client(account_sid, auth_token)
        
        # Send WhatsApp message
        message = client.messages.create(
            from_=f'whatsapp:{from_number}',
            body='🧪 Updated Twilio Test: Testing with new auth token and sandbox number',
            to=f'whatsapp:{to_number}'
        )
        
        print(f"✅ Message sent successfully!")
        print(f"Message SID: {message.sid}")
        print(f"Status: {message.status}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing direct Twilio WhatsApp message with new credentials...")
    test_twilio_whatsapp()
