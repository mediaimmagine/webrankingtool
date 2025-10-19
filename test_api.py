#!/usr/bin/env python3
"""
Test script to verify API endpoints work correctly
"""

import requests
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (SIMILARWEB_API_KEY, SEMRUSH_API_KEY, BUILTWITH_API_KEY, 
                   WAPPALYZER_API_KEY, PAGESPEED_API_KEY, USE_MOCK_DATA)

def test_similarweb_api():
    """Test SimilarWeb API endpoints"""
    print("Testing SimilarWeb API...")
    
    if not SIMILARWEB_API_KEY or SIMILARWEB_API_KEY == "YOUR_SIMILARWEB_API_KEY_HERE":
        print("SimilarWeb API key not configured")
        return False
    
    headers = {
        'api-key': SIMILARWEB_API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Test with a well-known domain
    test_domain = "google.com"
    
    # Try multiple endpoints to find the correct one
    endpoints_to_try = [
        f"https://api.similarweb.com/v1/website/{test_domain}/total-traffic-and-engagement/visits",
        f"https://api.similarweb.com/v1/website/{test_domain}/traffic-and-engagement/visits",
        f"https://api.similarweb.com/v1/website/{test_domain}/visits",
        f"https://api.similarweb.com/v1/website/{test_domain}/overview",
        f"https://api.similarweb.com/v1/website/{test_domain}/traffic-sources/overview"
    ]
    
    for i, endpoint in enumerate(endpoints_to_try, 1):
        try:
            print(f"Testing endpoint {i}/{len(endpoints_to_try)}: {endpoint}")
            
            response = requests.get(endpoint, headers=headers, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("SimilarWeb API is working!")
                print(f"Working endpoint: {endpoint}")
                print(f"Sample data: {data}")
                return True
            elif response.status_code == 404:
                print("Endpoint not found (404)")
            elif response.status_code == 401:
                print("Unauthorized (401) - Check your API key")
                print(f"Response: {response.text}")
                return False
            elif response.status_code == 403:
                print("Forbidden (403) - API key may not have required permissions")
                print(f"Response: {response.text}")
                return False
            else:
                print(f"API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Error testing endpoint {endpoint}: {e}")
    
    print("All SimilarWeb endpoints failed")
    return False

def test_semrush_api():
    """Test SEMrush API endpoints"""
    print("\nTesting SEMrush API...")
    
    if not SEMRUSH_API_KEY or SEMRUSH_API_KEY == "YOUR_SEMRUSH_API_KEY_HERE":
        print("SEMrush API key not configured")
        return False
    
    try:
        # Test with a well-known domain
        test_domain = "google.com"
        
        params = {
            'key': SEMRUSH_API_KEY,
            'type': 'domain_ranks',
            'domain': test_domain,
            'export_columns': 'Db,Dn,Rk,Or,Ot,Oc,Ad,At,Ac',
            'format': 'json'
        }
        
        print(f"Testing SEMrush API with domain: {test_domain}")
        
        response = requests.get("https://api.semrush.com", params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SEMrush API is working!")
            print(f"Sample data: {data}")
            return True
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing SEMrush API: {e}")
        return False

def test_builtwith_api():
    """Test BuiltWith API endpoints"""
    print("\nTesting BuiltWith API...")
    
    if not BUILTWITH_API_KEY or BUILTWITH_API_KEY == "YOUR_BUILTWITH_API_KEY_HERE":
        print("BuiltWith API key not configured")
        return False
    
    try:
        # Test with a well-known domain
        test_domain = "google.com"
        
        params = {
            'KEY': BUILTWITH_API_KEY,
            'LOOKUP': test_domain,
            'HIDETEXT': 'true',
            'HIDEDL': 'true'
        }
        
        print(f"Testing BuiltWith API with domain: {test_domain}")
        
        response = requests.get("https://api.builtwith.com/v20/api.json", params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("BuiltWith API is working!")
            print(f"Sample data: {data}")
            return True
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing BuiltWith API: {e}")
        return False

def test_wappalyzer_api():
    """Test Wappalyzer API endpoints"""
    print("\nTesting Wappalyzer API...")
    
    if not WAPPALYZER_API_KEY or WAPPALYZER_API_KEY == "YOUR_WAPPALYZER_API_KEY_HERE":
        print("Wappalyzer API key not configured")
        return False
    
    try:
        # Test with a well-known domain
        test_domain = "google.com"
        
        headers = {
            'Authorization': f'Bearer {WAPPALYZER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {'url': f'https://{test_domain}'}
        
        print(f"Testing Wappalyzer API with domain: {test_domain}")
        
        response = requests.post("https://api.wappalyzer.com/v2/lookup", 
                               headers=headers, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Wappalyzer API is working!")
            print(f"Sample data: {data}")
            return True
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing Wappalyzer API: {e}")
        return False

def test_pagespeed_api():
    """Test Google PageSpeed Insights API endpoints"""
    print("\nTesting PageSpeed API...")
    
    if not PAGESPEED_API_KEY or PAGESPEED_API_KEY == "YOUR_PAGESPEED_API_KEY_HERE":
        print("PageSpeed API key not configured")
        return False
    
    try:
        # Test with a well-known domain
        test_domain = "google.com"
        
        params = {
            'url': f'https://{test_domain}',
            'key': PAGESPEED_API_KEY,
            'strategy': 'mobile'
        }
        
        print(f"Testing PageSpeed API with domain: {test_domain}")
        
        response = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed", 
                              params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("PageSpeed API is working!")
            print(f"Sample data: {data}")
            return True
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing PageSpeed API: {e}")
        return False

def main():
    """Main test function"""
    print("API Endpoint Test Script")
    print("=" * 50)
    
    print(f"Mock Data Mode: {USE_MOCK_DATA}")
    print(f"SimilarWeb API Key: {'Configured' if SIMILARWEB_API_KEY and SIMILARWEB_API_KEY != 'YOUR_SIMILARWEB_API_KEY_HERE' else 'Not configured'}")
    print(f"SEMrush API Key: {'Configured' if SEMRUSH_API_KEY and SEMRUSH_API_KEY != 'YOUR_SEMRUSH_API_KEY_HERE' else 'Not configured'}")
    print(f"BuiltWith API Key: {'Configured' if BUILTWITH_API_KEY and BUILTWITH_API_KEY != 'YOUR_BUILTWITH_API_KEY_HERE' else 'Not configured'}")
    print(f"Wappalyzer API Key: {'Configured' if WAPPALYZER_API_KEY and WAPPALYZER_API_KEY != 'YOUR_WAPPALYZER_API_KEY_HERE' else 'Not configured'}")
    print(f"PageSpeed API Key: {'Configured' if PAGESPEED_API_KEY and PAGESPEED_API_KEY != 'YOUR_PAGESPEED_API_KEY_HERE' else 'Not configured'}")
    print()
    
    if USE_MOCK_DATA:
        print("Currently using mock data. Set USE_MOCK_DATA = False in config.py to use real APIs.")
        print()
    
    # Test APIs
    similarweb_ok = test_similarweb_api()
    semrush_ok = test_semrush_api()
    builtwith_ok = test_builtwith_api()
    wappalyzer_ok = test_wappalyzer_api()
    pagespeed_ok = test_pagespeed_api()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"SimilarWeb API (Expensive): {'Working' if similarweb_ok else 'Failed'}")
    print(f"SEMrush API (Expensive): {'Working' if semrush_ok else 'Failed'}")
    print(f"BuiltWith API (Free): {'Working' if builtwith_ok else 'Failed'}")
    print(f"Wappalyzer API (Free): {'Working' if wappalyzer_ok else 'Failed'}")
    print(f"PageSpeed API (Free): {'Working' if pagespeed_ok else 'Failed'}")
    
    free_apis_working = builtwith_ok or wappalyzer_ok or pagespeed_ok
    expensive_apis_working = similarweb_ok or semrush_ok
    
    if not free_apis_working and not expensive_apis_working:
        print("\nTo use real data:")
        print("1. Get FREE API keys from BuiltWith, Wappalyzer, or Google PageSpeed")
        print("2. Update config.py with your API keys")
        print("3. Set USE_MOCK_DATA = False in config.py")
        print("4. Run this test again to verify")
    elif free_apis_working and not expensive_apis_working:
        print("\nGreat! You have free APIs working. The tool will use these for real data.")
    elif expensive_apis_working:
        print("\nYou have expensive APIs working. Consider using free alternatives to save money.")

if __name__ == "__main__":
    main()
