#!/usr/bin/env python3
"""
Google Analytics API Setup and Authentication
Sets up credentials for accessing GA4 data via API
"""

import json
import os
from pathlib import Path

class GoogleAnalyticsSetup:
    """Setup Google Analytics API credentials"""
    
    def __init__(self):
        self.credentials_file = "google_analytics_credentials.json"
        self.config_file = "google_analytics_config.json"
    
    def setup_interactive(self):
        """Interactive setup for Google Analytics API"""
        print("\n" + "="*80)
        print("GOOGLE ANALYTICS API SETUP")
        print("="*80)
        
        print("\nThis will configure access to Google Analytics data via API.")
        print("You'll need to create a Service Account in Google Cloud Platform.")
        
        print("\n" + "="*80)
        print("STEP-BY-STEP GUIDE")
        print("="*80)
        
        print("\n1. CREATE SERVICE ACCOUNT:")
        print("   - Go to: https://console.cloud.google.com")
        print("   - Create new project or select existing")
        print("   - Enable 'Google Analytics Data API'")
        print("   - Create Service Account")
        print("   - Download JSON key file")
        
        print("\n2. GRANT ANALYTICS ACCESS:")
        print("   - Go to: https://analytics.google.com")
        print("   - Admin → Property Access Management")
        print("   - Add service account email as Viewer")
        
        print("\n3. GET PROPERTY ID:")
        print("   - In Google Analytics")
        print("   - Admin → Property Settings")
        print("   - Copy Property ID (format: 123456789)")
        
        print("\n" + "="*80)
        
        # Get Property ID
        property_id = input("\nEnter your GA4 Property ID: ").strip()
        
        if not property_id:
            print("[ERROR] Property ID is required")
            return
        
        # Get credentials file path
        print("\nEnter path to Service Account JSON key file:")
        print("(or press Enter to use default: google_analytics_credentials.json)")
        creds_path = input("Path: ").strip()
        
        if not creds_path:
            creds_path = self.credentials_file
        
        # Verify credentials file exists
        if not Path(creds_path).exists():
            print(f"\n[ERROR] Credentials file not found: {creds_path}")
            print("\n[HELP] Steps to get this file:")
            print("  1. Go to: https://console.cloud.google.com")
            print("  2. Select your project")
            print("  3. IAM & Admin → Service Accounts")
            print("  4. Click your service account")
            print("  5. Keys → Add Key → Create new key")
            print("  6. Choose JSON")
            print("  7. Download and save as: google_analytics_credentials.json")
            return
        
        # Copy credentials to standard location
        if creds_path != self.credentials_file:
            import shutil
            shutil.copy(creds_path, self.credentials_file)
            print(f"[OK] Credentials copied to: {self.credentials_file}")
        
        # Save configuration
        config = {
            'property_id': property_id,
            'credentials_file': self.credentials_file,
            'created_at': datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n[OK] Configuration saved to: {self.config_file}")
        print("\n" + "="*80)
        print("SETUP COMPLETE!")
        print("="*80)
        print("\nYou can now use the Google Analytics API to fetch real traffic data.")
        print("\nNext: Run 'python test_google_analytics_api.py' to test")
    
    def quick_setup_guide(self):
        """Print quick setup guide"""
        guide = """
================================================================================
GOOGLE ANALYTICS API - QUICK SETUP GUIDE
================================================================================

OVERVIEW:
To access GA4 data programmatically, you need:
1. Google Cloud Project with Analytics Data API enabled
2. Service Account with JSON credentials
3. Service Account added to GA4 property as Viewer
4. GA4 Property ID

================================================================================
DETAILED STEPS:
================================================================================

STEP 1: Create Google Cloud Project
────────────────────────────────────
1. Go to: https://console.cloud.google.com
2. Click: "Select a project" → "New Project"
3. Name: "Trieste News Analytics"
4. Click: "Create"

STEP 2: Enable Google Analytics Data API
──────────────────────────────────────────
1. In your project, click: "APIs & Services" → "Library"
2. Search: "Google Analytics Data API"
3. Click on it
4. Click: "Enable"
5. Wait for enablement (takes a few seconds)

STEP 3: Create Service Account
────────────────────────────────
1. Go to: "IAM & Admin" → "Service Accounts"
2. Click: "+ Create Service Account"
3. Name: "analytics-reader"
4. Description: "Read Google Analytics data"
5. Click: "Create and Continue"
6. Role: Skip (click "Continue")
7. Click: "Done"

STEP 4: Create JSON Key
─────────────────────────
1. Click on the service account you just created
2. Go to: "Keys" tab
3. Click: "Add Key" → "Create new key"
4. Choose: JSON
5. Click: "Create"
6. File downloads automatically (google_analytics_credentials.json)
7. Save this file in: C:\\Users\\front\\Documents\\WebRankingTool\\

STEP 5: Get Service Account Email
───────────────────────────────────
1. In the service account details, copy the email
2. Format: analytics-reader@project-name.iam.gserviceaccount.com
3. Keep this email - you'll need it next

STEP 6: Grant Analytics Access to Service Account
────────────────────────────────────────────────────
1. Go to: https://analytics.google.com
2. Click: Admin (gear icon)
3. Select: Your property (triesteallnews.it)
4. Click: "Property Access Management"
5. Click: "+" (Add users)
6. Email: Paste the service account email from Step 5
7. Role: "Viewer" (sufficient for reading data)
8. Uncheck: "Notify new users by email"
9. Click: "Add"

STEP 7: Get Property ID
─────────────────────────
1. Still in Analytics Admin
2. Click: "Property Settings"
3. Copy the Property ID (format: 123456789)
4. Keep this number

STEP 8: Run Setup Script
──────────────────────────
1. Open terminal/command prompt
2. Navigate to: C:\\Users\\front\\Documents\\WebRankingTool
3. Run: python google_analytics_setup.py
4. Enter Property ID when prompted
5. Enter path to JSON credentials file

================================================================================
VERIFICATION:
================================================================================

After setup, test with:
    python test_google_analytics_api.py

This will verify:
✅ Credentials are valid
✅ Service account has access
✅ Can fetch analytics data
✅ Real traffic data is available

================================================================================
SECURITY NOTES:
================================================================================

⚠️  The JSON credentials file contains sensitive data!
✅ Keep it secure (already in .gitignore)
✅ Never commit to git
✅ Only service account email is shared with GA
✅ Service account can only READ data (no write access)

================================================================================
TROUBLESHOOTING:
================================================================================

"Permission denied":
→ Make sure service account email is added to GA property

"Property not found":
→ Check Property ID is correct (numbers only)

"API not enabled":
→ Enable Google Analytics Data API in Cloud Console

================================================================================
"""
        print(guide)


def datetime_import():
    from datetime import datetime
    return datetime

datetime = datetime_import()


def main():
    """Main setup"""
    setup = GoogleAnalyticsSetup()
    
    print("\n1. Show Quick Setup Guide")
    print("2. Run Interactive Setup (after completing guide)")
    print("3. Exit")
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        setup.quick_setup_guide()
    elif choice == "2":
        setup.setup_interactive()
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()

