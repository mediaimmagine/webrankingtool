#!/usr/bin/env python3
"""
WordPress REST API Tester for triesteallnews.it
Tests authenticated API access and available data fields
"""

import requests
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional
import getpass

class WordPressAPITester:
    """
    Test WordPress REST API access and explore available data
    """
    
    def __init__(self, base_url: str, username: str, app_password: str):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        self.username = username
        self.app_password = app_password
        
        # Create Basic Auth header
        credentials = f"{username}:{app_password}"
        token = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {token}',
            'User-Agent': 'TriesteNewsAnalytics/1.0',
            'Accept': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """Test if API connection works"""
        print("\n" + "="*80)
        print("TESTING WORDPRESS REST API CONNECTION")
        print("="*80)
        
        try:
            # Test basic API endpoint
            response = requests.get(f"{self.base_url}/wp-json", headers=self.headers, timeout=10)
            
            print(f"\nAPI Endpoint: {self.base_url}/wp-json")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] API is accessible!")
                print(f"Site Name: {data.get('name', 'N/A')}")
                print(f"Description: {data.get('description', 'N/A')}")
                print(f"URL: {data.get('url', 'N/A')}")
                print(f"Namespaces: {', '.join(data.get('namespaces', []))}")
                return True
            else:
                print(f"[FAIL] API returned status {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Connection failed: {str(e)}")
            return False
    
    def test_authentication(self) -> bool:
        """Test if authentication works"""
        print("\n" + "="*80)
        print("TESTING AUTHENTICATION")
        print("="*80)
        
        try:
            # Try to access users endpoint (requires authentication)
            response = requests.get(f"{self.api_url}/users/me", headers=self.headers, timeout=10)
            
            print(f"\nEndpoint: {self.api_url}/users/me")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Authentication successful!")
                print(f"Username: {data.get('name', 'N/A')}")
                print(f"User ID: {data.get('id', 'N/A')}")
                print(f"Roles: {', '.join(data.get('roles', []))}")
                print(f"Capabilities: {len(data.get('capabilities', {}))} permissions")
                return True
            elif response.status_code == 401:
                print(f"[FAIL] Authentication failed - 401 Unauthorized")
                error_data = response.json()
                print(f"Error: {error_data.get('message', 'Unknown error')}")
                return False
            else:
                print(f"[WARN] Unexpected status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Authentication test failed: {str(e)}")
            return False
    
    def get_posts(self, per_page: int = 10, orderby: str = 'date') -> Optional[List[Dict]]:
        """Fetch posts from the API"""
        print("\n" + "="*80)
        print(f"FETCHING POSTS (per_page={per_page}, orderby={orderby})")
        print("="*80)
        
        try:
            params = {
                'per_page': per_page,
                'orderby': orderby,
                'order': 'desc',
                '_embed': True  # Include embedded data (author, featured media, etc.)
            }
            
            response = requests.get(
                f"{self.api_url}/posts",
                headers=self.headers,
                params=params,
                timeout=15
            )
            
            print(f"\nEndpoint: {self.api_url}/posts")
            print(f"Status Code: {response.status_code}")
            print(f"Total Posts Available: {response.headers.get('X-WP-Total', 'Unknown')}")
            print(f"Total Pages: {response.headers.get('X-WP-TotalPages', 'Unknown')}")
            
            if response.status_code == 200:
                posts = response.json()
                print(f"[OK] Retrieved {len(posts)} posts")
                return posts
            else:
                print(f"[FAIL] Could not fetch posts")
                print(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Failed to fetch posts: {str(e)}")
            return None
    
    def analyze_post_fields(self, posts: List[Dict]):
        """Analyze available fields in posts"""
        print("\n" + "="*80)
        print("ANALYZING POST DATA FIELDS")
        print("="*80)
        
        if not posts:
            print("[WARN] No posts to analyze")
            return
        
        # Get first post as sample
        sample_post = posts[0]
        
        print(f"\n[INFO] Analyzing first post:")
        print(f"Title: {sample_post.get('title', {}).get('rendered', 'N/A')[:60]}...")
        
        # Standard fields
        print(f"\n{'='*80}")
        print("STANDARD WORDPRESS FIELDS")
        print(f"{'='*80}")
        
        standard_fields = {
            'id': 'Post ID',
            'date': 'Publication Date',
            'date_gmt': 'Publication Date (GMT)',
            'modified': 'Modified Date',
            'slug': 'URL Slug',
            'status': 'Post Status',
            'type': 'Post Type',
            'link': 'Full URL',
            'title': 'Title',
            'content': 'Content',
            'excerpt': 'Excerpt',
            'author': 'Author ID',
            'featured_media': 'Featured Image ID',
            'comment_status': 'Comments Enabled',
            'categories': 'Category IDs',
            'tags': 'Tag IDs'
        }
        
        for field, description in standard_fields.items():
            value = sample_post.get(field)
            if value is not None:
                if isinstance(value, dict):
                    print(f"  ✓ {description} ({field}): [dict with {len(value)} keys]")
                elif isinstance(value, list):
                    print(f"  ✓ {description} ({field}): [list with {len(value)} items]")
                elif isinstance(value, str) and len(value) > 50:
                    print(f"  ✓ {description} ({field}): {value[:50]}...")
                else:
                    print(f"  ✓ {description} ({field}): {value}")
        
        # Custom fields / meta
        print(f"\n{'='*80}")
        print("CUSTOM FIELDS & META DATA")
        print(f"{'='*80}")
        
        if 'meta' in sample_post:
            meta = sample_post['meta']
            if meta and isinstance(meta, dict):
                print(f"[INFO] Found {len(meta)} meta fields:")
                for key, value in list(meta.items())[:20]:  # Show first 20
                    print(f"  • {key}: {value}")
            else:
                print("[INFO] No meta fields found")
        
        # ACF (Advanced Custom Fields)
        if 'acf' in sample_post:
            acf = sample_post['acf']
            if acf and isinstance(acf, dict):
                print(f"\n[INFO] Found ACF fields:")
                for key, value in acf.items():
                    print(f"  • {key}: {value}")
        
        # Embedded data
        print(f"\n{'='*80}")
        print("EMBEDDED DATA (Author, Categories, etc.)")
        print(f"{'='*80}")
        
        if '_embedded' in sample_post:
            embedded = sample_post['_embedded']
            print(f"[INFO] Embedded data keys: {list(embedded.keys())}")
            
            # Author data
            if 'author' in embedded and embedded['author']:
                author = embedded['author'][0]
                print(f"\nAuthor Information:")
                print(f"  Name: {author.get('name', 'N/A')}")
                print(f"  ID: {author.get('id', 'N/A')}")
                print(f"  URL: {author.get('link', 'N/A')}")
            
            # Categories
            if 'wp:term' in embedded:
                terms = embedded['wp:term']
                if terms and len(terms) > 0:
                    categories = terms[0]  # First array is categories
                    print(f"\nCategories:")
                    for cat in categories:
                        print(f"  • {cat.get('name', 'N/A')} (ID: {cat.get('id', 'N/A')})")
        
        # Look for view count fields
        print(f"\n{'='*80}")
        print("SEARCHING FOR VIEW/VISIT COUNT FIELDS")
        print(f"{'='*80}")
        
        view_fields_found = []
        
        # Common plugin field names for view counts
        view_field_names = [
            'views', 'view_count', 'post_views', 'post_views_count',
            'visits', 'visit_count', 'pageviews', 'page_views',
            'hits', 'hit_count', 'reader_count', 'read_count',
            'wp_postviews', 'post_view_count', 'ga_pageviews'
        ]
        
        # Check in root level
        for field in view_field_names:
            if field in sample_post:
                view_fields_found.append((field, sample_post[field], 'root'))
        
        # Check in meta
        if 'meta' in sample_post and isinstance(sample_post['meta'], dict):
            for field in view_field_names:
                if field in sample_post['meta']:
                    view_fields_found.append((field, sample_post['meta'][field], 'meta'))
        
        # Check in ACF
        if 'acf' in sample_post and isinstance(sample_post['acf'], dict):
            for field in view_field_names:
                if field in sample_post['acf']:
                    view_fields_found.append((field, sample_post['acf'][field], 'acf'))
        
        if view_fields_found:
            print(f"[SUCCESS] Found {len(view_fields_found)} potential view count field(s):")
            for field_name, value, location in view_fields_found:
                print(f"  ✓ {field_name} (in {location}): {value}")
        else:
            print("[INFO] No view count fields found")
            print("[INFO] The site may not have a view counter plugin installed")
            print("[INFO] Common plugins: WP-PostViews, Post Views Counter, Simple View Counter")
        
        # Save sample post to file for detailed analysis
        with open('sample_post_data.json', 'w', encoding='utf-8') as f:
            json.dump(sample_post, f, indent=2, ensure_ascii=False)
        print(f"\n[INFO] Full post data saved to: sample_post_data.json")
    
    def list_all_posts(self, posts: List[Dict]):
        """List all fetched posts"""
        print("\n" + "="*80)
        print("POSTS LISTING")
        print("="*80)
        
        for i, post in enumerate(posts, 1):
            title = post.get('title', {}).get('rendered', 'No title')
            date = post.get('date', 'No date')
            link = post.get('link', 'No link')
            
            # Get author name from embedded data
            author = 'Unknown'
            if '_embedded' in post and 'author' in post['_embedded']:
                author_data = post['_embedded']['author'][0]
                author = author_data.get('name', 'Unknown')
            
            # Get categories from embedded data
            categories = []
            if '_embedded' in post and 'wp:term' in post['_embedded']:
                terms = post['_embedded']['wp:term']
                if terms and len(terms) > 0:
                    categories = [cat.get('name', '') for cat in terms[0]]
            
            print(f"\n{i}. {title[:70]}")
            print(f"   Date: {date[:10]} | Author: {author}")
            print(f"   Categories: {', '.join(categories) if categories else 'None'}")
            print(f"   URL: {link}")
    
    def run_full_test(self):
        """Run all tests"""
        print("\n")
        print("="*80)
        print("WORDPRESS REST API FULL TEST SUITE")
        print("="*80)
        print(f"Website: {self.base_url}")
        print(f"Username: {self.username}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Test 1: Connection
        if not self.test_connection():
            print("\n[FAIL] Cannot proceed - API not accessible")
            return
        
        # Test 2: Authentication
        if not self.test_authentication():
            print("\n[FAIL] Cannot proceed - Authentication failed")
            print("\n[HELP] Please verify:")
            print("  1. Username is correct")
            print("  2. Application Password is correct (not regular password)")
            print("  3. Application Passwords are enabled in WordPress")
            return
        
        # Test 3: Fetch posts
        posts = self.get_posts(per_page=10, orderby='date')
        
        if not posts:
            print("\n[FAIL] Cannot proceed - No posts retrieved")
            return
        
        # Test 4: Analyze post structure
        self.analyze_post_fields(posts)
        
        # Test 5: List posts
        self.list_all_posts(posts)
        
        # Final summary
        print("\n" + "="*80)
        print("TEST COMPLETE")
        print("="*80)
        print(f"\n[OK] Successfully retrieved {len(posts)} posts")
        print(f"[OK] All post metadata is accessible")
        print(f"\nNext Steps:")
        print("  1. Check sample_post_data.json for complete data structure")
        print("  2. Look for view count fields in the analysis above")
        print("  3. If no view counts, consider installing a WordPress plugin")


def main():
    """Interactive test"""
    print("\n")
    print("="*80)
    print("WORDPRESS REST API AUTHENTICATION SETUP")
    print("="*80)
    
    # Get credentials
    base_url = input("\nWebsite URL (default: https://www.triesteallnews.it): ").strip()
    if not base_url:
        base_url = "https://www.triesteallnews.it"
    
    username = input("Username: ").strip()
    if not username:
        print("[ERROR] Username is required")
        return
    
    print("\nApplication Password:")
    print("(Create in WordPress: Users → Profile → Application Passwords)")
    app_password = getpass.getpass("Application Password: ").strip()
    
    if not app_password:
        print("[ERROR] Application Password is required")
        return
    
    # Remove spaces from app password (WordPress format)
    app_password = app_password.replace(' ', '')
    
    # Create tester and run tests
    tester = WordPressAPITester(base_url, username, app_password)
    tester.run_full_test()


if __name__ == "__main__":
    main()

