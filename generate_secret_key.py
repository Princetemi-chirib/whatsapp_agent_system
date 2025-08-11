#!/usr/bin/env python3
"""
Generate a secure secret key for the WhatsApp Agent Dispatch System
"""

import secrets
import string

def generate_secret_key(length=32):
    """Generate a secure random secret key."""
    # Use URL-safe base64 encoding
    return secrets.token_urlsafe(length)

def generate_simple_secret_key(length=32):
    """Generate a simple alphanumeric secret key."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    print("🔐 Generating Secret Keys for WhatsApp Agent Dispatch System")
    print("=" * 60)
    
    # Generate URL-safe secret key
    url_safe_key = generate_secret_key(32)
    print(f"URL-Safe Secret Key (Recommended):")
    print(f"SECRET_KEY={url_safe_key}")
    print()
    
    # Generate simple alphanumeric key
    simple_key = generate_simple_secret_key(32)
    print(f"Simple Alphanumeric Secret Key:")
    print(f"SECRET_KEY={simple_key}")
    print()
    
    print("📝 Instructions:")
    print("1. Copy one of the keys above")
    print("2. Replace 'your_secret_key_here_change_in_production' in your .env file")
    print("3. Keep this key secret and don't share it")
    print("4. Use different keys for development and production")
    print()
    print("⚠️  Security Notes:")
    print("- Never commit your .env file to version control")
    print("- Use a different key for production")
    print("- Keep your secret key secure")

