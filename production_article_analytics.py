#!/usr/bin/env python3
"""
Production Article Analytics System
Combines WordPress API + Cloudflare Analytics for complete, accurate data

Data Flow:
1. Fetch articles from WordPress REST API (real metadata)
2. Fetch traffic data from Cloudflare Analytics GraphQL API (real visit counts)
3. Match articles with traffic data by URL
4. Return complete article analytics with real data
"""

import requests
import json
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import re

@dataclass
class ProductionArticleData:
    """Complete article data with clear data source indicators"""
    # Article Metadata (from WordPress API)
    id: int
    title: str
    url: str
    slug: str
    publish_date: str
    modified_date: str
    author_id: int
    author_name: str
    category_ids: List[int]
    category_names: List[str]
    excerpt: str
    word_count: int
    
    # Traffic Data (from Cloudflare Analytics)
    page_views: Optional[int] = None  # Real data from Cloudflare
    unique_visitors: Optional[int] = None  # Real data from Cloudflare
    
    # Data Source Tracking
    has_real_traffic_data: bool = False
    data_source: str = "wordpress_api"  # "wordpress_api", "cloudflare_analytics", or "hybrid"
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


class ProductionArticleAnalytics:
    """
    Production-ready article analytics combining WordPress API and Cloudflare Analytics
    """
    
    def __init__(self, 
                 wordpress_base_url: str,
                 wordpress_client_id: str,
                 wordpress_client_secret: str,
                 cloudflare_api_token: str,
                 cloudflare_zone_id: str):
        
        # WordPress API Configuration
        self.wordpress_base_url = wordpress_base_url.rstrip('/')
        self.wordpress_api_url = f"{self.wordpress_base_url}/wp-json/wp/v2"
        self.wordpress_client_id = wordpress_client_id
        self.wordpress_client_secret = wordpress_client_secret
        
        # WordPress API Headers (OAuth)
        credentials = f"{wordpress_client_id}:{wordpress_client_secret}"
        token = base64.b64encode(credentials.encode()).decode()
        self.wordpress_headers = {
            'Authorization': f'Basic {token}',
            'Accept': 'application/json',
            'User-Agent': 'ProductionArticleAnalytics/1.0'
        }
        
        # Cloudflare API Configuration
        self.cloudflare_api_token = cloudflare_api_token
        self.cloudflare_zone_id = cloudflare_zone_id
        self.cloudflare_graphql_url = "https://api.cloudflare.com/client/v4/graphql"
        self.cloudflare_headers = {
            'Authorization': f'Bearer {cloudflare_api_token}',
            'Content-Type': 'application/json'
        }
        
        print(f"[INIT] Production Article Analytics System")
        print(f"  WordPress: {self.wordpress_base_url}")
        print(f"  Cloudflare Zone: {cloudflare_zone_id}")
    
    def get_articles(self, 
                     days_back: int = 7, 
                     per_page: int = 20,
                     orderby: str = 'date') -> List[ProductionArticleData]:
        """
        Get articles with complete data from WordPress API + Cloudflare Analytics
        
        Args:
            days_back: How many days of articles to fetch
            per_page: Articles per API request
            orderby: Sort order ('date', 'modified', 'title')
        
        Returns:
            List of ProductionArticleData with real traffic data where available
        """
        print(f"\n{'='*80}")
        print(f"FETCHING ARTICLES (Last {days_back} days)")
        print(f"{'='*80}")
        
        # Step 1: Get articles from WordPress API
        print(f"\n[STEP 1] Fetching articles from WordPress API...")
        wordpress_articles = self._fetch_wordpress_articles(days_back, per_page, orderby)
        
        if not wordpress_articles:
            print(f"[ERROR] No articles fetched from WordPress API")
            return []
        
        print(f"[OK] Fetched {len(wordpress_articles)} articles from WordPress")
        
        # Step 2: Get traffic data from Cloudflare Analytics
        print(f"\n[STEP 2] Fetching traffic data from Cloudflare Analytics...")
        cloudflare_traffic = self._fetch_cloudflare_analytics(days_back)
        
        if cloudflare_traffic:
            print(f"[OK] Fetched traffic data for {len(cloudflare_traffic)} URLs")
        else:
            print(f"[WARN] Could not fetch Cloudflare Analytics data")
        
        # Step 3: Merge WordPress articles with Cloudflare traffic data
        print(f"\n[STEP 3] Merging article data with traffic statistics...")
        complete_articles = self._merge_article_data(wordpress_articles, cloudflare_traffic)
        
        # Summary
        real_traffic_count = sum(1 for a in complete_articles if a.has_real_traffic_data)
        print(f"\n[SUMMARY]")
        print(f"  Total Articles: {len(complete_articles)}")
        print(f"  With Real Traffic Data: {real_traffic_count}")
        print(f"  Without Traffic Data: {len(complete_articles) - real_traffic_count}")
        
        return complete_articles
    
    def _fetch_wordpress_articles(self, days_back: int, per_page: int, orderby: str) -> List[Dict]:
        """Fetch articles from WordPress REST API"""
        articles = []
        page = 1
        date_filter = (datetime.now() - timedelta(days=days_back)).isoformat()
        
        try:
            while True:
                params = {
                    'per_page': per_page,
                    'page': page,
                    'orderby': orderby,
                    'order': 'desc',
                    '_embed': True,  # Include author and category data
                    'after': date_filter  # Only articles after this date
                }
                
                response = requests.get(
                    f"{self.wordpress_api_url}/posts",
                    headers=self.wordpress_headers,
                    params=params,
                    timeout=15
                )
                
                if response.status_code == 200:
                    page_articles = response.json()
                    
                    if not page_articles:
                        break  # No more articles
                    
                    articles.extend(page_articles)
                    
                    # Check if there are more pages
                    total_pages = int(response.headers.get('X-WP-TotalPages', 1))
                    
                    print(f"  Fetched page {page}/{total_pages} ({len(page_articles)} articles)")
                    
                    if page >= total_pages:
                        break
                    
                    page += 1
                    
                else:
                    print(f"  [ERROR] WordPress API returned status {response.status_code}")
                    break
                    
        except Exception as e:
            print(f"  [ERROR] WordPress API request failed: {str(e)}")
        
        return articles
    
    def _fetch_cloudflare_analytics(self, days_back: int) -> Dict[str, Dict]:
        """
        Fetch traffic data from Cloudflare GraphQL Analytics API
        
        Returns:
            Dict mapping URL paths to traffic data
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for GraphQL (YYYY-MM-DD)
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # GraphQL query for page views by URL
            # Note: Using simplified schema compatible with Cloudflare Pro
            query = """
            query GetPageViews($zoneTag: string, $startDate: string, $endDate: string) {
              viewer {
                zones(filter: {zoneTag: $zoneTag}) {
                  httpRequests1dGroups(
                    filter: {
                      date_geq: $startDate
                      date_lt: $endDate
                    }
                    limit: 10000
                  ) {
                    dimensions {
                      clientRequestPath
                    }
                    sum {
                      pageViews
                    }
                    uniq {
                      uniques
                    }
                  }
                }
              }
            }
            """
            
            # Variables for the query
            variables = {
                "zoneTag": self.cloudflare_zone_id,
                "startDate": start_date_str,
                "endDate": end_date_str
            }
            
            # Make GraphQL request
            payload = {
                "query": query,
                "variables": variables
            }
            
            response = requests.post(
                self.cloudflare_graphql_url,
                headers=self.cloudflare_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for errors
                if 'errors' in data:
                    print(f"  [ERROR] Cloudflare GraphQL errors:")
                    for error in data['errors']:
                        print(f"    - {error.get('message', 'Unknown error')}")
                    return {}
                
                # Extract traffic data
                traffic_data = {}
                
                try:
                    zones = data.get('data', {}).get('viewer', {}).get('zones', [])
                    if zones:
                        groups = zones[0].get('httpRequests1dGroups', [])
                        
                        for group in groups:
                            dimensions = group.get('dimensions', {})
                            path = dimensions.get('clientRequestPath', '')
                            
                            # Sum metrics
                            pageviews = group.get('sum', {}).get('pageViews', 0)
                            uniques = group.get('uniq', {}).get('uniques', 0)
                            
                            if path and pageviews > 0:
                                traffic_data[path] = {
                                    'page_views': pageviews,
                                    'unique_visitors': uniques
                                }
                        
                        print(f"  [OK] Processed {len(traffic_data)} URLs with traffic data")
                    else:
                        print(f"  [WARN] No zones data in response")
                        
                except Exception as e:
                    print(f"  [ERROR] Failed to parse Cloudflare response: {str(e)}")
                
                return traffic_data
                
            else:
                print(f"  [ERROR] Cloudflare API returned status {response.status_code}")
                print(f"  Response: {response.text[:200]}")
                return {}
                
        except Exception as e:
            print(f"  [ERROR] Cloudflare Analytics request failed: {str(e)}")
            return {}
    
    def _merge_article_data(self, 
                           wordpress_articles: List[Dict], 
                           cloudflare_traffic: Dict[str, Dict]) -> List[ProductionArticleData]:
        """
        Merge WordPress article data with Cloudflare traffic data
        
        Args:
            wordpress_articles: List of articles from WordPress API
            cloudflare_traffic: Dict mapping URL paths to traffic data
        
        Returns:
            List of complete ProductionArticleData objects
        """
        complete_articles = []
        
        for wp_article in wordpress_articles:
            try:
                # Extract WordPress data
                article_id = wp_article.get('id', 0)
                title = wp_article.get('title', {}).get('rendered', 'Untitled')
                url = wp_article.get('link', '')
                slug = wp_article.get('slug', '')
                publish_date = wp_article.get('date', '')[:10]  # YYYY-MM-DD
                modified_date = wp_article.get('modified', '')[:10]
                
                # Extract author data from embedded
                author_id = wp_article.get('author', 0)
                author_name = 'Unknown'
                if '_embedded' in wp_article and 'author' in wp_article['_embedded']:
                    author_data = wp_article['_embedded']['author'][0]
                    author_name = author_data.get('name', 'Unknown')
                
                # Extract category data
                category_ids = wp_article.get('categories', [])
                category_names = []
                if '_embedded' in wp_article and 'wp:term' in wp_article['_embedded']:
                    terms = wp_article['_embedded']['wp:term']
                    if terms and len(terms) > 0:
                        category_names = [cat.get('name', '') for cat in terms[0]]
                
                # Extract excerpt and content
                excerpt_html = wp_article.get('excerpt', {}).get('rendered', '')
                excerpt = self._strip_html(excerpt_html)
                
                # Estimate word count from content
                content_html = wp_article.get('content', {}).get('rendered', '')
                content_text = self._strip_html(content_html)
                word_count = len(content_text.split()) if content_text else 0
                
                # Extract URL path for matching with Cloudflare data
                url_path = self._extract_url_path(url)
                
                # Check if we have traffic data for this URL
                traffic_data = cloudflare_traffic.get(url_path)
                
                if traffic_data:
                    # We have real traffic data!
                    article = ProductionArticleData(
                        id=article_id,
                        title=title,
                        url=url,
                        slug=slug,
                        publish_date=publish_date,
                        modified_date=modified_date,
                        author_id=author_id,
                        author_name=author_name,
                        category_ids=category_ids,
                        category_names=category_names,
                        excerpt=excerpt[:200],
                        word_count=word_count,
                        page_views=traffic_data['page_views'],
                        unique_visitors=traffic_data['unique_visitors'],
                        has_real_traffic_data=True,
                        data_source="hybrid"  # WordPress + Cloudflare
                    )
                else:
                    # No traffic data, WordPress metadata only
                    article = ProductionArticleData(
                        id=article_id,
                        title=title,
                        url=url,
                        slug=slug,
                        publish_date=publish_date,
                        modified_date=modified_date,
                        author_id=author_id,
                        author_name=author_name,
                        category_ids=category_ids,
                        category_names=category_names,
                        excerpt=excerpt[:200],
                        word_count=word_count,
                        page_views=None,  # No data available
                        unique_visitors=None,
                        has_real_traffic_data=False,
                        data_source="wordpress_api"  # Only WordPress data
                    )
                
                complete_articles.append(article)
                
            except Exception as e:
                print(f"  [WARN] Failed to process article {wp_article.get('id', '?')}: {str(e)}")
                continue
        
        return complete_articles
    
    def _extract_url_path(self, url: str) -> str:
        """Extract the path component from a URL for matching with Cloudflare data"""
        try:
            # Remove protocol and domain
            # Example: "https://www.triesteallnews.it/2025/11/article-title/" → "/2025/11/article-title/"
            if '://' in url:
                url = url.split('://', 1)[1]
            if '/' in url:
                path = '/' + '/'.join(url.split('/')[1:])
                return path
            return url
        except:
            return url
    
    def _strip_html(self, html: str) -> str:
        """Remove HTML tags from text"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html).strip()
    
    def get_articles_sorted_by_traffic(self, days_back: int = 7, limit: int = 20) -> List[ProductionArticleData]:
        """
        Get articles sorted by traffic (real data first, then by page views)
        
        Args:
            days_back: How many days of articles to fetch
            limit: Maximum number of articles to return
        
        Returns:
            Sorted list of articles
        """
        articles = self.get_articles(days_back=days_back, per_page=limit)
        
        # Sort: Articles with real traffic data first (by page views desc), then others by date
        articles_with_traffic = [a for a in articles if a.has_real_traffic_data]
        articles_without_traffic = [a for a in articles if not a.has_real_traffic_data]
        
        articles_with_traffic.sort(key=lambda x: x.page_views or 0, reverse=True)
        articles_without_traffic.sort(key=lambda x: x.publish_date, reverse=True)
        
        return articles_with_traffic + articles_without_traffic
    
    def export_to_dict(self, articles: List[ProductionArticleData]) -> List[Dict]:
        """Export articles to dictionary format for JSON/CSV export"""
        return [
            {
                'id': a.id,
                'title': a.title,
                'url': a.url,
                'publish_date': a.publish_date,
                'author': a.author_name,
                'categories': ', '.join(a.category_names),
                'page_views': a.page_views if a.has_real_traffic_data else 'N/A',
                'unique_visitors': a.unique_visitors if a.has_real_traffic_data else 'N/A',
                'word_count': a.word_count,
                'has_real_traffic': 'Yes' if a.has_real_traffic_data else 'No',
                'data_source': a.data_source
            }
            for a in articles
        ]
    
    def print_article_report(self, articles: List[ProductionArticleData], limit: int = 10):
        """Print a formatted report of articles"""
        print(f"\n{'='*80}")
        print(f"ARTICLE ANALYTICS REPORT")
        print(f"{'='*80}")
        
        articles_with_traffic = [a for a in articles if a.has_real_traffic_data]
        articles_without_traffic = [a for a in articles if not a.has_real_traffic_data]
        
        print(f"\nSummary:")
        print(f"  Total Articles: {len(articles)}")
        print(f"  With Real Traffic Data: {len(articles_with_traffic)}")
        print(f"  Without Traffic Data: {len(articles_without_traffic)}")
        
        if articles_with_traffic:
            total_views = sum(a.page_views for a in articles_with_traffic if a.page_views)
            avg_views = total_views / len(articles_with_traffic) if articles_with_traffic else 0
            print(f"  Total Page Views: {total_views:,}")
            print(f"  Average Views per Article: {avg_views:,.0f}")
        
        print(f"\n{'='*80}")
        print(f"TOP ARTICLES (showing first {limit})")
        print(f"{'='*80}")
        
        for i, article in enumerate(articles[:limit], 1):
            print(f"\n{i}. {article.title[:70]}")
            print(f"   URL: {article.url}")
            print(f"   Date: {article.publish_date} | Author: {article.author_name}")
            print(f"   Categories: {', '.join(article.category_names) if article.category_names else 'None'}")
            
            if article.has_real_traffic_data:
                print(f"   [REAL DATA] Page Views: {article.page_views:,} | Unique Visitors: {article.unique_visitors:,}")
            else:
                print(f"   [NO TRAFFIC DATA] (Article too new or not in Cloudflare Analytics)")
            
            print(f"   Word Count: {article.word_count} | Source: {article.data_source}")


