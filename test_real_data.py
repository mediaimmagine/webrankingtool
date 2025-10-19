#!/usr/bin/env python3
"""
Test script to verify the tool is using real PageSpeed data
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_ranking_tool import WebRankingTool

def test_real_data():
    """Test if the tool is using real data"""
    print("Testing WebRankingTool with real data...")
    
    # Initialize the tool
    tool = WebRankingTool()
    
    print(f"Mock data enabled: {tool.use_mock_data}")
    print(f"PageSpeed API key: {'Set' if tool.pagespeed_api_key else 'Not set'}")
    print(f"SEOZoom API key: {'Set' if tool.seozoom_api_key else 'Not set'}")
    print(f"BuiltWith API key: {'Set' if tool.builtwith_api_key else 'Not set'}")
    print(f"Wappalyzer API key: {'Set' if tool.wappalyzer_api_key else 'Not set'}")
    
    # Test with one domain
    test_domain = "triesteallnews.it"
    print(f"\nTesting with domain: {test_domain}")
    
    try:
        results = tool.compare_websites([test_domain])
        
        if test_domain in results:
            metrics_list = results[test_domain]
            print(f"\nFound {len(metrics_list)} data sources:")
            
            for i, metrics in enumerate(metrics_list):
                print(f"\nData Source {i+1}:")
                print(f"  Domain: {metrics.domain}")
                print(f"  Data Source: {metrics.data_source}")
                print(f"  Global Rank: {metrics.global_rank}")
                print(f"  Monthly Visits: {metrics.monthly_visits}")
                print(f"  Bounce Rate: {metrics.bounce_rate}")
                print(f"  Average Visit Duration: {metrics.avg_visit_duration}")
                print(f"  Pages per Visit: {metrics.pages_per_visit}")
                print(f"  Traffic Sources: {metrics.traffic_sources}")
                print(f"  Top Countries: {metrics.top_countries}")
        else:
            print("No results found!")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_data()
