#!/usr/bin/env python3
"""
Quick Setup for Real Data
Helps you configure the tool with your API key
"""

import os
import sys

def main():
    print("=" * 60)
    print("QUICK SETUP FOR REAL DATA")
    print("=" * 60)
    print()
    print("This will help you set up real website data")
    print("Total cost: $0/month using FREE APIs")
    print()
    
    print("Available FREE APIs:")
    print("1. BuiltWith API (500 free requests/month) - EASIEST")
    print("2. Wappalyzer API (1,000 free requests/month)")
    print("3. Google PageSpeed API (25,000 free requests/day)")
    print()
    
    print("To get your API key:")
    print("1. Visit one of the URLs above")
    print("2. Sign up for free account")
    print("3. Get your API key from dashboard")
    print("4. Come back here and enter it")
    print()
    
    # Check if config.py exists
    if not os.path.exists("config.py"):
        print("Error: config.py not found!")
        return
    
    # Read current config
    with open("config.py", 'r') as f:
        config_content = f.read()
    
    # Check current status
    has_builtwith = 'BUILTWITH_API_KEY = "' in config_content and 'YOUR_BUILTWITH_API_KEY_HERE' not in config_content
    has_wappalyzer = 'WAPPALYZER_API_KEY = "' in config_content and 'YOUR_WAPPALYZER_API_KEY_HERE' not in config_content
    has_pagespeed = 'PAGESPEED_API_KEY = "' in config_content and 'YOUR_PAGESPEED_API_KEY_HERE' not in config_content
    
    print("Current API Status:")
    print(f"- BuiltWith: {'Configured' if has_builtwith else 'Not configured'}")
    print(f"- Wappalyzer: {'Configured' if has_wappalyzer else 'Not configured'}")
    print(f"- PageSpeed: {'Configured' if has_pagespeed else 'Not configured'}")
    print()
    
    if has_builtwith or has_wappalyzer or has_pagespeed:
        print("SUCCESS: You have API keys configured!")
        print("Your tool is ready to use real data.")
        print()
        print("Next steps:")
        print("1. Run: .\\test_api.bat")
        print("2. Run: .\\run_gui.bat")
        print("3. Analyze your websites to see real data!")
    else:
        print("No API keys configured yet.")
        print()
        print("To get started:")
        print("1. Choose an API from the list above")
        print("2. Sign up for free account")
        print("3. Get your API key")
        print("4. Run: .\\add_api_key.bat")
        print()
        print("Recommended: Start with BuiltWith API (easiest)")
        print("Visit: https://api.builtwith.com/")
    
    print()
    print("=" * 60)
    print("SECURITY REMINDER")
    print("=" * 60)
    print()
    print("IMPORTANT: Never share your API keys!")
    print("- Keep them private and secure")
    print("- Store them only in config.py")
    print("- You can regenerate them anytime")
    print("- Free APIs have usage limits")
    print()
    print("The tool is designed to work safely with your keys")

if __name__ == "__main__":
    main()












































