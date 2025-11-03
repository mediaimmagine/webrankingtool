#!/usr/bin/env python3
"""
Google Analytics Data Fetcher
Fetches real traffic data from GA4 using Analytics Data API
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    OrderBy,
    FilterExpression,
    Filter,
    FilterExpressionList
)
from google.oauth2 import service_account


class GoogleAnalyticsFetcher:
    """
    Fetch real traffic data from Google Analytics 4
    """
    
    def __init__(self, credentials_file: str, property_id: str):
        """
        Initialize GA fetcher
        
        Args:
            credentials_file: Path to service account JSON credentials
            property_id: GA4 Property ID (format: "123456789")
        """
        self.property_id = f"properties/{property_id}"
        
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
        
        # Initialize client
        self.client = BetaAnalyticsDataClient(credentials=credentials)
        
        print(f"[INIT] Google Analytics Fetcher")
        print(f"  Property ID: {property_id}")
    
    def get_page_views_by_url(self, 
                               days_back: int = 7,
                               limit: int = 1000) -> Dict[str, Dict]:
        """
        Get page views per URL for the specified time period
        
        Args:
            days_back: Number of days to look back
            limit: Maximum number of URLs to return
        
        Returns:
            Dict mapping URL paths to traffic data
            Example: {"/2025/11/article-title/": {"views": 1523, "users": 1205}}
        """
        print(f"\n[INFO] Fetching page views from Google Analytics (last {days_back} days)...")
        
        try:
            # Define date range
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Create request
            request = RunReportRequest(
                property=self.property_id,
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                dimensions=[
                    Dimension(name="pagePath"),
                    Dimension(name="pageTitle")
                ],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="bounceRate")
                ],
                limit=limit,
                order_bys=[
                    OrderBy(
                        metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"),
                        desc=True
                    )
                ]
            )
            
            # Run report
            response = self.client.run_report(request)
            
            # Process results
            traffic_data = {}
            
            for row in response.rows:
                page_path = row.dimension_values[0].value
                page_title = row.dimension_values[1].value
                views = int(row.metric_values[0].value)
                users = int(row.metric_values[1].value)
                avg_duration = float(row.metric_values[2].value)
                bounce_rate = float(row.metric_values[3].value)
                
                traffic_data[page_path] = {
                    'page_views': views,
                    'unique_users': users,
                    'avg_session_duration': avg_duration,
                    'bounce_rate': bounce_rate,
                    'page_title': page_title
                }
            
            print(f"[OK] Retrieved traffic data for {len(traffic_data)} URLs")
            return traffic_data
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch GA data: {str(e)}")
            return {}
    
    def get_article_traffic(self, article_url_path: str, days_back: int = 30) -> Optional[Dict]:
        """
        Get traffic data for a specific article URL
        
        Args:
            article_url_path: URL path (e.g., "/2025/11/article-title/")
            days_back: Number of days to analyze
        
        Returns:
            Dict with traffic metrics or None
        """
        try:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Create filter for specific page
            dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.EXACT,
                        value=article_url_path
                    )
                )
            )
            
            request = RunReportRequest(
                property=self.property_id,
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                dimensions=[Dimension(name="pagePath")],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers")
                ],
                dimension_filter=dimension_filter
            )
            
            response = self.client.run_report(request)
            
            if response.rows:
                row = response.rows[0]
                return {
                    'page_views': int(row.metric_values[0].value),
                    'unique_users': int(row.metric_values[1].value)
                }
            
            return None
            
        except Exception as e:
            print(f"[WARN] Could not get traffic for {article_url_path}: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """Test if GA API connection works"""
        print("\n[TEST] Testing Google Analytics API connection...")
        
        try:
            # Simple test: get last 7 days total
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            request = RunReportRequest(
                property=self.property_id,
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers")
                ]
            )
            
            response = self.client.run_report(request)
            
            if response.rows:
                total_views = int(response.rows[0].metric_values[0].value)
                total_users = int(response.rows[0].metric_values[1].value)
                
                print(f"[OK] Connection successful!")
                print(f"  Last 7 days - Page Views: {total_views:,}")
                print(f"  Last 7 days - Users: {total_users:,}")
                return True
            else:
                print(f"[WARN] Connection works but no data yet")
                print(f"[INFO] Data appears 24-48 hours after Site Kit installation")
                return True
                
        except Exception as e:
            print(f"[ERROR] Connection failed: {str(e)}")
            return False


def load_config() -> Optional[Dict]:
    """Load GA configuration"""
    try:
        with open('google_analytics_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def main():
    """Test setup"""
    setup = GoogleAnalyticsSetup()
    setup.quick_setup_guide()
    
    print("\n" + "="*80)
    input("Press Enter after completing the setup guide...")
    
    setup.setup_interactive()


if __name__ == "__main__":
    main()

