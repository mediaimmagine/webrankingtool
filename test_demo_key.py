#!/usr/bin/env python3
"""
Test Demo API Key
Shows you how real data works with a demo
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("DEMO: REAL DATA vs MOCK DATA")
    print("=" * 60)
    print()
    print("This demo shows you the difference between:")
    print("- MOCK DATA (simulated, not real)")
    print("- REAL DATA (actual website data from APIs)")
    print()
    
    try:
        from web_ranking_tool import WebRankingTool
        
        # Test with mock data
        print("1. TESTING WITH MOCK DATA:")
        print("-" * 40)
        tool_mock = WebRankingTool()
        tool_mock.use_mock_data = True
        
        results_mock = tool_mock.compare_websites(["triesteallnews.it"])
        if results_mock and "triesteallnews.it" in results_mock:
            metrics = results_mock["triesteallnews.it"][0]
            print(f"Domain: {metrics.domain}")
            print(f"Data Source: {metrics.data_source} (MOCK DATA)")
            print(f"Global Rank: {metrics.global_rank:,}")
            print(f"Monthly Visits: {metrics.monthly_visits:,}")
            print(f"Bounce Rate: {metrics.bounce_rate}%")
        
        print()
        print("2. TESTING WITH REAL DATA MODE:")
        print("-" * 40)
        tool_real = WebRankingTool()
        tool_real.use_mock_data = False
        
        results_real = tool_real.compare_websites(["triesteallnews.it"])
        if results_real and "triesteallnews.it" in results_real:
            metrics = results_real["triesteallnews.it"][0]
            print(f"Domain: {metrics.domain}")
            print(f"Data Source: {metrics.data_source} (REAL DATA MODE)")
            print(f"Global Rank: {metrics.global_rank:,}")
            print(f"Monthly Visits: {metrics.monthly_visits:,}")
            print(f"Bounce Rate: {metrics.bounce_rate}%")
        
        print()
        print("=" * 60)
        print("WHAT'S THE DIFFERENCE?")
        print("=" * 60)
        print()
        print("MOCK DATA:")
        print("- Generated algorithmically")
        print("- Same values every time")
        print("- Not based on real website performance")
        print("- Good for testing and demos")
        print()
        print("REAL DATA (with API key):")
        print("- Actual website analytics")
        print("- Live data from APIs")
        print("- Changes based on real performance")
        print("- Professional-grade insights")
        print()
        print("=" * 60)
        print("TO GET REAL DATA:")
        print("=" * 60)
        print()
        print("1. Get free API key: .\\get_builtwith_key.bat")
        print("2. Add API key: .\\add_api_key.bat")
        print("3. Test setup: .\\test_api.bat")
        print("4. Use tool: .\\run_gui.bat")
        print()
        print("Total time: 5 minutes")
        print("Total cost: $0")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

