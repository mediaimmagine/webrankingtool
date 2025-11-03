#!/usr/bin/env python3
"""
Secure WordPress API Credentials Manager
Stores credentials encrypted or in a secure config file
"""

import json
import os
from pathlib import Path
import getpass

class WordPressCredentialsManager:
    """Manage WordPress API credentials securely"""
    
    def __init__(self, config_file: str = "wordpress_api_config.json"):
        self.config_file = config_file
        self.config_path = Path(config_file)
    
    def save_credentials(self, base_url: str, username: str, app_password: str):
        """Save credentials to config file"""
        config = {
            'base_url': base_url,
            'username': username,
            'app_password': app_password,
            'created_at': import_datetime().now().isoformat()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set file permissions (read/write for owner only on Unix systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(self.config_file, 0o600)
        
        print(f"[OK] Credentials saved to {self.config_file}")
        print(f"[SECURITY] Keep this file secure and don't commit it to git!")
    
    def load_credentials(self) -> dict:
        """Load credentials from config file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        return config
    
    def has_credentials(self) -> bool:
        """Check if credentials are saved"""
        return self.config_path.exists()
    
    def remove_credentials(self):
        """Remove saved credentials"""
        if self.config_path.exists():
            self.config_path.unlink()
            print(f"[OK] Credentials removed from {self.config_file}")
    
    def setup_interactive(self):
        """Interactive setup"""
        print("\n" + "="*80)
        print("WORDPRESS API CREDENTIALS SETUP")
        print("="*80)
        
        if self.has_credentials():
            print(f"\n[INFO] Credentials file already exists: {self.config_file}")
            overwrite = input("Overwrite existing credentials? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("[INFO] Keeping existing credentials")
                return
        
        base_url = input("\nWebsite URL (default: https://www.triesteallnews.it): ").strip()
        if not base_url:
            base_url = "https://www.triesteallnews.it"
        
        username = input("WordPress Username: ").strip()
        if not username:
            print("[ERROR] Username is required")
            return
        
        print("\nApplication Password:")
        print("How to create:")
        print("  1. Log in to WordPress admin")
        print("  2. Go to Users → Your Profile")
        print("  3. Scroll down to 'Application Passwords'")
        print("  4. Enter a name (e.g., 'Article Analytics')")
        print("  5. Click 'Add New Application Password'")
        print("  6. Copy the generated password")
        
        app_password = getpass.getpass("\nApplication Password: ").strip()
        
        if not app_password:
            print("[ERROR] Application Password is required")
            return
        
        # Remove spaces from app password (WordPress format allows spaces for readability)
        app_password = app_password.replace(' ', '')
        
        # Save credentials
        self.save_credentials(base_url, username, app_password)
        
        print("\n[OK] Setup complete!")
        print(f"\n[NEXT] Run: python wordpress_api_tester.py")


def import_datetime():
    """Import datetime module"""
    from datetime import datetime
    return datetime


def main():
    """Setup credentials"""
    manager = WordPressCredentialsManager()
    manager.setup_interactive()


if __name__ == "__main__":
    main()

