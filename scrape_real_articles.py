#!/usr/bin/env python3
"""
Scrape real articles from triesteallnews.it category pages
"""

import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

def scrape_category_page(category='cronaca'):
    """Scrape articles from a category page"""
    
    base_url = "https://www.triesteallnews.it"
    url = f"{base_url}/{category}"
    
    print("="*80)
    print(f"SCRAPING CATEGORY: {category}")
    print(f"URL: {url}")
    print("="*80)
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Content Length: {len(response.content):,} bytes")
        
        if response.status_code != 200:
            print(f"[FAIL] Could not access page")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"\n[OK] Page loaded successfully")
        print(f"Page Title: {soup.title.string if soup.title else 'N/A'}")
        
        # Save HTML for analysis
        with open(f'sample_page_{category}.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"\n[INFO] Saved HTML to: sample_page_{category}.html")
        
        # Try to find article elements
        print(f"\n" + "="*80)
        print("LOOKING FOR ARTICLE ELEMENTS")
        print("="*80)
        
        articles_found = []
        
        # Try different selectors
        selectors = [
            ('article', 'article tags'),
            ('div[class*="post"]', 'divs with "post" in class'),
            ('div[class*="entry"]', 'divs with "entry" in class'),
            ('div[class*="item"]', 'divs with "item" in class'),
            ('div[class*="card"]', 'divs with "card" in class'),
            ('div[class*="article"]', 'divs with "article" in class'),
            ('h1 a', 'h1 links'),
            ('h2 a', 'h2 links'),
            ('h3 a', 'h3 links'),
            ('a[class*="title"]', 'links with "title" in class'),
            ('a[rel="bookmark"]', 'bookmark links'),
        ]
        
        for selector, description in selectors:
            elements = soup.select(selector)
            print(f"\n{description} ({selector}): {len(elements)} found")
            
            if len(elements) > 0:
                # Show first few
                for i, elem in enumerate(elements[:5], 1):
                    text = elem.get_text(strip=True)[:80]
                    href = elem.get('href', 'N/A') if elem.name == 'a' else 'N/A'
                    classes = elem.get('class', [])
                    print(f"  {i}. Text: {text}")
                    if href != 'N/A':
                        print(f"     URL: {href}")
                    print(f"     Classes: {classes}")
        
        # Look for specific data fields
        print(f"\n" + "="*80)
        print("LOOKING FOR METADATA FIELDS")
        print("="*80)
        
        # Date elements
        date_elements = soup.find_all(['time', 'span'], class_=re.compile(r'date|time', re.I))
        print(f"\nDate/Time elements: {len(date_elements)}")
        for i, elem in enumerate(date_elements[:5], 1):
            print(f"  {i}. {elem.get('class')}: {elem.get_text(strip=True)}")
            if elem.get('datetime'):
                print(f"     datetime attr: {elem.get('datetime')}")
        
        # Author elements
        author_elements = soup.find_all(class_=re.compile(r'author|byline', re.I))
        print(f"\nAuthor elements: {len(author_elements)}")
        for i, elem in enumerate(author_elements[:5], 1):
            print(f"  {i}. {elem.get('class')}: {elem.get_text(strip=True)}")
        
        # View/read count elements
        view_elements = soup.find_all(class_=re.compile(r'view|read|count|visits', re.I))
        print(f"\nView/Read count elements: {len(view_elements)}")
        for i, elem in enumerate(view_elements[:10], 1):
            text = elem.get_text(strip=True)
            if text and len(text) < 50:  # Skip long text
                print(f"  {i}. {elem.get('class')}: {text}")
        
        # Category/tag elements
        category_elements = soup.find_all(class_=re.compile(r'category|tag|section', re.I))
        print(f"\nCategory/Tag elements: {len(category_elements)}")
        for i, elem in enumerate(category_elements[:10], 1):
            text = elem.get_text(strip=True)
            if text and len(text) < 50:
                print(f"  {i}. {elem.get('class')}: {text}")
        
        # Look for structured data
        print(f"\n" + "="*80)
        print("LOOKING FOR STRUCTURED DATA")
        print("="*80)
        
        json_ld = soup.find_all('script', type='application/ld+json')
        print(f"\nJSON-LD scripts: {len(json_ld)}")
        for i, script in enumerate(json_ld, 1):
            try:
                data = json.loads(script.string)
                print(f"\nJSON-LD {i}:")
                print(f"  @type: {data.get('@type')}")
                if data.get('@type') == 'Article':
                    print(f"  headline: {data.get('headline', 'N/A')}")
                    print(f"  datePublished: {data.get('datePublished', 'N/A')}")
                    print(f"  author: {data.get('author', 'N/A')}")
                    print(f"  interactionCount: {data.get('interactionStatistic', 'N/A')}")
                print(f"  Keys: {list(data.keys())[:10]}")
            except json.JSONDecodeError:
                print(f"  Could not parse JSON-LD {i}")
        
        # Check meta tags
        print(f"\n" + "="*80)
        print("META TAGS")
        print("="*80)
        
        meta_tags = soup.find_all('meta', attrs={'property': True})
        for meta in meta_tags[:15]:
            prop = meta.get('property', '')
            content = meta.get('content', '')
            if prop and content:
                print(f"  {prop}: {content[:80]}")
        
        print("\n" + "="*80)
        print("SCRAPING COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Test scraping multiple categories"""
    categories = ['cronaca', 'sport', 'politica']
    
    for category in categories:
        scrape_category_page(category)
        print("\n\n")

if __name__ == "__main__":
    main()


