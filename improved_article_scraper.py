#!/usr/bin/env python3
"""
Improved Article Scraper for triesteallnews.it
Extracts REAL data where available and clearly marks estimated data
"""

import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import random
import re

@dataclass
class ImprovedArticleData:
    """Article data with clear distinction between real and estimated data"""
    # REAL DATA (extracted from website)
    title: str
    url: str
    publish_date: Optional[str] = None  # Real date from website
    author: Optional[str] = None  # Real author from website
    category: Optional[str] = None  # Real category from website
    
    # ESTIMATED DATA (not available from scraping)
    read_count_estimated: int = 0
    engagement_score_estimated: float = 0.0
    social_shares_estimated: int = 0
    comments_count_estimated: int = 0
    word_count_estimated: int = 0
    
    # METADATA
    is_real_data: bool = True  # True if scraped from website
    data_source: str = "scraped"  # "scraped", "estimated", or "mock"
    scrape_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class ImprovedArticleScraper:
    """
    Improved article scraper that extracts real data from triesteallnews.it
    """
    
    def __init__(self):
        self.base_url = "https://www.triesteallnews.it"
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        # Known categories
        self.categories = {
            'cronaca': 'Cronaca',
            'sport': 'Sport',
            'politica': 'Politica',
            'cultura': 'Cultura',
            'economia': 'Economia',
            'opinioni': 'Opinioni',
            'regione': 'Regione',
            'attualita': 'Attualità'
        }
    
    def scrape_articles(self, category: str = 'cronaca', limit: int = 10) -> List[ImprovedArticleData]:
        """
        Scrape real articles from a category page
        
        Args:
            category: Category to scrape (cronaca, sport, politica, etc.)
            limit: Maximum number of articles to return
            
        Returns:
            List of ImprovedArticleData with real data where available
        """
        articles = []
        
        try:
            url = f"{self.base_url}/{category}"
            print(f"\n[INFO] Scraping {url}...")
            
            response = self.scraper.get(url, timeout=15)
            
            if response.status_code != 200:
                print(f"[WARN] Page returned status {response.status_code}")
                return self._generate_fallback_articles(category, limit)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"[OK] Page loaded successfully")
            
            # Extract articles using the selectors we discovered
            articles = self._extract_articles_from_soup(soup, category, limit)
            
            if articles:
                print(f"[OK] Extracted {len(articles)} real articles")
                return articles
            else:
                print(f"[WARN] No articles found, using fallback")
                return self._generate_fallback_articles(category, limit)
                
        except Exception as e:
            print(f"[ERROR] Scraping failed: {str(e)}")
            return self._generate_fallback_articles(category, limit)
    
    def _extract_articles_from_soup(self, soup: BeautifulSoup, category: str, limit: int) -> List[ImprovedArticleData]:
        """Extract article data from parsed HTML"""
        articles = []
        found_urls = set()
        
        # Based on our testing, we know:
        # - h3 a elements contain article titles and URLs
        # - bookmark links (a[rel="bookmark"]) also contain articles
        # - date elements have datetime attributes with real dates
        # - author elements contain real author names
        
        # Find all article links
        article_links = soup.select('h3 a')
        
        if not article_links:
            # Try bookmark links as fallback
            article_links = soup.select('a[rel="bookmark"]')
        
        print(f"[INFO] Found {len(article_links)} potential article links")
        
        for link in article_links:
            if len(articles) >= limit:
                break
            
            # Get title and URL
            title = link.get_text(strip=True)
            url = link.get('href', '')
            
            # Skip if invalid or duplicate
            if not title or len(title) < 10 or url in found_urls:
                continue
            
            # Make URL absolute
            if url and not url.startswith('http'):
                url = url if url.startswith('http') else f"{self.base_url}{url}" if url.startswith('/') else f"{self.base_url}/{url}"
            
            found_urls.add(url)
            
            # Try to extract metadata from nearby elements
            parent = link.parent
            if parent:
                parent = parent.parent  # Go up one more level to get the container
            
            # Extract date
            publish_date = self._extract_date_from_element(parent if parent else link)
            
            # Extract author
            author = self._extract_author_from_element(parent if parent else link)
            
            # Create article with real data
            article = ImprovedArticleData(
                title=title,
                url=url,
                publish_date=publish_date,
                author=author,
                category=self.categories.get(category, category.capitalize()),
                # Estimated data (clearly marked)
                read_count_estimated=self._estimate_read_count(title, category, publish_date),
                engagement_score_estimated=self._estimate_engagement(title),
                social_shares_estimated=self._estimate_shares(category),
                comments_count_estimated=self._estimate_comments(category),
                word_count_estimated=random.randint(300, 800),
                # Metadata
                is_real_data=True,
                data_source="scraped"
            )
            
            articles.append(article)
            
            print(f"  [{len(articles)}] {title[:60]}...")
            print(f"      Date: {publish_date or 'N/A'} | Author: {author or 'Unknown'}")
        
        # Sort by estimated read count (highest first)
        articles.sort(key=lambda x: x.read_count_estimated, reverse=True)
        
        return articles[:limit]
    
    def _extract_date_from_element(self, element) -> Optional[str]:
        """Extract publication date from element or nearby elements"""
        if not element:
            return None
        
        try:
            # Look for time elements with datetime attribute
            time_elem = element.find('time', attrs={'datetime': True})
            if time_elem:
                datetime_str = time_elem.get('datetime')
                if datetime_str:
                    # Parse and format the date
                    try:
                        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                        return dt.strftime('%Y-%m-%d')
                    except:
                        pass
            
            # Look for date classes
            date_elem = element.find(class_=re.compile(r'date|time', re.I))
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                if date_text:
                    # Try to parse Italian dates (e.g., "3 Novembre 2025")
                    return self._parse_italian_date(date_text)
            
        except Exception:
            pass
        
        return None
    
    def _extract_author_from_element(self, element) -> Optional[str]:
        """Extract author from element or nearby elements"""
        if not element:
            return None
        
        try:
            # Look for author classes
            author_elem = element.find(class_=re.compile(r'author|byline|writer', re.I))
            if author_elem:
                author_text = author_elem.get_text(strip=True)
                # Clean up author text
                author_text = author_text.replace('di', '').replace('Di', '').replace('by', '').replace('By', '').strip()
                
                # Skip generic names
                if author_text and author_text.lower() not in ['redazione', 'staff', 'admin', '-']:
                    return author_text
            
        except Exception:
            pass
        
        return None
    
    def _parse_italian_date(self, date_str: str) -> Optional[str]:
        """Parse Italian date format (e.g., '3 Novembre 2025')"""
        try:
            # Italian month names
            months = {
                'gennaio': '01', 'febbraio': '02', 'marzo': '03', 'aprile': '04',
                'maggio': '05', 'giugno': '06', 'luglio': '07', 'agosto': '08',
                'settembre': '09', 'ottobre': '10', 'novembre': '11', 'dicembre': '12'
            }
            
            # Extract day, month, year
            parts = date_str.lower().split()
            if len(parts) >= 3:
                day = parts[0]
                month_name = parts[1]
                year = parts[2]
                
                if month_name in months:
                    month = months[month_name]
                    return f"{year}-{month}-{day.zfill(2)}"
        except:
            pass
        
        return None
    
    def _estimate_read_count(self, title: str, category: str, date: Optional[str]) -> int:
        """
        Estimate read count based on content analysis
        NOTE: This is ESTIMATED data, not real traffic statistics
        """
        # Base reads by category
        base_reads = {
            'cronaca': 1200,
            'sport': 800,
            'politica': 1000,
            'cultura': 600,
            'economia': 700,
            'opinioni': 500
        }
        
        base = base_reads.get(category, 600)
        
        # Adjust for keywords in title
        title_lower = title.lower()
        if any(word in title_lower for word in ['trieste', 'emergenza', 'allarme', 'incidente']):
            base *= 1.3
        
        # Add randomness
        variation = random.uniform(0.7, 1.3)
        estimated = int(base * variation)
        
        return estimated
    
    def _estimate_engagement(self, title: str) -> float:
        """Estimate engagement score (1-10)"""
        base_score = 7.0
        
        # Adjust based on title length (optimal 50-70 chars)
        if 50 <= len(title) <= 70:
            base_score += 1.0
        
        # Add randomness
        variation = random.uniform(-0.5, 0.5)
        score = base_score + variation
        
        return round(min(10.0, max(1.0, score)), 1)
    
    def _estimate_shares(self, category: str) -> int:
        """Estimate social shares"""
        base_shares = {
            'cronaca': 45,
            'sport': 35,
            'politica': 40,
            'cultura': 25
        }
        
        base = base_shares.get(category, 30)
        return random.randint(int(base * 0.5), int(base * 1.5))
    
    def _estimate_comments(self, category: str) -> int:
        """Estimate comments count"""
        base_comments = {
            'cronaca': 25,
            'sport': 20,
            'politica': 35,
            'cultura': 15
        }
        
        base = base_comments.get(category, 20)
        return random.randint(int(base * 0.3), int(base * 1.2))
    
    def _generate_fallback_articles(self, category: str, limit: int) -> List[ImprovedArticleData]:
        """Generate fallback articles when scraping fails"""
        print(f"[WARN] Using fallback data for {category}")
        
        # Generic article templates
        templates = [
            f"Notizie importanti di {category} a Trieste",
            f"Ultime novità dalla sezione {category}",
            f"Aggiornamenti {category} dalla redazione",
        ]
        
        articles = []
        for i in range(min(limit, len(templates))):
            article = ImprovedArticleData(
                title=templates[i],
                url=f"{self.base_url}/{category}/fallback-{i+1}",
                publish_date=datetime.now().strftime('%Y-%m-%d'),
                author="Redazione",
                category=self.categories.get(category, category.capitalize()),
                read_count_estimated=random.randint(300, 800),
                engagement_score_estimated=round(random.uniform(6.0, 8.0), 1),
                social_shares_estimated=random.randint(15, 40),
                comments_count_estimated=random.randint(5, 20),
                word_count_estimated=random.randint(300, 600),
                is_real_data=False,
                data_source="fallback"
            )
            articles.append(article)
        
        return articles
    
    def scrape_multiple_categories(self, categories: List[str] = None, articles_per_category: int = 5) -> List[ImprovedArticleData]:
        """Scrape articles from multiple categories"""
        if categories is None:
            categories = ['cronaca', 'sport', 'politica']
        
        all_articles = []
        
        for category in categories:
            print(f"\n{'='*80}")
            print(f"SCRAPING CATEGORY: {category.upper()}")
            print(f"{'='*80}")
            
            articles = self.scrape_articles(category, articles_per_category)
            all_articles.extend(articles)
        
        # Sort all articles by estimated read count
        all_articles.sort(key=lambda x: x.read_count_estimated, reverse=True)
        
        return all_articles
    
    def print_article_report(self, articles: List[ImprovedArticleData]):
        """Print a detailed report of scraped articles"""
        print(f"\n{'='*80}")
        print("ARTICLE SCRAPING REPORT")
        print(f"{'='*80}")
        
        real_count = sum(1 for a in articles if a.is_real_data)
        fallback_count = len(articles) - real_count
        
        print(f"\nTotal Articles: {len(articles)}")
        print(f"Real Data (scraped): {real_count}")
        print(f"Fallback Data: {fallback_count}")
        
        print(f"\n{'='*80}")
        print("TOP ARTICLES (by estimated read count)")
        print(f"{'='*80}")
        
        for i, article in enumerate(articles[:10], 1):
            print(f"\n{i}. {article.title}")
            print(f"   URL: {article.url}")
            print(f"   Date: {article.publish_date or 'N/A'} | Author: {article.author or 'Unknown'}")
            print(f"   Category: {article.category}")
            print(f"   Est. Reads: {article.read_count_estimated:,} | Engagement: {article.engagement_score_estimated}/10")
            print(f"   Data Source: {article.data_source.upper()} | Real Data: {'YES' if article.is_real_data else 'NO'}")


def main():
    """Test the improved scraper"""
    scraper = ImprovedArticleScraper()
    
    # Scrape multiple categories
    articles = scraper.scrape_multiple_categories(
        categories=['cronaca', 'sport', 'politica'],
        articles_per_category=5
    )
    
    # Print report
    scraper.print_article_report(articles)


if __name__ == "__main__":
    main()

