#!/usr/bin/env python3
"""
Test script for real article data fetching from triesteallnews.it
"""

from article_analytics import ArticleAnalyticsEngine

def test_real_articles():
    print("Testing Real Article Data Fetching")
    print("=" * 60)
    
    engine = ArticleAnalyticsEngine()
    
    # Test daily articles
    print("\nFetching Daily Most Read Articles...")
    daily_articles = engine.get_most_read_articles("daily", 10)
    
    print(f"\nFound {len(daily_articles)} daily articles:")
    print("-" * 60)
    
    for i, article in enumerate(daily_articles, 1):
        is_real = "triesteallnews.it" in article.url
        data_type = "REAL" if is_real else "MOCK"
        
        print(f"{i:2d}. [{data_type}] {article.title[:65]}{'...' if len(article.title) > 65 else ''}")
        print(f"    Category: {article.category} | Author: {article.author} | Reads: {article.read_count:,}")
        print(f"    URL: {article.url}")
        print()
    
    # Test analytics generation
    print("Generating Article Analytics...")
    analytics = engine.get_article_analytics("daily")
    
    print(f"\nAnalytics Summary:")
    print(f"   Total Articles: {analytics.total_articles}")
    print(f"   Total Reads: {analytics.total_reads:,}")
    print(f"   Avg Engagement: {analytics.engagement_metrics['average_engagement_score']:.1f}/10")
    print(f"   Total Social Shares: {analytics.engagement_metrics['total_social_shares']:,}")
    print(f"   Total Comments: {analytics.engagement_metrics['total_comments']:,}")
    
    print(f"\nCategory Breakdown:")
    for category, reads in list(analytics.category_breakdown.items())[:5]:
        print(f"   {category}: {reads:,} reads")
    
    print(f"\nTop Authors:")
    for author, reads in list(analytics.author_performance.items())[:5]:
        print(f"   {author}: {reads:,} reads")
    
    # Count real vs mock articles
    real_count = sum(1 for article in daily_articles if "triesteallnews.it" in article.url)
    mock_count = len(daily_articles) - real_count
    
    print(f"\nData Source Summary:")
    print(f"   Real Articles: {real_count}")
    print(f"   Mock Articles: {mock_count}")
    print(f"   Success Rate: {real_count/len(daily_articles)*100:.1f}%")
    
    print("\n" + "=" * 60)
    print("Real article data fetching test completed!")

if __name__ == "__main__":
    test_real_articles()
