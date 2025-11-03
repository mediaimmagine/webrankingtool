#!/usr/bin/env python3
"""
Test WordPress API with miniOrange OAuth 2.0 Authentication
"""

import requests
import base64
import json

base_url = "https://www.triesteallnews.it"
client_id = "3epDCiDKlSAN"
client_secret = "aWr0PgkvIu7RhtiRXYm3kahQ"

print("\n" + "="*80)
print("TESTING WORDPRESS API WITH MINIORANGE OAUTH 2.0")
print("="*80)
print(f"Website: {base_url}")
print(f"Client ID: {client_id}")
print(f"Authentication: OAuth 2.0 (miniOrange)")

# Step 1: Get Access Token
print("\n" + "="*80)
print("STEP 1: Getting OAuth Access Token")
print("="*80)

# Try different token endpoints that miniOrange might use
token_endpoints = [
    f"{base_url}/wp-json/miniorange-api/v1/token",
    f"{base_url}/wp-json/mo-api-auth/v1/token",
    f"{base_url}/oauth/token",
    f"{base_url}/wp-json/oauth/token",
    f"{base_url}/wp-json/api/v1/token"
]

access_token = None

for token_endpoint in token_endpoints:
    print(f"\nTrying: {token_endpoint}")
    
    try:
        # Prepare OAuth token request
        # Method 1: Client credentials in body
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        response = requests.post(
            token_endpoint,
            data=token_data,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_response = response.json()
            access_token = token_response.get('access_token')
            
            if access_token:
                print(f"[SUCCESS] Access token obtained!")
                print(f"Token type: {token_response.get('token_type', 'Bearer')}")
                print(f"Expires in: {token_response.get('expires_in', 'Unknown')} seconds")
                break
        
    except Exception as e:
        print(f"Error: {str(e)}")

# If standard token endpoint doesn't work, try direct API access with credentials
if not access_token:
    print(f"\n[INFO] Standard OAuth token endpoints not found")
    print(f"[INFO] Trying direct API access with client credentials...")

# Step 2: Make API Request
print("\n" + "="*80)
print("STEP 2: Fetching Posts from WordPress API")
print("="*80)

try:
    # Prepare headers
    if access_token:
        # Use Bearer token if we got one
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        print(f"Using Bearer token authentication")
    else:
        # Try Basic Auth with client credentials
        credentials = f"{client_id}:{client_secret}"
        token = base64.b64encode(credentials.encode()).decode()
        headers = {
            'Authorization': f'Basic {token}',
            'Accept': 'application/json'
        }
        print(f"Using Basic Auth with client credentials")
    
    # Add common headers
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    headers['Content-Type'] = 'application/json'
    
    response = requests.get(
        f"{base_url}/wp-json/wp/v2/posts",
        headers=headers,
        params={
            'per_page': 5,
            '_embed': True
        },
        timeout=15
    )
    
    print(f"\nEndpoint: {base_url}/wp-json/wp/v2/posts")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        posts = response.json()
        total_posts = response.headers.get('X-WP-Total', 'Unknown')
        
        print(f"\n{'='*80}")
        print("[SUCCESS] API ACCESS WORKING!")
        print(f"{'='*80}")
        print(f"Retrieved: {len(posts)} posts")
        print(f"Total Available: {total_posts} posts")
        
        # Display posts
        print(f"\n{'='*80}")
        print("ARTICLES RETRIEVED")
        print(f"{'='*80}")
        
        for i, post in enumerate(posts, 1):
            title = post.get('title', {}).get('rendered', 'No title')
            date = post.get('date', 'No date')[:10]
            link = post.get('link', 'No link')
            
            # Get author name from embedded data
            author_name = 'Unknown'
            if '_embedded' in post and 'author' in post['_embedded']:
                author_data = post['_embedded']['author'][0]
                author_name = author_data.get('name', 'Unknown')
            
            # Get categories
            categories = []
            if '_embedded' in post and 'wp:term' in post['_embedded']:
                terms = post['_embedded']['wp:term']
                if terms and len(terms) > 0:
                    categories = [cat.get('name', '') for cat in terms[0]]
            
            print(f"\n{i}. {title[:70]}")
            print(f"   Date: {date} | Author: {author_name}")
            print(f"   Categories: {', '.join(categories) if categories else 'None'}")
            print(f"   URL: {link}")
        
        # Search for view counts
        print(f"\n{'='*80}")
        print("SEARCHING FOR VIEW COUNT FIELDS")
        print(f"{'='*80}")
        
        view_field_names = [
            'views', 'view_count', 'post_views', 'post_views_count',
            'visits', 'visit_count', 'pageviews', 'page_views'
        ]
        
        all_view_fields = set()
        for post in posts:
            # Check root level
            for field in view_field_names:
                if field in post:
                    all_view_fields.add(f"{field} (root level)")
            
            # Check meta
            if 'meta' in post and isinstance(post['meta'], dict):
                for field in view_field_names:
                    if field in post['meta']:
                        all_view_fields.add(f"{field} (in meta)")
        
        if all_view_fields:
            print(f"\n[SUCCESS] Found view count fields:")
            for field in all_view_fields:
                print(f"  - {field}")
            print(f"\n[EXCELLENT] You have REAL visit/view count data available!")
        else:
            print(f"\n[INFO] No view count fields found")
            print(f"[INFO] The site may not have a view counter plugin installed")
            print(f"\n[RECOMMENDATION] Install one of these WordPress plugins:")
            print(f"  - WP-PostViews")
            print(f"  - Post Views Counter")
        
        # Save sample post
        if posts:
            with open('miniorange_oauth_sample_post.json', 'w', encoding='utf-8') as f:
                json.dump(posts[0], f, indent=2, ensure_ascii=False)
            print(f"\n[INFO] Full post data saved to: miniorange_oauth_sample_post.json")
        
        # Save credentials for future use
        config = {
            'base_url': base_url,
            'authentication_method': 'oauth',
            'client_id': client_id,
            'client_secret': client_secret,
            'access_token': access_token if access_token else None
        }
        
        with open('miniorange_oauth_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print(f"[INFO] OAuth credentials saved to: miniorange_oauth_config.json")
        
    elif response.status_code == 401:
        print(f"\n[FAIL] 401 Unauthorized")
        print(f"[INFO] Authentication failed")
        
        try:
            error = response.json()
            print(f"\nError Details:")
            print(json.dumps(error, indent=2))
        except:
            print(f"Response: {response.text[:300]}")
        
        print(f"\n[HELP] Possible issues:")
        print(f"  1. Client ID or Secret incorrect")
        print(f"  2. OAuth not properly configured in miniOrange")
        print(f"  3. Need to request access token first")
        
    elif response.status_code == 403:
        print(f"\n[FAIL] 403 Forbidden")
        print(f"[INFO] Access denied by server")
        print(f"\n[HELP] Check miniOrange IP whitelist settings")
        
    elif response.status_code == 400:
        print(f"\n[FAIL] 400 Bad Request")
        
        try:
            error = response.json()
            print(f"\nError Details:")
            print(json.dumps(error, indent=2))
        except:
            print(f"Response: {response.text[:300]}")
        
        print(f"\n[HELP] The credentials format might still be incorrect")
        print(f"[HELP] Check miniOrange documentation for exact OAuth format")
        
    else:
        print(f"\n[FAIL] Unexpected status code: {response.status_code}")
        try:
            error = response.json()
            print(f"Response:")
            print(json.dumps(error, indent=2))
        except:
            print(f"Response: {response.text[:300]}")
        
except requests.exceptions.Timeout:
    print(f"\n[ERROR] Request timeout")
except requests.exceptions.ConnectionError:
    print(f"\n[ERROR] Connection error")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*80}")
print("TEST COMPLETE")
print(f"{'='*80}")

