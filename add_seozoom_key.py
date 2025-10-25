#!/usr/bin/env python3
"""
Script to add SEOZoom API key to config.py
"""

import os
import sys

def add_seozoom_key():
    """Add SEOZoom API key to config.py"""
    print("=" * 60)
    print("SEOZoom API Key Setup")
    print("=" * 60)
    print()
    print("To get your SEOZoom API key:")
    print("1. Log in to your SEOZoom account")
    print("2. Go to your dashboard")
    print("3. Navigate to API settings")
    print("4. Copy your API key")
    print()
    
    # Get API key from user
    api_key = input("Enter your SEOZoom API key: ").strip()
    
    if not api_key:
        print("No API key provided. Exiting.")
        return
    
    # Read current config
    config_path = "config.py"
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found!")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the SEOZoom API key
    old_line = "SEOZOOM_API_KEY = None  # Get from your SEOZoom dashboard"
    new_line = f'SEOZOOM_API_KEY = "{api_key}"  # SEOZoom API key'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Write updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print()
        print("✅ SEOZoom API key added successfully!")
        print()
        print("Your tool will now use real SEOZoom data for:")
        print("- Real website traffic statistics")
        print("- Actual visitor counts")
        print("- Real bounce rates and engagement metrics")
        print("- Accurate geographic data")
        print("- True traffic source analysis")
        print()
        print("You can now run your tool with real data!")
        
    else:
        print("Error: Could not find the SEOZoom API key line in config.py")
        print("Please check the file manually.")

if __name__ == "__main__":
    add_seozoom_key()
    input("\nPress Enter to exit...")






















































