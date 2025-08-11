# Environment Variables Setup Guide

## 🔧 Complete .env File Configuration

Here's your complete `.env` file with all the values you need:

```env
# WhatsApp Agent System Environment Variables

# FastAPI Configuration
HOST=0.0.0.0
PORT=5000

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=whatsapp_agent_system

# Twilio WhatsApp API Configuration
# Get these from: https://console.twilio.com/
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886

# Security
# Generated using: python generate_secret_key.py
SECRET_KEY=b2rsOSFOhpKeJ_6QJUKOySAgH0b0L1-YT54dJXBgFdw

# Logging
LOG_LEVEL=INFO
```

## 🔑 Where Each Value Comes From

### **1. SECRET_KEY**
- **Source**: Generated locally (not from any service)
- **How to get**: Run `python generate_secret_key.py`
- **Example**: `SECRET_KEY=b2rsOSFOhpKeJ_6QJUKOySAgH0b0L1-YT54dJXBgFdw`

### **2. TWILIO_ACCOUNT_SID**
- **Source**: Twilio Console Dashboard
- **How to get**: https://console.twilio.com/ → Dashboard
- **Format**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### **3. TWILIO_AUTH_TOKEN**
- **Source**: Twilio Console Dashboard
- **How to get**: https://console.twilio.com/ → Dashboard → Click "Show"
- **Format**: `your_actual_auth_token_here`

### **4. TWILIO_WHATSAPP_NUMBER**
- **Source**: WhatsApp Business API Sandbox
- **How to get**: Twilio Console → Messaging → Try WhatsApp → Join Sandbox
- **Format**: `+14155238886` (usually this number for sandbox)

### **5. MONGODB_URI**
- **Source**: Your MongoDB installation
- **Local**: `mongodb://localhost:27017`
- **Cloud**: `mongodb+srv://username:password@cluster.mongodb.net`

### **6. MONGODB_DB_NAME**
- **Source**: You choose this name
- **Recommended**: `whatsapp_agent_system`

## 🚀 Quick Setup Steps

### **Step 1: Generate Secret Key**
```bash
python generate_secret_key.py
```

### **Step 2: Get Twilio Credentials**
1. Sign up at https://www.twilio.com/
2. Get credentials from https://console.twilio.com/
3. Join WhatsApp sandbox

### **Step 3: Update .env File**
Replace the placeholder values with your actual credentials.

### **Step 4: Test Configuration**
```bash
python -m app.main
```

## 🔒 Security Best Practices

### **Never Do This:**
- ❌ Commit `.env` file to Git
- ❌ Share your secret key publicly
- ❌ Use the same key for development and production
- ❌ Use weak passwords

### **Always Do This:**
- ✅ Keep `.env` file in `.gitignore`
- ✅ Use strong, unique secret keys
- ✅ Use different keys for different environments
- ✅ Regularly rotate your Twilio Auth Token

## 📁 File Structure

Your project should look like this:
```
whatsapp_agent_system/
├── .env                          # Your environment variables (keep secret)
├── .gitignore                    # Should include .env
├── app/
├── requirements.txt
├── setup_database.py
├── generate_secret_key.py        # Generate secret keys
├── TWILIO_SETUP_GUIDE.md         # Twilio setup instructions
├── API_DOCUMENTATION.md          # API documentation
└── ENVIRONMENT_SETUP.md          # This file
```

## 🛠️ Troubleshooting

### **Common Issues:**

1. **"Twilio credentials not configured"**
   - Check that all three Twilio variables are set
   - Ensure no extra spaces in values

2. **"MongoDB connection failed"**
   - Verify MongoDB is running
   - Check MONGODB_URI format

3. **"Secret key not found"**
   - Ensure SECRET_KEY is set in .env
   - Check for typos

4. **"Port already in use"**
   - Change PORT in .env file
   - Kill existing processes on port 5000

## 📋 Checklist

- [ ] Generated secret key using `python generate_secret_key.py`
- [ ] Created Twilio account and got credentials
- [ ] Joined WhatsApp Business API sandbox
- [ ] Updated `.env` file with all values
- [ ] Tested the application with `python -m app.main`
- [ ] Added `.env` to `.gitignore`

## 🎯 Next Steps

1. **Complete the setup** using this guide
2. **Test the API** with sample requests
3. **Configure Twilio webhooks** for production
4. **Deploy to your server**
5. **Set up monitoring and logging**

Your WhatsApp Agent Dispatch System will be fully configured once you complete these steps!

