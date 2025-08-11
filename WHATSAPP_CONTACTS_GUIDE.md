# WhatsApp Contacts Management Guide

## 📱 **How WhatsApp Business API Works**

### **Key Points:**
- ❌ **No traditional contact list** like regular WhatsApp
- ✅ **Recipients must opt-in** to receive messages
- ✅ **Messages sent to phone numbers** (with opt-in)
- ✅ **No contact management** required in Twilio

## 🔧 **Adding Recipients (Development/Sandbox)**

### **Step 1: Get Your Sandbox Code**
1. Go to **Twilio Console**: https://console.twilio.com/
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. You'll see your **sandbox code** (e.g., "join abc-123-xyz")

### **Step 2: Have Recipients Join**
Each person who should receive messages needs to:

1. **Open WhatsApp** on their phone
2. **Send a message** to `+14155238886` (your Twilio WhatsApp number)
3. **Message content**: `join abc-123-xyz` (replace with your actual sandbox code)

### **Step 3: Verify Success**
- Recipients will receive: *"You have successfully joined the WhatsApp Business API Sandbox"*
- They're now part of your sandbox
- You can send them messages

## 🏠 **Managing Real Estate Agents**

### **Using the Agent Management Script**
```bash
python manage_agents.py
```

This script helps you:
- ✅ **Add new agents** to your database
- ✅ **List all agents** in the system
- ✅ **Update agent status** (active/inactive)
- ✅ **Get sandbox instructions**

### **Adding Agents Step by Step**

1. **Run the script**: `python manage_agents.py`
2. **Select option 1**: "Add New Agent"
3. **Enter agent details**:
   - Agent ID: `agent_001`
   - Name: `John Smith`
   - Phone: `+2348012345678` (with country code)
   - Email: `john.smith@realestate.com`
   - Zone: `Lekki`
4. **Add specializations**: Apartments, Houses, etc.
5. **Enter experience**: Years of experience

### **Example Agent Data**
```json
{
  "agent_id": "agent_001",
  "name": "John Smith",
  "phone": "+2348012345678",
  "email": "john.smith@realestate.com",
  "status": "active",
  "zone": "Lekki",
  "specializations": ["Apartments", "Houses"],
  "experience_years": 5,
  "rating": 4.8,
  "total_inspections": 0
}
```

## 📋 **Workflow for Adding New Agents**

### **1. Agent Joins WhatsApp Sandbox**
```
Agent sends: "join abc-123-xyz" to +14155238886
Agent receives: "You have successfully joined the WhatsApp Business API Sandbox"
```

### **2. Add Agent to Database**
```bash
python manage_agents.py
# Select option 1: Add New Agent
# Enter agent details
```

### **3. Agent Receives Inspection Requests**
- When inspection requests are created, all active agents receive WhatsApp messages
- First agent to reply "YES" gets assigned the job

## 🚀 **For Production (Full WhatsApp Business API)**

### **Opt-in Process:**
1. **Recipients must explicitly opt-in** to receive messages
2. **No sandbox limitations** - can message any phone number
3. **Higher message limits** and full features

### **Opt-in Methods:**
- **Web opt-in**: Website form with phone number
- **SMS opt-in**: Send SMS with opt-in link
- **QR code**: Scan QR code to opt-in
- **Manual opt-in**: Customer service process

## 📊 **Managing Agent Status**

### **Active Agents**
- ✅ **Receive inspection requests** via WhatsApp
- ✅ **Can respond** to job assignments
- ✅ **Get reminders** and notifications

### **Inactive Agents**
- ❌ **Don't receive** inspection requests
- ❌ **Can't respond** to job assignments
- ❌ **No notifications** sent

### **Update Agent Status**
```bash
python manage_agents.py
# Select option 3: Update Agent Status
# Enter phone number and new status
```

## 🔍 **Testing Your Setup**

### **1. Test Agent Addition**
```bash
python manage_agents.py
# Add a test agent with your phone number
```

### **2. Test WhatsApp Sending**
```bash
# Create an inspection request
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

### **3. Test Agent Response**
```bash
# Simulate agent responding "YES"
curl -X POST "http://localhost:5000/api/webhooks/twilio/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+2348012345678&Body=YES"
```

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **"Agent not receiving messages"**
   - Check if agent joined sandbox
   - Verify phone number format (+country code)
   - Ensure agent status is "active"

2. **"Sandbox code not working"**
   - Get fresh sandbox code from Twilio Console
   - Ensure exact format: "join abc-123-xyz"
   - Check if sandbox is still active

3. **"Phone number not found"**
   - Verify phone number in database
   - Check country code format
   - Ensure agent exists in system

### **Support Resources:**
- **Twilio WhatsApp Docs**: https://www.twilio.com/docs/whatsapp
- **Sandbox Guide**: https://www.twilio.com/docs/whatsapp/sandbox
- **Agent Management**: Use `python manage_agents.py`

## 📞 **Quick Commands**

### **List All Agents**
```bash
python manage_agents.py
# Select option 2: List All Agents
```

### **Add New Agent**
```bash
python manage_agents.py
# Select option 1: Add New Agent
```

### **Get Sandbox Instructions**
```bash
python manage_agents.py
# Select option 4: WhatsApp Sandbox Instructions
```

Your WhatsApp Agent Dispatch System is ready to manage real estate agents and send them inspection requests! 🚀

