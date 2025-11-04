#!/usr/bin/env python3
"""
Comprehensive SEOZoom API diagnostics
Find the correct endpoints and authentication method
"""

import requests
import json
from config import SEOZOOM_API_KEY

def test_all_seozoom_endpoints(domain="triesteallnews.it"):
    """Test all possible SEOZoom API v2 endpoints"""
    
    api_key = SEOZOOM_API_KEY
    base_url = "https://apiv2.seozoom.com/api/v2"
    
    print("="*80)
    print("SEOZoom API v2 - Comprehensive Endpoint Testing")
    print("="*80)
    print(f"API Key: {api_key}")
    print(f"Domain: {domain}")
    print(f"Base URL: {base_url}")
    print()
    
    # Different endpoint patterns to try
    endpoints = [
        # Project/domain listing
        "/projects",
        "/projects/list",
        "/domains",
        "/domains/list",
        
        # Domain-specific with domain in path
        f"/keyword-overview/{domain}",
        f"/domain/{domain}",
        f"/domain/{domain}/keywords",
        f"/project/{domain}",
        f"/project/{domain}/keywords",
        
        # URLs endpoint with different actions
        "/urls/",
        
        # Keyword research
        "/keyword-research",
        "/keywords",
        "/keywords/domain",
        
        # Search console style
        "/search-console/keywords",
        f"/search-console/{domain}/keywords",
    ]
    
    # Different auth methods
    auth_methods = [
        ("Query param", {'api_key': api_key}),
        ("Bearer header", {'Authorization': f'Bearer {api_key}'}),
        ("API-Key header", {'X-API-Key': api_key}),
        ("Token header", {'Authorization': f'Token {api_key}'}),
    ]
    
    # URL formats for /urls/ endpoint
    url_formats = [
        f"https://www.{domain}",
        f"https://{domain}",
        domain,
        f"www.{domain}"
    ]
    
    success_count = 0
    
    # Test 1: Simple endpoints (no params)
    print("\n" + "="*80)
    print("TEST 1: Simple Endpoints (GET without params)")
    print("="*80)
    
    for endpoint in endpoints[:6]:  # Project listings
        for auth_name, auth in auth_methods:
            try:
                url = base_url + endpoint
                
                if 'api_key' in auth:
                    # Query param
                    response = requests.get(url, params=auth, timeout=10)
                else:
                    # Header auth
                    response = requests.get(url, headers=auth, timeout=10)
                
                if response.status_code == 200:
                    print(f"[OK] SUCCESS: {endpoint} with {auth_name}")
                    print(f"   Response: {response.text[:200]}...")
                    success_count += 1
                    
                    # Save successful response
                    with open(f'seozoom_success_{auth_name.replace(" ", "_")}.json', 'w') as f:
                        f.write(response.text)
                    
                elif response.status_code == 401:
                    print(f"[AUTH] {endpoint} - Auth failed ({auth_name})")
                elif response.status_code == 404:
                    pass  # Skip 404s to reduce output
                else:
                    print(f"[WARN] {endpoint} - Status {response.status_code} ({auth_name}): {response.text[:50]}")
                    
            except Exception as e:
                pass
    
    # Test 2: /urls/ endpoint with actions
    print("\n" + "="*80)
    print("TEST 2: /urls/ Endpoint with Actions and URL Formats")
    print("="*80)
    
    actions = ['keywords', 'intentgap', 'overview', 'traffic', 'stats']
    
    for action in actions:
        for url_format in url_formats:
            params = {
                'api_key': api_key,
                'action': action,
                'url': url_format,
                'db': 'it',
                'limit': 10
            }
            
            try:
                response = requests.get(f"{base_url}/urls/", params=params, timeout=10)
                
                if response.status_code == 200:
                    print(f"[OK] SUCCESS: action={action}, url={url_format}")
                    print(f"   Response: {response.text[:200]}...")
                    success_count += 1
                    
                    # Save
                    with open(f'seozoom_success_{action}_{url_format.replace("://", "_").replace(".", "_")}.json', 'w') as f:
                        f.write(response.text)
                    
                elif response.status_code != 404 and response.status_code != 400:
                    print(f"[WARN] action={action}, url={url_format} - Status {response.status_code}: {response.text[:80]}")
                    
            except Exception as e:
                pass
    
    # Test 3: Try listing all projects/domains
    print("\n" + "="*80)
    print("TEST 3: List Your Projects/Domains")
    print("="*80)
    
    list_endpoints = [
        "/projects",
        "/project/list",
        "/domains/list",
        "/account/projects",
        "/user/projects"
    ]
    
    for endpoint in list_endpoints:
        for auth_name, auth in auth_methods:
            try:
                url = base_url + endpoint
                
                if 'api_key' in auth:
                    response = requests.get(url, params=auth, timeout=10)
                else:
                    response = requests.get(url, headers=auth, timeout=10)
                
                if response.status_code == 200:
                    print(f"[OK] SUCCESS: {endpoint} with {auth_name}")
                    data = response.json()
                    print(f"   Projects found: {json.dumps(data, indent=2)[:300]}...")
                    success_count += 1
                    
                    with open('seozoom_projects_list.json', 'w') as f:
                        json.dump(data, f, indent=2)
                        
            except Exception as e:
                pass
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    if success_count > 0:
        print(f"\n[OK] Found {success_count} working endpoint(s)!")
        print(f"\nCheck the generated JSON files for successful responses.")
    else:
        print(f"\n[ERROR] No working endpoints found")
        print(f"\nPossible issues:")
        print(f"  1. Domain not added to your SEOZoom project")
        print(f"  2. API key doesn't have access to keyword data")
        print(f"  3. Need to add domain in SEOZoom web interface first")
        print(f"\nRecommendation:")
        print(f"  - Log into seozoom.it")
        print(f"  - Add '{domain}' to your projects")
        print(f"  - Check API key permissions")

if __name__ == "__main__":
    test_all_seozoom_endpoints()

