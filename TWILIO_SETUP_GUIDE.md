# Twilio Setup Guide for WhatsApp Agent Dispatch System

## 🚀 Quick Setup Steps

### Step 1: Create Twilio Account
1. Go to https://www.twilio.com/
2. Click "Sign up for free"
3. Fill in your details and verify email/phone

### Step 2: Get Account Credentials
1. Log into https://console.twilio.com/
2. On the dashboard, you'll see:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: `[Click to show]` (click to reveal)

### Step 3: Enable WhatsApp Business API
1. In Twilio Console → **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Click **"Join the WhatsApp Business API Sandbox"**
3. Follow the sandbox activation instructions

### Step 4: Get WhatsApp Number
1. In the sandbox, you'll see your WhatsApp number: `+14155238886`
2. This is your `TWILIO_WHATSAPP_NUMBER`

### Step 5: Activate Sandbox
1. Send the join message from your phone to `+14155238886`
2. Format: `join <your-sandbox-code>`

### Step 6: Update Environment Variables

Replace the values in your `.env` file:

```env
# Twilio WhatsApp API Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
```

## 📱 WhatsApp Business API Sandbox

### What is the Sandbox?
- **Free testing environment** for WhatsApp Business API
- **Limited to 1000 messages per month** (free tier)
- **Perfect for development and testing**

### Sandbox Limitations:
- ✅ **Free to use**
- ✅ **1000 messages/month**
- ✅ **Real WhatsApp messages**
- ❌ **Limited to sandbox participants**
- ❌ **Not for production use**

### For Production:
- **Apply for WhatsApp Business API** through Twilio
- **Get verified business account**
- **Higher message limits**
- **Full WhatsApp Business features**

## 🔧 Testing Your Setup

### 1. Test WhatsApp Sending
```bash
# Test sending a message
curl -X POST "http://localhost:5000/api/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "property": {
      "property_id": "test_001",
      "title": "Test Property",
      "address": "123 Test Street",
      "property_type": "Apartment",
      "bedrooms": 2,
      "bathrooms": 1,
      "price": 30000000,
      "area": "100 sqm"
    },
    "client": {
      "client_id": "test_client_001",
      "name": "Test Client",
      "phone": "+2348012345678",
      "email": "test@example.com"
    },
    "inspection_date": "2024-01-20",
    "inspection_time": "10:00",
    "notes": "Test inspection request"
  }'
```

### 2. Test Webhook (Agent Response)
```bash
# Simulate agent responding "YES"
curl -X POST "http://localhost:5000/api/webhooks/twilio/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+2348012345678&Body=YES"
```

## 💰 Pricing Information

### Free Tier (Sandbox):
- **$0/month**
- **1000 messages/month**
- **Perfect for development**

### Production Pricing:
- **$0.005 per message** (outbound)
- **$0.005 per message** (inbound)
- **No monthly fees**
- **Pay only for what you use**

## 🛠️ Troubleshooting

### Common Issues:

1. **"Twilio credentials not configured"**
   - Check your `.env` file
   - Ensure all three variables are set

2. **"Authentication failed"**
   - Verify Account SID and Auth Token
   - Check for extra spaces or characters

3. **"WhatsApp number not found"**
   - Ensure you've joined the sandbox
   - Check the WhatsApp number format

4. **"Message delivery failed"**
   - Verify recipient has joined sandbox
   - Check message format

### Support Resources:
- **Twilio Documentation**: https://www.twilio.com/docs/whatsapp
- **Twilio Support**: https://support.twilio.com/
- **WhatsApp Business API**: https://developers.facebook.com/docs/whatsapp

## 🔒 Security Best Practices

1. **Never commit credentials to Git**
2. **Use environment variables**
3. **Rotate Auth Token regularly**
4. **Monitor usage in Twilio Console**
5. **Set up webhook validation**

## 📞 Next Steps

1. **Complete the setup** using this guide
2. **Test with sample inspection requests**
3. **Add real agent phone numbers** to the sandbox
4. **Deploy to production** when ready
5. **Apply for full WhatsApp Business API** for production use

Your WhatsApp Agent Dispatch System will be fully functional once you complete these steps!

