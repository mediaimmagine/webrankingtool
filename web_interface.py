#!/usr/bin/env python3
"""
Web Interface for MediaImmagine Web Ranking Tool
Flask-based web application for comparing website metrics
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template, request, jsonify, send_file
    import json
    import csv
    import io
    from datetime import datetime
    from web_ranking_tool import WebRankingTool, WebsiteMetrics
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory and all dependencies are installed.")
    print("Try running: pip install -r requirements.txt")
    input("Press Enter to exit...")
    sys.exit(1)

app = Flask(__name__)

# Global tool instance
ranking_tool = WebRankingTool()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_websites():
    """Compare websites endpoint"""
    try:
        data = request.get_json()
        domains = data.get('domains', [])
        
        if not domains:
            return jsonify({'error': 'No domains provided'}), 400
        
        # Clean domain names
        cleaned_domains = []
        for domain in domains:
            domain = domain.strip().lower()
            domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
            if domain:
                cleaned_domains.append(domain)
        
        if not cleaned_domains:
            return jsonify({'error': 'No valid domains provided'}), 400
        
        # Compare websites
        results = ranking_tool.compare_websites(cleaned_domains)
        
        # Convert results to JSON-serializable format
        json_results = {}
        for domain, metrics_list in results.items():
            json_results[domain] = []
            for metrics in metrics_list:
                json_results[domain].append({
                    'data_source': metrics.data_source,
                    'global_rank': metrics.global_rank,
                    'country_rank': metrics.country_rank,
                    'monthly_visits': metrics.monthly_visits,
                    'bounce_rate': metrics.bounce_rate,
                    'avg_visit_duration': metrics.avg_visit_duration,
                    'pages_per_visit': metrics.pages_per_visit,
                    'traffic_sources': metrics.traffic_sources,
                    'top_countries': metrics.top_countries
                })
        
        return jsonify({
            'success': True,
            'results': json_results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/csv', methods=['POST'])
def export_csv():
    """Export results as CSV"""
    try:
        data = request.get_json()
        results_data = data.get('results', {})
        
        if not results_data:
            return jsonify({'error': 'No results to export'}), 400
        
        # Convert JSON results back to WebsiteMetrics objects
        results = {}
        for domain, metrics_list in results_data.items():
            results[domain] = []
            for metrics_dict in metrics_list:
                metrics = WebsiteMetrics(
                    domain=domain,
                    data_source=metrics_dict['data_source'],
                    global_rank=metrics_dict.get('global_rank'),
                    country_rank=metrics_dict.get('country_rank'),
                    monthly_visits=metrics_dict.get('monthly_visits'),
                    bounce_rate=metrics_dict.get('bounce_rate'),
                    avg_visit_duration=metrics_dict.get('avg_visit_duration'),
                    pages_per_visit=metrics_dict.get('pages_per_visit'),
                    traffic_sources=metrics_dict.get('traffic_sources'),
                    top_countries=metrics_dict.get('top_countries')
                )
                results[domain].append(metrics)
        
        # Create CSV in memory
        output = io.StringIO()
        fieldnames = ['Domain', 'Data Source', 'Global Rank', 'Country Rank', 
                     'Monthly Visits', 'Bounce Rate', 'Avg Visit Duration', 
                     'Pages per Visit', 'Traffic Sources', 'Top Countries']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for domain, metrics_list in results.items():
            for metrics in metrics_list:
                writer.writerow({
                    'Domain': domain,
                    'Data Source': metrics.data_source,
                    'Global Rank': metrics.global_rank or 'N/A',
                    'Country Rank': metrics.country_rank or 'N/A',
                    'Monthly Visits': metrics.monthly_visits or 'N/A',
                    'Bounce Rate': f"{metrics.bounce_rate:.1f}%" if metrics.bounce_rate else 'N/A',
                    'Avg Visit Duration': f"{metrics.avg_visit_duration:.1f}s" if metrics.avg_visit_duration else 'N/A',
                    'Pages per Visit': f"{metrics.pages_per_visit:.1f}" if metrics.pages_per_visit else 'N/A',
                    'Traffic Sources': json.dumps(metrics.traffic_sources) if metrics.traffic_sources else 'N/A',
                    'Top Countries': json.dumps(metrics.top_countries) if metrics.top_countries else 'N/A'
                })
        
        # Create response
        output.seek(0)
        csv_data = output.getvalue()
        output.close()
        
        # Return CSV file
        return send_file(
            io.BytesIO(csv_data.encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'web_ranking_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/json', methods=['POST'])
def export_json():
    """Export results as JSON"""
    try:
        data = request.get_json()
        results_data = data.get('results', {})
        
        if not results_data:
            return jsonify({'error': 'No results to export'}), 400
        
        # Add metadata
        export_data = {
            'comparison_date': datetime.now().isoformat(),
            'tool': 'MediaImmagine Web Ranking Tool',
            'domains': results_data
        }
        
        # Return JSON file
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        return send_file(
            io.BytesIO(json_str.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'web_ranking_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'tool': 'MediaImmagine Web Ranking Tool'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
