#!/usr/bin/env python3
"""
Diagnostic tool to test what real data we can extract from triesteallnews.it
Tests multiple scraping methods and shows exactly what's available
"""

import requests
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
import json

class WebsiteDiagnostics:
    def __init__(self):
        self.base_url = "https://www.triesteallnews.it"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
    
    def test_basic_connection(self):
        """Test if we can connect to the website at all"""
        print("\n" + "="*80)
        print("TEST 1: Basic Website Connection")
        print("="*80)
        
        test_result = {
            'test_name': 'Basic Connection',
            'success': False,
            'details': {}
        }
        
        try:
            response = requests.get(self.base_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            test_result['details']['status_code'] = response.status_code
            test_result['details']['content_length'] = len(response.content)
            test_result['details']['headers'] = dict(response.headers)
            
            if response.status_code == 200:
                test_result['success'] = True
                print(f"[OK] SUCCESS: Connected to website")
                print(f"   Status Code: {response.status_code}")
                print(f"   Content Length: {len(response.content):,} bytes")
                
                # Check for Cloudflare protection
                if 'cloudflare' in response.text.lower() or 'Just a moment' in response.text:
                    print(f"   [WARNING] Cloudflare protection detected")
                    test_result['details']['cloudflare_protection'] = True
                else:
                    print(f"   [OK] No Cloudflare challenge detected")
                    test_result['details']['cloudflare_protection'] = False
                    
            else:
                print(f"[FAIL] FAILED: Status code {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] ERROR: {str(e)}")
            test_result['details']['error'] = str(e)
        
        self.results['tests'].append(test_result)
        return test_result
    
    def test_cloudscraper(self):
        """Test using cloudscraper to bypass Cloudflare"""
        print("\n" + "="*80)
        print("TEST 2: Cloudscraper Method")
        print("="*80)
        
        test_result = {
            'test_name': 'Cloudscraper',
            'success': False,
            'details': {}
        }
        
        try:
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                }
            )
            
            response = scraper.get(self.base_url, timeout=15)
            
            test_result['details']['status_code'] = response.status_code
            test_result['details']['content_length'] = len(response.content)
            
            if response.status_code == 200 and "Just a moment" not in response.text:
                test_result['success'] = True
                print(f"[OK] SUCCESS: Bypassed Cloudflare protection")
                print(f"   Status Code: {response.status_code}")
                print(f"   Content Length: {len(response.content):,} bytes")
                
                # Try to parse the HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                test_result['details']['title'] = soup.title.string if soup.title else "No title"
                print(f"   Page Title: {test_result['details']['title']}")
                
                # Return the soup for further analysis
                test_result['soup'] = soup
                
            else:
                print(f"[FAIL] FAILED: Could not bypass Cloudflare")
                test_result['details']['cloudflare_blocked'] = True
                
        except Exception as e:
            print(f"[ERROR] ERROR: {str(e)}")
            test_result['details']['error'] = str(e)
        
        self.results['tests'].append(test_result)
        return test_result
    
    def test_article_extraction(self, soup):
        """Test what article data we can extract"""
        print("\n" + "="*80)
        print("TEST 3: Article Data Extraction")
        print("="*80)
        
        test_result = {
            'test_name': 'Article Extraction',
            'success': False,
            'details': {
                'articles_found': 0,
                'articles': []
            }
        }
        
        try:
            # Try different selectors for articles
            selectors_to_try = [
                ('article', 'article tag'),
                ('div.article', 'div with class article'),
                ('div.post', 'div with class post'),
                ('div[class*="entry"]', 'div with entry in class'),
                ('div[class*="item"]', 'div with item in class'),
                ('h2 a', 'h2 links'),
                ('h3 a', 'h3 links'),
                ('a[href*="/"]', 'all links')
            ]
            
            found_articles = []
            
            for selector, description in selectors_to_try:
                elements = soup.select(selector)
                print(f"\n   Testing: {description} -> Found {len(elements)} elements")
                
                if elements and len(elements) > 0:
                    # Try to extract article info from first few elements
                    for i, element in enumerate(elements[:5]):
                        article_info = self._extract_article_info(element)
                        if article_info and article_info not in found_articles:
                            found_articles.append(article_info)
                            print(f"      Article {len(found_articles)}:")
                            print(f"         Title: {article_info.get('title', 'N/A')[:70]}")
                            print(f"         URL: {article_info.get('url', 'N/A')}")
                            print(f"         Date: {article_info.get('date', 'N/A')}")
                            print(f"         Author: {article_info.get('author', 'N/A')}")
                            print(f"         Read Count: {article_info.get('read_count', 'N/A')}")
                            
                            if len(found_articles) >= 10:
                                break
                
                if len(found_articles) >= 10:
                    break
            
            test_result['details']['articles_found'] = len(found_articles)
            test_result['details']['articles'] = found_articles
            
            if len(found_articles) > 0:
                test_result['success'] = True
                print(f"\n[OK] SUCCESS: Extracted {len(found_articles)} articles")
            else:
                print(f"\n[FAIL] FAILED: Could not extract any articles")
                
        except Exception as e:
            print(f"\n[ERROR] ERROR: {str(e)}")
            test_result['details']['error'] = str(e)
        
        self.results['tests'].append(test_result)
        return test_result
    
    def _extract_article_info(self, element):
        """Extract article information from an element"""
        article = {}
        
        try:
            # Get title
            if element.name == 'a':
                article['title'] = element.get_text(strip=True)
                article['url'] = element.get('href', '')
            else:
                link = element.find('a')
                if link:
                    article['title'] = link.get_text(strip=True)
                    article['url'] = link.get('href', '')
                else:
                    # Try to get any text
                    article['title'] = element.get_text(strip=True)[:100]
                    article['url'] = ''
            
            # Skip if no meaningful title
            if not article['title'] or len(article['title']) < 10:
                return None
            
            # Skip navigation/menu items
            skip_words = ['home', 'menu', 'login', 'register', 'contact', 'about', 'search']
            if any(word in article['title'].lower() for word in skip_words):
                return None
            
            # Try to extract date
            date_selectors = ['.date', '.publish-date', '.entry-date', '.post-date', 'time']
            article['date'] = None
            for selector in date_selectors:
                date_elem = element.find(class_=selector.strip('.')) if selector.startswith('.') else element.find(selector)
                if date_elem:
                    article['date'] = date_elem.get_text(strip=True)
                    break
            
            # Try to extract author
            author_selectors = ['.author', '.byline', '.writer', '.by-author']
            article['author'] = None
            for selector in author_selectors:
                author_elem = element.find(class_=selector.strip('.'))
                if author_elem:
                    article['author'] = author_elem.get_text(strip=True)
                    break
            
            # Try to extract read count / views
            view_selectors = [
                '.views', '.read-count', '.view-count', '.readers', 
                '[class*="view"]', '[class*="read"]', '[class*="count"]'
            ]
            article['read_count'] = None
            for selector in view_selectors:
                if selector.startswith('['):
                    view_elem = element.select_one(selector)
                else:
                    view_elem = element.find(class_=selector.strip('.'))
                if view_elem:
                    text = view_elem.get_text(strip=True)
                    # Try to extract numbers
                    import re
                    numbers = re.findall(r'\d+', text)
                    if numbers:
                        article['read_count'] = numbers[0]
                        break
            
            # Try to extract category
            category_selectors = ['.category', '.tag', '.section']
            article['category'] = None
            for selector in category_selectors:
                cat_elem = element.find(class_=selector.strip('.'))
                if cat_elem:
                    article['category'] = cat_elem.get_text(strip=True)
                    break
            
            # Make URL absolute
            if article['url'] and not article['url'].startswith('http'):
                if article['url'].startswith('/'):
                    article['url'] = f"{self.base_url}{article['url']}"
                else:
                    article['url'] = f"{self.base_url}/{article['url']}"
            
            return article
            
        except Exception:
            return None
    
    def test_specific_page(self, url):
        """Test a specific page to see what data is available"""
        print("\n" + "="*80)
        print(f"TEST 4: Specific Page Analysis - {url}")
        print("="*80)
        
        test_result = {
            'test_name': 'Specific Page',
            'success': False,
            'details': {}
        }
        
        try:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract all possible metadata
                print(f"\n   Analyzing page structure:")
                
                # Title
                title = soup.find('h1')
                print(f"   Title: {title.get_text(strip=True) if title else 'Not found'}")
                
                # Meta tags
                print(f"\n   Meta Tags:")
                meta_tags = soup.find_all('meta')
                for meta in meta_tags[:10]:
                    name = meta.get('name') or meta.get('property', '')
                    content = meta.get('content', '')
                    if name and content:
                        print(f"      {name}: {content[:80]}")
                
                # Check for structured data (JSON-LD)
                print(f"\n   Structured Data (JSON-LD):")
                json_ld = soup.find_all('script', type='application/ld+json')
                if json_ld:
                    for i, script in enumerate(json_ld[:3]):
                        try:
                            data = json.loads(script.string)
                            print(f"      Schema {i+1}: {json.dumps(data, indent=6)[:200]}...")
                        except:
                            pass
                else:
                    print(f"      No JSON-LD found")
                
                test_result['success'] = True
                
            else:
                print(f"   [FAIL] Could not load page: Status {response.status_code}")
                
        except Exception as e:
            print(f"   [ERROR] ERROR: {str(e)}")
            test_result['details']['error'] = str(e)
        
        self.results['tests'].append(test_result)
        return test_result
    
    def save_report(self, filename='diagnostic_report.json'):
        """Save diagnostic report to file"""
        # Remove soup objects (not JSON serializable)
        for test in self.results['tests']:
            if 'soup' in test:
                del test['soup']
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n" + "="*80)
        print(f"Diagnostic report saved to: {filename}")
        print("="*80)
    
    def run_full_diagnostic(self):
        """Run all diagnostic tests"""
        print("\n")
        print("=" * 80)
        print(" " * 20 + "WEBSITE DATA DIAGNOSTIC TOOL")
        print(" " * 25 + "triesteallnews.it")
        print("=" * 80)
        
        # Test 1: Basic connection
        basic_result = self.test_basic_connection()
        
        # Test 2: Cloudscraper
        scraper_result = self.test_cloudscraper()
        
        # Test 3: Extract articles if we got a soup
        if scraper_result.get('success') and 'soup' in scraper_result:
            article_result = self.test_article_extraction(scraper_result['soup'])
            
            # Test 4: If we found articles, test a specific one
            if article_result['success'] and article_result['details']['articles']:
                first_article = article_result['details']['articles'][0]
                if first_article.get('url') and first_article['url'].startswith('http'):
                    self.test_specific_page(first_article['url'])
        
        # Summary
        print("\n" + "="*80)
        print("DIAGNOSTIC SUMMARY")
        print("="*80)
        
        total_tests = len(self.results['tests'])
        successful_tests = sum(1 for test in self.results['tests'] if test['success'])
        
        print(f"\nTotal Tests Run: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        
        print(f"\nConclusion:")
        if successful_tests >= 3:
            print("   [OK] Website is accessible and we can extract article data")
        elif successful_tests >= 2:
            print("   [WARNING] Website is accessible but article extraction is limited")
        elif successful_tests >= 1:
            print("   [WARNING] Website is accessible but heavily protected")
        else:
            print("   [FAIL] Cannot access website - all methods failed")
        
        # Save report
        self.save_report()

def main():
    diagnostics = WebsiteDiagnostics()
    diagnostics.run_full_diagnostic()

if __name__ == "__main__":
    main()

