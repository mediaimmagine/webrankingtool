#!/usr/bin/env python3
"""
Cloudflare API Setup Script for WebRankingTool
Helps configure Cloudflare Browser Rendering API credentials
"""

import os
import sys
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID

def setup_cloudflare_api():
    print("Cloudflare Browser Rendering API Setup")
    print("=" * 50)
    print()
    print("To use the official Cloudflare API for accurate article data:")
    print("1. Go to https://dash.cloudflare.com/profile/api-tokens")
    print("2. Create a new API token with 'Browser Rendering - Edit' permission")
    print("3. Find your Account ID in the Cloudflare dashboard sidebar")
    print()
    
    # Check current configuration
    if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID:
        print("Cloudflare API is already configured!")
        print(f"   Account ID: {CLOUDFLARE_ACCOUNT_ID[:8]}...")
        print(f"   API Token: {CLOUDFLARE_API_TOKEN[:8]}...")
        return True
    
    print("Cloudflare API not configured yet.")
    print()
    
    # Get credentials from user
    account_id = input("Enter your Cloudflare Account ID: ").strip()
    api_token = input("Enter your Cloudflare API Token: ").strip()
    
    if not account_id or not api_token:
        print("Both Account ID and API Token are required.")
        return False
    
    # Update config.py
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the None values
        content = content.replace(
            'CLOUDFLARE_ACCOUNT_ID = None',
            f'CLOUDFLARE_ACCOUNT_ID = "{account_id}"'
        )
        content = content.replace(
            'CLOUDFLARE_API_TOKEN = None',
            f'CLOUDFLARE_API_TOKEN = "{api_token}"'
        )
        
        with open('config.py', 'w') as f:
            f.write(content)
        
        print("Cloudflare API credentials saved to config.py")
        print()
        print("The article analytics will now use the official Cloudflare API")
        print("for more accurate and reliable data fetching.")
        
        return True
        
    except Exception as e:
        print(f"Error updating config.py: {e}")
        return False

def test_cloudflare_api():
    """Test the Cloudflare API connection"""
    print("\nTesting Cloudflare API connection...")
    
    try:
        from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_BROWSER_RENDERING_URL
        import requests
        
        if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ACCOUNT_ID:
            print("Cloudflare API not configured")
            return False
        
        # Test API endpoint
        url = CLOUDFLARE_BROWSER_RENDERING_URL.format(account_id=CLOUDFLARE_ACCOUNT_ID)
        headers = {
            'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple request
        test_data = {
            "url": "https://www.triesteallnews.it/",
            "wait_for": "networkidle"
        }
        
        print(f"Testing API endpoint: {url}")
        response = requests.post(url, json=test_data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("Cloudflare API connection successful!")
            return True
        else:
            print(f"API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing API: {e}")
        return False

if __name__ == "__main__":
    print("Cloudflare API Setup for WebRankingTool")
    print("=" * 50)
    
    # Setup API credentials
    if setup_cloudflare_api():
        # Test the API
        test_cloudflare_api()
    
    print("\nSetup complete!")
    print("You can now run the GUI application to use the official Cloudflare API.")
