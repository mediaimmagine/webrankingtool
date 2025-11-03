#!/usr/bin/env python3
"""
Test different URLs and structure of triesteallnews.it
"""

import requests
import cloudscraper
from bs4 import BeautifulSoup
import json

def test_urls():
    """Test various URLs to find the site structure"""
    
    base_url = "https://www.triesteallnews.it"
    
    # URLs to try
    test_urls = [
        "/",
        "/cronaca",
        "/cronaca/",
        "/sport",
        "/sport/",
        "/politica",
        "/cultura",
        "/home",
        "/index.php",
        "/wp-json/wp/v2/posts?per_page=10",  # WordPress REST API
        "/wp-json/wp/v2/posts?per_page=10&orderby=date",
        "/wp-json/",
    ]
    
    scraper = cloudscraper.create_scraper()
    
    print("="*80)
    print("TESTING WEBSITE URL STRUCTURE")
    print("="*80)
    
    for url_path in test_urls:
        full_url = base_url + url_path
        print(f"\n{full_url}")
        print("-"*80)
        
        try:
            response = scraper.get(full_url, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Content Length: {len(response.content):,} bytes")
            
            # Check content type
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            # If it's JSON (WordPress API)
            if 'json' in content_type:
                try:
                    data = response.json()
                    print(f"JSON Response: {type(data)}")
                    if isinstance(data, list):
                        print(f"Number of posts: {len(data)}")
                        if data:
                            # Show first post
                            post = data[0]
                            print(f"\nFirst Post:")
                            print(f"  ID: {post.get('id')}")
                            print(f"  Title: {post.get('title', {}).get('rendered', 'N/A')[:80]}")
                            print(f"  Date: {post.get('date', 'N/A')}")
                            print(f"  Link: {post.get('link', 'N/A')}")
                            print(f"  Author ID: {post.get('author', 'N/A')}")
                            
                            # Check for custom fields that might have view count
                            if 'meta' in post:
                                print(f"  Meta fields: {post['meta']}")
                            if 'acf' in post:
                                print(f"  ACF fields: {post['acf']}")
                    elif isinstance(data, dict):
                        print(f"JSON keys: {list(data.keys())[:10]}")
                except json.JSONDecodeError:
                    print("Could not parse JSON")
            
            # If it's HTML
            elif 'html' in content_type:
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find('title')
                    if title:
                        print(f"Page Title: {title.get_text()[:80]}")
                    
                    # Look for article links
                    links = soup.find_all('a', href=True, limit=5)
                    article_links = [a for a in links if len(a.get_text(strip=True)) > 20]
                    if article_links:
                        print(f"\nSample article links found: {len(article_links)}")
                        for i, link in enumerate(article_links[:3], 1):
                            print(f"  {i}. {link.get_text(strip=True)[:60]}")
                            print(f"     URL: {link['href']}")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    test_urls()