def main():
    """Test the production analytics system"""
    from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID
    
    # Load WordPress OAuth credentials
    try:
        with open('miniorange_oauth_config.json', 'r') as f:
            oauth_config = json.load(f)
            wordpress_base_url = oauth_config['base_url']
            client_id = oauth_config['client_id']
            client_secret = oauth_config['client_secret']
    except FileNotFoundError:
        print("[ERROR] miniorange_oauth_config.json not found")
        print("[INFO] Run test_miniorange_oauth.py first to save credentials")
        return
    
    # Create analytics instance
    analytics = ProductionArticleAnalytics(
        wordpress_base_url=wordpress_base_url,
        wordpress_client_id=client_id,
        wordpress_client_secret=client_secret,
        cloudflare_api_token=CLOUDFLARE_API_TOKEN,
        cloudflare_zone_id=CLOUDFLARE_ZONE_ID
    )
    
    # Get articles with traffic data
    articles = analytics.get_articles_sorted_by_traffic(days_back=7, limit=20)
    
    # Try to fetch Google Analytics data if configured
    try:
        from google_analytics_fetcher import GoogleAnalyticsFetcher, load_config
        
        ga_config = load_config()
        if ga_config:
            print(f"\n[INFO] Google Analytics API configured - fetching real traffic data...")
            ga_fetcher = GoogleAnalyticsFetcher(
                credentials_file=ga_config['credentials_file'],
                property_id=ga_config['property_id']
            )
            
            # Get GA traffic data
            ga_traffic = ga_fetcher.get_page_views_by_url(days_back=7)
            
            if ga_traffic:
                print(f"[OK] Google Analytics data retrieved - updating articles...")
                
                # Update articles with GA data
                for article in articles:
                    url_path = analytics._extract_url_path(article.url)
                    if url_path in ga_traffic:
                        ga_data = ga_traffic[url_path]
                        article.page_views = ga_data.get('page_views')
                        article.unique_visitors = ga_data.get('unique_users')
                        article.has_real_traffic_data = True
                        article.data_source = "hybrid"  # WordPress + GA
                
                # Re-sort by real traffic
                articles.sort(key=lambda x: x.page_views or 0, reverse=True)
                print(f"[OK] Articles updated with Google Analytics data!")
        else:
            print(f"\n[INFO] Google Analytics API not yet configured")
            print(f"[INFO] Run 'python google_analytics_setup.py' to set up API access")
            
    except ImportError:
        print(f"\n[INFO] Google Analytics library not installed")
        print(f"[INFO] Run: pip install google-analytics-data")
    except Exception as e:
        print(f"\n[WARN] Could not fetch Google Analytics data: {str(e)}")
        print(f"[INFO] Using WordPress data only")
    
    # Print report
    analytics.print_article_report(articles, limit=10)
    
    # Export to JSON
    articles_dict = analytics.export_to_dict(articles)
    with open('production_articles_with_traffic.json', 'w', encoding='utf-8') as f:
        json.dump(articles_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\n[INFO] Data exported to: production_articles_with_traffic.json")


if __name__ == "__main__":
    main()

