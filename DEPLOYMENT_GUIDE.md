# Deployment Guide for WhatsApp Agent System

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/whatsapp_agent_system.git
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to https://railway.app/
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect it's a Python app

3. **Set Environment Variables**
   - Go to your project settings
   - Add these environment variables:
     ```
     TWILIO_ACCOUNT_SID=your_twilio_sid
     TWILIO_AUTH_TOKEN=your_twilio_token
     TWILIO_WHATSAPP_NUMBER=+14155238886
     MONGODB_URI=your_mongodb_uri
     MONGODB_DB_NAME=whatsapp_agent_system
     SECRET_KEY=your_secret_key
     ```

4. **Get your live URL**
   - Railway will give you a URL like: `https://your-app-name.railway.app`

### Option 2: Render (Free tier)

1. **Sign up at Render**: https://render.com/
2. **Create New Web Service**
3. **Connect your GitHub repository**
4. **Configure**:
   - **Name**: `whatsapp-agent-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Set Environment Variables** (same as Railway)
6. **Deploy**

### Option 3: PythonAnywhere (Free tier)

1. **Sign up**: https://www.pythonanywhere.com/
2. **Upload your code** (or clone from GitHub)
3. **Create a new web app**:
   - Choose "Manual configuration"
   - Python version: 3.11
4. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure WSGI file**:
   ```python
   import sys
   path = '/home/yourusername/whatsapp_agent_system'
   if path not in sys.path:
       sys.path.append(path)
   
   from app.main import app
   application = app
   ```
6. **Set environment variables** in the web app configuration

## MongoDB Setup

### Option A: MongoDB Atlas (Free tier)
1. **Sign up**: https://www.mongodb.com/atlas
2. **Create a free cluster**
3. **Get connection string**:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/whatsapp_agent_system
   ```

### Option B: Use local MongoDB (not recommended for production)
- Keep using your local MongoDB for testing

## Update Twilio Webhook URLs

Once deployed, update your Twilio webhook URLs:

1. **Go to Twilio Console** → **Messaging** → **Try it out** → **Send a WhatsApp message**
2. **Update Inbound URL**:
   ```
   https://your-app-name.railway.app/api/webhooks/twilio/whatsapp
   ```
3. **Update Status Callback URL**:
   ```
   https://your-app-name.railway.app/api/webhooks/twilio/status-callback
   ```

## Testing Your Live Deployment

1. **Test the health endpoint**:
   ```
   https://your-app-name.railway.app/health
   ```

2. **Create an inspection request**:
   ```bash
   curl -X POST https://your-app-name.railway.app/api/jobs/ \
     -H "Content-Type: application/json" \
     -d '{
       "property": {
         "property_id": "test_live_001",
         "title": "Live Test Property",
         "address": "123 Live Test Street",
         "property_type": "Apartment",
         "bedrooms": 2,
         "bathrooms": 1,
         "price": 50000000
       },
       "client": {
         "client_id": "test_client_live_001",
         "name": "Live Test Client",
         "phone": "+2348012345678",
         "email": "livetest@example.com"
       },
       "inspection_date": "2024-01-30",
       "inspection_time": "14:00"
     }'
   ```

3. **Test WhatsApp integration**:
   - Reply "YES" to the inspection request
   - Reply "CONFIRM" to confirm schedule
   - Wait for reminders and prompts

## Troubleshooting

### Common Issues:

1. **Environment variables not set**
   - Check your deployment platform's environment variable settings

2. **MongoDB connection issues**
   - Ensure your MongoDB URI is correct
   - Check if your IP is whitelisted (for Atlas)

3. **Twilio webhook not working**
   - Verify the webhook URLs are correct
   - Check if your app is accessible from the internet

4. **App not starting**
   - Check the logs in your deployment platform
   - Ensure all dependencies are in `requirements.txt`

## Security Notes

- Never commit sensitive data (API keys, tokens) to your repository
- Use environment variables for all sensitive configuration
- Consider using a `.env` file for local development (but don't commit it)

## Next Steps

1. **Deploy to your chosen platform**
2. **Set up environment variables**
3. **Update Twilio webhook URLs**
4. **Test the complete flow**
5. **Monitor logs for any issues**

Your WhatsApp agent system will then be live and accessible from anywhere!
