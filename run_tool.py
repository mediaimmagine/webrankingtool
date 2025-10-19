#!/usr/bin/env python3
"""
Web Ranking Tool Runner
Easy way to run the tool in different modes
"""

import sys
import os
import argparse

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from web_ranking_tool import WebRankingTool
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory and all dependencies are installed.")
    print("Try running: pip install -r requirements.txt")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Web Ranking Tool Runner")
    parser.add_argument("--mode", choices=['cli', 'web'], default='web', 
                       help="Run mode: cli for command line, web for web interface")
    parser.add_argument("--domains", nargs="+", help="Domains to compare (CLI mode only)")
    parser.add_argument("--output", "-o", help="Output file (CLI mode only)")
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        if not args.domains:
            print("Error: Please provide domains to compare in CLI mode")
            print("Example: python run_tool.py --mode cli --domains google.com facebook.com")
            sys.exit(1)
        
        print("Web Ranking Tool - CLI Mode")
        print("=" * 50)
        
        tool = WebRankingTool()
        results = tool.compare_websites(args.domains)
        tool.generate_report(results, args.output)
        
    elif args.mode == 'web':
        print("Starting Web Interface...")
        print("Open your browser and go to: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        from web_interface import app
        app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

