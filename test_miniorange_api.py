#!/usr/bin/env python3
"""
Test WordPress API with miniOrange Basic Authentication
"""

import requests
import base64
import json

base_url = "https://www.triesteallnews.it"
username = "redazioneMarketing"
app_password = "uq5zlraxnmXeOySouuLTCfGl"

print("\n" + "="*80)
print("TESTING WORDPRESS API WITH MINIORANGE BASIC AUTHENTICATION")
print("="*80)
print(f"Website: {base_url}")
print(f"Username: {username}")
print(f"Authentication: Basic Auth (miniOrange)")

# Create Basic Auth header
credentials = f"{username}:{app_password}"
token = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {token}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Test 1: Try to get posts
print("\n" + "="*80)
print("TEST 1: Fetching Posts from WordPress API")
print("="*80)

try:
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
    print(f"Headers Sent: Authorization: Basic [REDACTED]")
    
    if response.status_code == 200:
        posts = response.json()
        total_posts = response.headers.get('X-WP-Total', 'Unknown')
        
        print(f"\n[SUCCESS] API Access Working!")
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
            author_id = post.get('author', 'Unknown')
            
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
            
            # Check for view count fields
            view_fields_found = []
            
            # Check common view count field names
            view_field_names = [
                'views', 'view_count', 'post_views', 'post_views_count',
                'visits', 'visit_count', 'pageviews', 'page_views'
            ]
            
            # Check in root
            for field in view_field_names:
                if field in post:
                    view_fields_found.append((field, post[field], 'root'))
            
            # Check in meta
            if 'meta' in post and isinstance(post['meta'], dict):
                for field in view_field_names:
                    if field in post['meta']:
                        view_fields_found.append((field, post['meta'][field], 'meta'))
            
            if view_fields_found:
                for field_name, value, location in view_fields_found:
                    print(f"   [VIEW COUNT] {field_name} ({location}): {value}")
        
        # Save first post for detailed analysis
        if posts:
            with open('miniorange_api_sample_post.json', 'w', encoding='utf-8') as f:
                json.dump(posts[0], f, indent=2, ensure_ascii=False)
            print(f"\n[INFO] Full post data saved to: miniorange_api_sample_post.json")
        
        # Search for view counts across all posts
        print(f"\n{'='*80}")
        print("SEARCHING FOR VIEW COUNT FIELDS")
        print(f"{'='*80}")
        
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
            print(f"  - Simple View Counter")
        
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
        print(f"  1. Username or password incorrect")
        print(f"  2. miniOrange plugin not configured properly")
        print(f"  3. User doesn't have sufficient permissions")
        
    elif response.status_code == 403:
        print(f"\n[FAIL] 403 Forbidden")
        print(f"[INFO] Access denied by server")
        
        print(f"\n[HELP] Possible issues:")
        print(f"  1. REST API disabled in miniOrange")
        print(f"  2. IP address not whitelisted (if IP restriction enabled)")
        print(f"  3. Server firewall blocking API access")
        print(f"  4. nginx configuration blocking /wp-json")
        
    elif response.status_code == 400:
        print(f"\n[FAIL] 400 Bad Request")
        
        try:
            error = response.json()
            print(f"\nError Details:")
            print(json.dumps(error, indent=2))
        except:
            print(f"Response: {response.text[:300]}")
        
        print(f"\n[HELP] This might mean:")
        print(f"  1. miniOrange expects different authentication format")
        print(f"  2. Additional configuration needed in miniOrange")
        print(f"  3. Wrong authentication method selected")
        
    else:
        print(f"\n[FAIL] Unexpected status code: {response.status_code}")
        print(f"Response: {response.text[:300]}")
        
except requests.exceptions.Timeout:
    print(f"\n[ERROR] Request timeout - server took too long to respond")
except requests.exceptions.ConnectionError:
    print(f"\n[ERROR] Connection error - cannot reach server")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

# Test 2: Check authentication endpoint
print(f"\n{'='*80}")
print("TEST 2: Checking User Authentication")
print(f"{'='*80}")

try:
    response = requests.get(
        f"{base_url}/wp-json/wp/v2/users/me",
        headers=headers,
        timeout=10
    )
    
    print(f"\nEndpoint: {base_url}/wp-json/wp/v2/users/me")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"\n[SUCCESS] User authentication confirmed!")
        print(f"User Name: {user_data.get('name', 'N/A')}")
        print(f"User ID: {user_data.get('id', 'N/A')}")
        print(f"Roles: {', '.join(user_data.get('roles', []))}")
    else:
        print(f"[INFO] Status {response.status_code} - User endpoint may require different permissions")
        
except Exception as e:
    print(f"[INFO] Could not access user endpoint: {str(e)}")

print(f"\n{'='*80}")
print("TEST COMPLETE")
print(f"{'='*80}")

