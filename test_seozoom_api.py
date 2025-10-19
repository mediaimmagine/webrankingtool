#!/usr/bin/env python3
"""
Test script to diagnose SEOZoom API endpoints
"""

import requests
import json

def test_seozoom_api():
    """Test different SEOZoom API endpoints and authentication methods"""
    
    api_key = "AK-c8713689b856896216114ac25e2bb7a4"
    domain = "triesteallnews.it"
    
    print("=" * 60)
    print("SEOZoom API Endpoint Testing")
    print("=" * 60)
    print(f"API Key: {api_key}")
    print(f"Domain: {domain}")
    print()
    
    # Different base URLs to try
    base_urls = [
        "https://api.seozoom.it/v1",
        "https://api.seozoom.it/v2", 
        "https://api.seozoom.it",
        "https://seozoom.it/api/v1",
        "https://seozoom.it/api",
        "https://www.seozoom.it/api/v1",
        "https://www.seozoom.it/api"
    ]
    
    # Different endpoint patterns
    endpoints = [
        f"/website/{domain}",
        f"/sites/{domain}",
        f"/domain/{domain}",
        f"/website/{domain}/stats",
        f"/website/{domain}/traffic",
        f"/website/{domain}/overview",
        f"/website/{domain}/analytics",
        f"/website/{domain}/data",
        f"/sites/{domain}/stats",
        f"/sites/{domain}/traffic",
        f"/domain/{domain}/stats",
        f"/domain/{domain}/traffic",
        "/website",
        "/sites",
        "/domain",
        "/stats",
        "/traffic"
    ]
    
    # Different authentication methods
    auth_methods = [
        {"Authorization": f"Bearer {api_key}"},
        {"X-API-Key": api_key},
        {"api_key": api_key},
        {"key": api_key},
        {"Authorization": f"Token {api_key}"},
        {"Authorization": f"API-Key {api_key}"},
        {"Authorization": api_key},
        {"X-Auth-Token": api_key},
        {"X-Api-Key": api_key}
    ]
    
    print("Testing different combinations...")
    print()
    
    for base_url in base_urls:
        for endpoint in endpoints:
            for auth_method in auth_methods:
                url = base_url + endpoint
                headers = {
                    'Content-Type': 'application/json',
                    **auth_method
                }
                
                try:
                    print(f"Testing: {url}")
                    print(f"Auth: {list(auth_method.keys())[0]}")
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("SUCCESS! Found working endpoint!")
                        print(f"Response: {response.text[:200]}...")
                        return url, auth_method
                    elif response.status_code == 401:
                        print("Authentication failed")
                    elif response.status_code == 403:
                        print("Forbidden - API key might be invalid")
                    elif response.status_code == 404:
                        print("Not found")
                    else:
                        print(f"Error: {response.status_code}")
                    
                    print()
                    
                except Exception as e:
                    print(f"Exception: {e}")
                    print()
    
    print("No working endpoints found. This might mean:")
    print("1. The API endpoints are different")
    print("2. The API key is invalid or expired")
    print("3. The API requires different authentication")
    print("4. The API might be down or changed")
    print()
    print("Please check your SEOZoom dashboard for the correct API documentation.")

if __name__ == "__main__":
    test_seozoom_api()
    input("\nPress Enter to exit...")
