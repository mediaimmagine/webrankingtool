#!/usr/bin/env python3
"""
Google PageSpeed API Setup Helper
Guides you through setting up Google PageSpeed API
"""

import os
import sys

def main():
    print("=" * 60)
    print("GOOGLE PAGESPEED API SETUP")
    print("=" * 60)
    print()
    print("This will help you set up Google PageSpeed API")
    print("Cost: COMPLETELY FREE")
    print("Limit: 25,000 requests per day")
    print("No credit card required!")
    print()
    
    print("STEP 1: Create Google Cloud Project")
    print("-" * 40)
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Click 'Create Project' (free)")
    print("3. Enter project name: 'WebRankingTool'")
    print("4. Click 'Create'")
    print()
    
    print("STEP 2: Enable PageSpeed Insights API")
    print("-" * 40)
    print("1. In your project, go to 'APIs & Services' > 'Library'")
    print("2. Search for 'PageSpeed Insights API'")
    print("3. Click on it")
    print("4. Click 'Enable'")
    print()
    
    print("STEP 3: Create API Key")
    print("-" * 40)
    print("1. Go to 'APIs & Services' > 'Credentials'")
    print("2. Click 'Create Credentials' > 'API Key'")
    print("3. Copy your API key (it will look like: AIzaSyC...)")
    print("4. (Optional) Click 'Restrict Key' for security")
    print()
    
    print("STEP 4: Add API Key to Tool")
    print("-" * 40)
    print("After you get your API key:")
    print("1. Open config.py in text editor")
    print("2. Find: PAGESPEED_API_KEY = None")
    print("3. Change to: PAGESPEED_API_KEY = 'your_key_here'")
    print("4. Save the file")
    print()
    
    print("STEP 5: Test Your Setup")
    print("-" * 40)
    print("1. Run: .\\test_api.bat")
    print("2. You should see 'PageSpeed API is working!'")
    print("3. Run: .\\run_gui.bat")
    print("4. Analyze your sites - you'll see REAL DATA!")
    print()
    
    # Check if config.py exists
    if not os.path.exists("config.py"):
        print("Error: config.py not found!")
        return
    
    # Read current config
    with open("config.py", 'r') as f:
        config_content = f.read()
    
    # Check current status
    has_pagespeed = 'PAGESPEED_API_KEY = "' in config_content and 'YOUR_PAGESPEED_API_KEY_HERE' not in config_content
    
    print("=" * 60)
    print("CURRENT STATUS")
    print("=" * 60)
    print()
    print(f"PageSpeed API Key: {'Configured' if has_pagespeed else 'Not configured'}")
    print()
    
    if has_pagespeed:
        print("SUCCESS: You have PageSpeed API configured!")
        print("Your tool is ready to use real data.")
        print()
        print("Next steps:")
        print("1. Run: .\\test_api.bat")
        print("2. Run: .\\run_gui.bat")
        print("3. Analyze your websites to see real data!")
    else:
        print("No PageSpeed API key configured yet.")
        print()
        print("Follow the steps above to get your API key.")
        print("Then edit config.py to add it.")
    
    print()
    print("=" * 60)
    print("WHAT YOU'LL GET WITH PAGESPEED API")
    print("=" * 60)
    print()
    print("Real website data including:")
    print("- Performance scores (0-100)")
    print("- Core Web Vitals metrics")
    print("- Mobile and desktop analysis")
    print("- Loading times and optimization suggestions")
    print("- Professional website insights")
    print()
    print("Perfect for analyzing:")
    print("- triesteallnews.it")
    print("- triesteprima.it")
    print("- triestecafe.it")
    print()
    print("=" * 60)
    print("TROUBLESHOOTING")
    print("=" * 60)
    print()
    print("If you have trouble:")
    print("1. Make sure you're signed into Google")
    print("2. Check that the API is enabled")
    print("3. Verify your API key is correct")
    print("4. Try the test: .\\test_api.bat")
    print()
    print("Need help? The setup usually takes 5-10 minutes.")

if __name__ == "__main__":
    main()






















































