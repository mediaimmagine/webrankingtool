#!/usr/bin/env python3
"""
Demo with API Key
Shows how the tool works with a real API key
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("DEMO: TOOL WITH API KEY")
    print("=" * 60)
    print()
    print("This shows how the tool works when you add an API key")
    print()
    
    # Check current config
    try:
        from config import BUILTWITH_API_KEY, USE_MOCK_DATA
        
        print("Current Configuration:")
        print(f"- Mock Data Mode: {USE_MOCK_DATA}")
        print(f"- BuiltWith API Key: {'Configured' if BUILTWITH_API_KEY and BUILTWITH_API_KEY != 'YOUR_BUILTWITH_API_KEY_HERE' else 'Not configured'}")
        print()
        
        if BUILTWITH_API_KEY and BUILTWITH_API_KEY != 'YOUR_BUILTWITH_API_KEY_HERE':
            print("SUCCESS: You have an API key configured!")
            print("The tool will use real data from BuiltWith API.")
        else:
            print("No API key configured yet.")
            print()
            print("To add your API key:")
            print("1. Get free API key from: https://api.builtwith.com/")
            print("2. Edit config.py")
            print("3. Change: BUILTWITH_API_KEY = None")
            print("4. To: BUILTWITH_API_KEY = 'your_key_here'")
            print("5. Save the file")
            print("6. Run: .\\test_api.bat")
        
        print()
        print("=" * 60)
        print("WHAT HAPPENS WITH API KEY:")
        print("=" * 60)
        print()
        print("WITHOUT API KEY (Current):")
        print("- Uses improved mock data")
        print("- Shows 'REAL DATA' but it's simulated")
        print("- Same values every time")
        print("- Good for testing")
        print()
        print("WITH API KEY (After you add one):")
        print("- Uses actual BuiltWith API")
        print("- Gets real website technology data")
        print("- Live data from their servers")
        print("- Professional-grade insights")
        print()
        print("=" * 60)
        print("YOUR SITES WITH REAL DATA:")
        print("=" * 60)
        print()
        print("When you add an API key, you'll get:")
        print("- Real technology stack for each site")
        print("- Actual hosting information")
        print("- Live analytics data")
        print("- Professional website analysis")
        print()
        print("Sites to analyze:")
        print("- triesteallnews.it")
        print("- triesteprima.it") 
        print("- triestecafe.it")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

