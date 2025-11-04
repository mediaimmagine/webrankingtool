#!/usr/bin/env python3
"""
SEOZoom Keyword Analysis
Get most used keywords for a domain using SEOZoom API
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime

class SEOZoomKeywords:
    """SEOZoom keyword analysis"""
    
    def __init__(self, api_key: str, base_url: str = "https://apiv2.seozoom.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 30
    
    def get_keywords(self, domain: str, limit: int = 100, db: str = 'it') -> Optional[Dict]:
        """
        Get top keywords for a domain
        
        Args:
            domain: Domain to analyze (e.g., 'triesteallnews.it')
            limit: Maximum number of keywords to return
            db: Database region (it, uk, us, etc.)
        
        Returns:
            Dict with keyword data or None if error
        """
        try:
            print(f"\n[INFO] Fetching SEOZoom keywords for {domain}...")
            
            # Remove any existing protocol/www from input
            clean_domain = domain.replace('https://', '').replace('http://', '').replace('www.', '').strip()
            
            # Try different URL formats - both with and without www
            url_formats = [
                f"https://www.{clean_domain}",
                f"https://{clean_domain}",
                f"http://www.{clean_domain}",
                f"http://{clean_domain}"
            ]
            
            print(f"[INFO] Will try {len(url_formats)} URL variations...")
            
            for i, url_format in enumerate(url_formats, 1):
                print(f"\n[INFO] Attempt {i}/{len(url_formats)}: {url_format}")
                result = self._fetch_keywords_for_url(url_format, limit, db)
                if result and result.get('keywords'):
                    print(f"[OK] SUCCESS with URL format: {url_format}")
                    result['working_url'] = url_format
                    return result
            
            print(f"\n[ERROR] No keywords found for {domain} with any URL format")
            print(f"[INFO] Tried: {', '.join(url_formats)}")
            return None
            
        except Exception as e:
            print(f"[ERROR] Failed to get keywords: {str(e)}")
            return None
    
    def _fetch_keywords_for_url(self, url: str, limit: int, db: str) -> Optional[Dict]:
        """Fetch keywords for specific URL format"""
        try:
            # SEOZoom API v2 uses /urls/ endpoint with action parameter
            endpoint = f"{self.base_url}/urls/"
            
            # Try multiple actions - intentgap is known to work
            actions_to_try = ['intentgap', 'keywords']
            
            for action in actions_to_try:
                params = {
                    'api_key': self.api_key,
                    'action': action,
                    'url': url,
                    'db': db,
                    'limit': limit
                }
                
                print(f"[DEBUG] Calling: {endpoint}")
                print(f"[DEBUG] Params: action={action}, url={url}, db={db}, limit={limit}")
                
                response = requests.get(endpoint, params=params, timeout=self.timeout)
                
                print(f"[DEBUG] Status: {response.status_code}")
                
                if response.status_code == 200:
                data = response.json()
                print(f"[DEBUG] Response received: {json.dumps(data)[:300]}...")
                
                # SEOZoom returns data in different formats
                keywords = []
                
                # Try to extract keywords from response
                if isinstance(data, dict):
                    if 'keywords' in data:
                        keywords = data['keywords']
                    elif 'data' in data:
                        keywords = data['data']
                    elif 'results' in data:
                        keywords = data['results']
                elif isinstance(data, list):
                    keywords = data
                
                if keywords:
                    print(f"[OK] Found {len(keywords)} keywords")
                    return {
                        'domain': url,
                        'keywords': keywords,
                        'total': len(keywords),
                        'database': db,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    print(f"[WARN] No keywords in response structure")
                    return None
            
            elif response.status_code == 401:
                print(f"[ERROR] Authentication failed - check API key")
                return None
            elif response.status_code == 403:
                print(f"[ERROR] Access forbidden - API key might be invalid")
                return None
            elif response.status_code == 400:
                print(f"[ERROR] Bad request - check parameters")
                print(f"[DEBUG] Response: {response.text[:300]}")
                return None
            else:
                print(f"[WARN] Status {response.status_code}")
                print(f"[DEBUG] Response: {response.text[:300]}")
                return None
            
            print(f"[WARN] No working endpoint found for {url}")
            return None
                
        except Exception as e:
            print(f"[ERROR] Request failed: {str(e)}")
            return None
    
    def format_keywords_table(self, keywords_data: Dict) -> List[Dict]:
        """
        Format keywords data for display
        
        Returns:
            List of dicts with formatted keyword data
        """
        if not keywords_data or 'keywords' not in keywords_data:
            return []
        
        formatted = []
        for i, kw in enumerate(keywords_data['keywords'], 1):
            # Handle different data structures
            if isinstance(kw, dict):
                formatted.append({
                    'rank': i,
                    'keyword': kw.get('keyword', kw.get('kw', 'N/A')),
                    'search_volume': kw.get('search_volume', kw.get('volume', kw.get('searches', 0))),
                    'position': kw.get('position', kw.get('pos', kw.get('rank', 'N/A'))),
                    'traffic': kw.get('traffic', kw.get('visits', 0)),
                    'cpc': kw.get('cpc', kw.get('cost', 0)),
                    'competition': kw.get('competition', kw.get('comp', 'N/A')),
                    'url': kw.get('url', kw.get('page', 'N/A'))
                })
            elif isinstance(kw, str):
                # Simple keyword list
                formatted.append({
                    'rank': i,
                    'keyword': kw,
                    'search_volume': 'N/A',
                    'position': 'N/A',
                    'traffic': 'N/A',
                    'cpc': 'N/A',
                    'competition': 'N/A',
                    'url': 'N/A'
                })
        
        return formatted


def main():
    """Test SEOZoom keywords"""
    from config import SEOZOOM_API_KEY
    
    print("="*60)
    print("SEOZoom Keyword Analysis Test")
    print("="*60)
    
    seozoom = SEOZoomKeywords(SEOZOOM_API_KEY)
    
    # Test with triesteallnews.it
    keywords_data = seozoom.get_keywords('triesteallnews.it', limit=50)
    
    if keywords_data:
        print(f"\n{'='*60}")
        print(f"TOP KEYWORDS FOR TRIESTEALLNEWS.IT")
        print(f"{'='*60}")
        
        formatted = seozoom.format_keywords_table(keywords_data)
        
        if formatted:
            print(f"\n{'Rank':<6} {'Keyword':<30} {'Volume':<10} {'Position':<10}")
            print("-"*60)
            
            for kw in formatted[:20]:  # Show top 20
                print(f"{kw['rank']:<6} {str(kw['keyword']):<30} {str(kw['search_volume']):<10} {str(kw['position']):<10}")
        
        print(f"\nTotal keywords found: {len(formatted)}")
    else:
        print("\n[ERROR] Could not retrieve keywords")
        print("This could mean:")
        print("  1. API key is invalid or expired")
        print("  2. Domain not found in SEOZoom database")
        print("  3. API endpoint has changed")


if __name__ == "__main__":
    main()

