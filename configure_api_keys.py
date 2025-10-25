#!/usr/bin/env python3
"""
API Key Configuration Helper
Helps you add API keys to config.py
"""

import os
import sys

def main():
    print("=" * 60)
    print("API KEY CONFIGURATION HELPER")
    print("=" * 60)
    print()
    print("This will help you add API keys to config.py")
    print()
    
    # Read current config
    config_path = "config.py"
    if not os.path.exists(config_path):
        print("Error: config.py not found!")
        return
    
    with open(config_path, 'r') as f:
        config_content = f.read()
    
    print("Available free APIs:")
    print("1. BuiltWith API (500 free requests/month)")
    print("2. Wappalyzer API (1,000 free requests/month)")
    print("3. Google PageSpeed API (25,000 free requests/day)")
    print()
    
    choice = input("Which API do you want to configure? (1/2/3): ").strip()
    
    if choice == "1":
        api_name = "BuiltWith"
        api_key_var = "BUILTWITH_API_KEY"
        api_url = "https://api.builtwith.com/"
    elif choice == "2":
        api_name = "Wappalyzer"
        api_key_var = "WAPPALYZER_API_KEY"
        api_url = "https://www.wappalyzer.com/api/"
    elif choice == "3":
        api_name = "PageSpeed"
        api_key_var = "PAGESPEED_API_KEY"
        api_url = "https://console.cloud.google.com/"
    else:
        print("Invalid choice!")
        return
    
    print()
    print(f"To get your {api_name} API key:")
    print(f"1. Visit: {api_url}")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print()
    
    api_key = input(f"Enter your {api_name} API key: ").strip()
    
    if not api_key:
        print("No API key entered. Exiting.")
        return
    
    # Update config file
    old_line = f'{api_key_var} = None  # Get free API key from {api_url}'
    new_line = f'{api_key_var} = "{api_key}"  # {api_name} API key'
    
    if old_line in config_content:
        config_content = config_content.replace(old_line, new_line)
    else:
        # Try alternative format
        old_line = f'{api_key_var} = "YOUR_{api_key_var}_HERE"'
        new_line = f'{api_key_var} = "{api_key}"'
        config_content = config_content.replace(old_line, new_line)
    
    # Write updated config
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print()
    print(f"✅ {api_name} API key configured!")
    print()
    print("Next steps:")
    print("1. Run: .\\test_api.bat")
    print("2. Run: .\\run_gui.bat")
    print("3. Analyze websites to see real data!")
    print()
    
    # Test the API
    test_now = input("Test the API now? (y/n): ").strip().lower()
    if test_now == 'y':
        print()
        print("Testing API...")
        try:
            from test_api import test_builtwith_api, test_wappalyzer_api, test_pagespeed_api
            
            if choice == "1":
                result = test_builtwith_api()
            elif choice == "2":
                result = test_wappalyzer_api()
            elif choice == "3":
                result = test_pagespeed_api()
            
            if result:
                print("✅ API test successful! You're ready to use real data.")
            else:
                print("❌ API test failed. Check your API key.")
        except Exception as e:
            print(f"Error testing API: {e}")

if __name__ == "__main__":
    main()












































