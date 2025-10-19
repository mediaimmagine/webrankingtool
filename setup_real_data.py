#!/usr/bin/env python3
"""
Real Data Setup Wizard
Helps configure the tool to use real website data
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("REAL DATA SETUP WIZARD")
    print("=" * 60)
    print()
    print("This wizard will help you configure the tool to use")
    print("REAL website data instead of mock data.")
    print()
    print("Total cost: $0/month using FREE APIs!")
    print()
    
    # Show current configuration
    try:
        from config import USE_MOCK_DATA, BUILTWITH_API_KEY, WAPPALYZER_API_KEY, PAGESPEED_API_KEY
        print("Current Configuration:")
        print(f"- Mock Data Mode: {USE_MOCK_DATA}")
        print(f"- BuiltWith API: {'Configured' if BUILTWITH_API_KEY and BUILTWITH_API_KEY != 'YOUR_BUILTWITH_API_KEY_HERE' else 'Not configured'}")
        print(f"- Wappalyzer API: {'Configured' if WAPPALYZER_API_KEY and WAPPALYZER_API_KEY != 'YOUR_WAPPALYZER_API_KEY_HERE' else 'Not configured'}")
        print(f"- PageSpeed API: {'Configured' if PAGESPEED_API_KEY and PAGESPEED_API_KEY != 'YOUR_PAGESPEED_API_KEY_HERE' else 'Not configured'}")
        print()
    except ImportError:
        print("Error: Could not load configuration")
        return
    
    # Check if any APIs are configured
    has_apis = any([
        BUILTWITH_API_KEY and BUILTWITH_API_KEY != 'YOUR_BUILTWITH_API_KEY_HERE',
        WAPPALYZER_API_KEY and WAPPALYZER_API_KEY != 'YOUR_WAPPALYZER_API_KEY_HERE',
        PAGESPEED_API_KEY and PAGESPEED_API_KEY != 'YOUR_PAGESPEED_API_KEY_HERE'
    ])
    
    if has_apis:
        print("SUCCESS: You have API keys configured!")
        print("The tool is ready to use real data.")
        print()
        print("Next steps:")
        print("1. Run: .\\test_api.bat")
        print("2. Run: .\\run_gui.bat")
        print("3. Analyze websites to see real data!")
    else:
        print("WARNING: No API keys configured yet.")
        print()
        print("To get real data, you need to:")
        print("1. Get a free API key from one of these services:")
        print("   - BuiltWith: https://api.builtwith.com/ (500 free requests/month)")
        print("   - Wappalyzer: https://www.wappalyzer.com/api/ (1,000 free requests/month)")
        print("   - PageSpeed: https://console.cloud.google.com/ (25,000 free requests/day)")
        print()
        print("2. Edit config.py and add your API key")
        print("3. Run this wizard again")
        print()
        print("For detailed instructions, run: .\\GET_REAL_DATA.bat")
    
    print()
    print("=" * 60)
    print("QUICK TEST")
    print("=" * 60)
    print()
    
    # Test current setup
    try:
        from web_ranking_tool import WebRankingTool
        tool = WebRankingTool()
        
        print("Testing with a sample website...")
        print("Domain: google.com")
        print()
        
        # Test with a well-known domain
        results = tool.compare_websites(["google.com"])
        
        if results and "google.com" in results:
            domain_results = results["google.com"]
            print(f"Found {len(domain_results)} data sources:")
            print()
            
            for i, metrics in enumerate(domain_results, 1):
                data_type = "REAL DATA" if not tool.use_mock_data else "MOCK DATA"
                print(f"Source {i}: {metrics.data_source} ({data_type})")
                print(f"  - Global Rank: {metrics.global_rank:,}" if metrics.global_rank else "  - Global Rank: N/A")
                print(f"  - Monthly Visits: {metrics.monthly_visits:,}" if metrics.monthly_visits else "  - Monthly Visits: N/A")
                print(f"  - Bounce Rate: {metrics.bounce_rate}%" if metrics.bounce_rate else "  - Bounce Rate: N/A")
                print()
        else:
            print("No results found. Check your API configuration.")
            
    except Exception as e:
        print(f"Error testing: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    
    print()
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print()
    print("1. If you see 'MOCK DATA' above, get free API keys")
    print("2. If you see 'REAL DATA' above, you're all set!")
    print("3. Run: .\\run_gui.bat to start using the tool")
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
