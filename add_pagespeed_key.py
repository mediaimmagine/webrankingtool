#!/usr/bin/env python3
"""
Add PageSpeed API Key Helper
Helps you add your Google PageSpeed API key to config.py
"""

import os
import sys

def main():
    print("=" * 60)
    print("ADD PAGESPEED API KEY")
    print("=" * 60)
    print()
    print("This will help you add your Google PageSpeed API key")
    print()
    
    # Check if config.py exists
    if not os.path.exists("config.py"):
        print("Error: config.py not found!")
        return
    
    # Read current config
    with open("config.py", 'r') as f:
        config_content = f.read()
    
    # Check if key is already configured
    if 'PAGESPEED_API_KEY = "' in config_content and 'YOUR_PAGESPEED_API_KEY_HERE' not in config_content:
        print("PageSpeed API key is already configured!")
        print()
        # Extract current key (show first 10 characters)
        lines = config_content.split('\n')
        for line in lines:
            if 'PAGESPEED_API_KEY = "' in line:
                key = line.split('"')[1]
                print(f"Current key: {key[:10]}...")
                break
        
        replace = input("Do you want to replace it? (y/n): ").strip().lower()
        if replace != 'y':
            print("Keeping current API key.")
            return
    
    print("To get your Google PageSpeed API key:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a project (free)")
    print("3. Enable PageSpeed Insights API")
    print("4. Create an API key")
    print("5. Copy the key (starts with AIzaSyC...)")
    print()
    
    api_key = input("Enter your PageSpeed API key: ").strip()
    
    if not api_key:
        print("No API key entered. Exiting.")
        return
    
    # Validate API key format
    if not api_key.startswith('AIzaSy'):
        print("Warning: Google API keys usually start with 'AIzaSy'")
        print("Are you sure this is correct? (y/n): ", end="")
        confirm = input().strip().lower()
        if confirm != 'y':
            print("Please check your API key and try again.")
            return
    
    # Update config file
    old_line = 'PAGESPEED_API_KEY = None  # Get free API key from https://developers.google.com/speed/docs/insights/v5/get-started'
    new_line = f'PAGESPEED_API_KEY = "{api_key}"  # Google PageSpeed API key'
    
    if old_line in config_content:
        config_content = config_content.replace(old_line, new_line)
        print("✅ PageSpeed API key added to config.py!")
    else:
        # Try alternative format
        old_line = 'PAGESPEED_API_KEY = "YOUR_PAGESPEED_API_KEY_HERE"'
        new_line = f'PAGESPEED_API_KEY = "{api_key}"'
        if old_line in config_content:
            config_content = config_content.replace(old_line, new_line)
            print("✅ PageSpeed API key added to config.py!")
        else:
            print("❌ Could not find PAGESPEED_API_KEY line in config.py")
            print("Please manually edit config.py and add:")
            print(f'PAGESPEED_API_KEY = "{api_key}"')
            return
    
    # Write updated config
    with open("config.py", 'w') as f:
        f.write(config_content)
    
    print()
    print("Next steps:")
    print("1. Run: .\\test_api.bat")
    print("2. Run: .\\run_gui.bat")
    print("3. Analyze websites to see REAL DATA!")
    print()
    
    # Test the API
    test_now = input("Test the API now? (y/n): ").strip().lower()
    if test_now == 'y':
        print()
        print("Testing PageSpeed API...")
        try:
            import requests
            
            params = {
                'url': 'https://google.com',
                'key': api_key,
                'strategy': 'mobile'
            }
            
            response = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed", 
                                  params=params, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ PageSpeed API is working! You now have real data.")
                print("Your tool will now use real website performance data!")
            else:
                print(f"❌ API Error: {response.status_code}")
                print("Check your API key and try again.")
        except Exception as e:
            print(f"Error testing API: {e}")

if __name__ == "__main__":
    main()












































