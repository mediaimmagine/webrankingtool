#!/usr/bin/env python3
"""
Simple API Key Adder
Helps you add your BuiltWith API key to config.py
"""

import os
import sys

def main():
    print("=" * 60)
    print("ADD API KEY TO CONFIG")
    print("=" * 60)
    print()
    print("This will help you add your BuiltWith API key to config.py")
    print()
    
    # Check if config.py exists
    if not os.path.exists("config.py"):
        print("Error: config.py not found!")
        return
    
    # Read current config
    with open("config.py", 'r') as f:
        config_content = f.read()
    
    # Check if key is already configured
    if 'BUILTWITH_API_KEY = "' in config_content and 'YOUR_BUILTWITH_API_KEY_HERE' not in config_content:
        print("BuiltWith API key is already configured!")
        print()
        # Extract current key (show first 10 characters)
        lines = config_content.split('\n')
        for line in lines:
            if 'BUILTWITH_API_KEY = "' in line:
                key = line.split('"')[1]
                print(f"Current key: {key[:10]}...")
                break
        
        replace = input("Do you want to replace it? (y/n): ").strip().lower()
        if replace != 'y':
            print("Keeping current API key.")
            return
    
    print("To get your BuiltWith API key:")
    print("1. Visit: https://api.builtwith.com/")
    print("2. Sign up for free account")
    print("3. Get your API key from dashboard")
    print()
    
    api_key = input("Enter your BuiltWith API key: ").strip()
    
    if not api_key:
        print("No API key entered. Exiting.")
        return
    
    # Update config file
    old_line = 'BUILTWITH_API_KEY = None  # Get free API key from https://api.builtwith.com/'
    new_line = f'BUILTWITH_API_KEY = "{api_key}"  # BuiltWith API key'
    
    if old_line in config_content:
        config_content = config_content.replace(old_line, new_line)
        print("✅ API key added to config.py!")
    else:
        # Try alternative format
        old_line = 'BUILTWITH_API_KEY = "YOUR_BUILTWITH_API_KEY_HERE"'
        new_line = f'BUILTWITH_API_KEY = "{api_key}"'
        if old_line in config_content:
            config_content = config_content.replace(old_line, new_line)
            print("✅ API key added to config.py!")
        else:
            print("❌ Could not find BUILTWITH_API_KEY line in config.py")
            print("Please manually edit config.py and add:")
            print(f'BUILTWITH_API_KEY = "{api_key}"')
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
        print("Testing BuiltWith API...")
        try:
            import requests
            
            params = {
                'KEY': api_key,
                'LOOKUP': 'google.com',
                'HIDETEXT': 'true',
                'HIDEDL': 'true'
            }
            
            response = requests.get("https://api.builtwith.com/v20/api.json", params=params, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ BuiltWith API is working! You now have real data.")
            else:
                print(f"❌ API Error: {response.status_code}")
                print("Check your API key and try again.")
        except Exception as e:
            print(f"Error testing API: {e}")

if __name__ == "__main__":
    main()




