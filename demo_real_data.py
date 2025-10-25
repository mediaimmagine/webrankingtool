#!/usr/bin/env python3
"""
Demo Real Data
Shows you how the tool works with real API data
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("REAL DATA DEMO")
    print("=" * 60)
    print()
    print("This demo shows you how the tool works with real data")
    print()
    
    try:
        from web_ranking_tool import WebRankingTool
        
        # Create tool instance
        tool = WebRankingTool()
        
        print("Current Configuration:")
        print(f"- Mock Data Mode: {tool.use_mock_data}")
        print(f"- BuiltWith API: {'Configured' if tool.builtwith_api_key and tool.builtwith_api_key != 'YOUR_BUILTWITH_API_KEY_HERE' else 'Not configured'}")
        print(f"- Wappalyzer API: {'Configured' if tool.wappalyzer_api_key and tool.wappalyzer_api_key != 'YOUR_WAPPALYZER_API_KEY_HERE' else 'Not configured'}")
        print(f"- PageSpeed API: {'Configured' if tool.pagespeed_api_key and tool.pagespeed_api_key != 'YOUR_PAGESPEED_API_KEY_HERE' else 'Not configured'}")
        print()
        
        # Test with your sites
        test_sites = ["triesteallnews.it", "triesteprima.it", "triestecafe.it"]
        
        print("Testing with your sites:")
        for site in test_sites:
            print(f"- {site}")
        print()
        
        print("Analyzing websites...")
        print()
        
        # Analyze each site
        for site in test_sites:
            print(f"Analyzing {site}...")
            results = tool.compare_websites([site])
            
            if results and site in results:
                domain_results = results[site]
                print(f"Found {len(domain_results)} data sources:")
                
                for i, metrics in enumerate(domain_results, 1):
                    data_type = "REAL DATA" if not tool.use_mock_data else "MOCK DATA"
                    print(f"  {i}. {metrics.data_source} ({data_type})")
                    print(f"     - Global Rank: {metrics.global_rank:,}" if metrics.global_rank else "     - Global Rank: N/A")
                    print(f"     - Monthly Visits: {metrics.monthly_visits:,}" if metrics.monthly_visits else "     - Monthly Visits: N/A")
                    print(f"     - Bounce Rate: {metrics.bounce_rate}%" if metrics.bounce_rate else "     - Bounce Rate: N/A")
                    print()
            else:
                print(f"No results for {site}")
                print()
        
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print()
        
        if tool.use_mock_data:
            print("Currently using MOCK DATA (simulated data)")
            print("To get REAL DATA:")
            print("1. Get free API key: .\\get_builtwith_key.bat")
            print("2. Add API key: .\\add_api_key.bat")
            print("3. Test setup: .\\test_api.bat")
        else:
            has_real_apis = any([
                tool.builtwith_api_key and tool.builtwith_api_key != 'YOUR_BUILTWITH_API_KEY_HERE',
                tool.wappalyzer_api_key and tool.wappalyzer_api_key != 'YOUR_WAPPALYZER_API_KEY_HERE',
                tool.pagespeed_api_key and tool.pagespeed_api_key != 'YOUR_PAGESPEED_API_KEY_HERE'
            ])
            
            if has_real_apis:
                print("SUCCESS: You have real API keys configured!")
                print("The tool is using REAL DATA from APIs.")
            else:
                print("WARNING: No real API keys configured.")
                print("The tool is using improved mock data.")
                print("To get real data: .\\get_builtwith_key.bat")
        
        print()
        print("Next steps:")
        print("1. Run: .\\run_gui.bat")
        print("2. Analyze your websites")
        print("3. See the difference between mock and real data")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()












































