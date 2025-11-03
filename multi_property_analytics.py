#!/usr/bin/env python3
"""
Multi-Property Google Analytics Aggregator
Combines data from multiple GA4 properties
"""

import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from google_analytics_fetcher import GoogleAnalyticsFetcher
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension, OrderBy

class MultiPropertyAnalytics:
    """
    Aggregate data from multiple GA4 properties
    """
    
    def __init__(self, credentials_file: str, property_configs: List[Dict]):
        """
        Initialize with multiple properties
        
        Args:
            credentials_file: Path to service account JSON
            property_configs: List of dicts with 'property_id' and 'label'
        """
        self.credentials_file = credentials_file
        self.property_configs = property_configs
        self.fetchers = {}
        
        # Initialize fetchers for each property
        for config in property_configs:
            prop_id = config['property_id']
            try:
                self.fetchers[prop_id] = GoogleAnalyticsFetcher(
                    credentials_file=credentials_file,
                    property_id=prop_id
                )
                print(f"[OK] Initialized fetcher for {config['label']} ({prop_id})")
            except Exception as e:
                print(f"[WARN] Could not initialize {config['label']}: {str(e)[:80]}")
    
    def get_aggregated_metrics(self, days_back: int = 7) -> Dict:
        """
        Get aggregated metrics across all properties
        
        Returns:
            Dict with combined totals
        """
        print(f"\n[INFO] Fetching aggregated metrics from {len(self.fetchers)} properties...")
        
        total_views = 0
        total_users = 0
        total_sessions = 0
        total_avg_duration = 0
        total_bounce_rate = 0
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        property_data = []
        
        for prop_id, fetcher in self.fetchers.items():
            try:
                request = RunReportRequest(
                    property=fetcher.property_id,
                    date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                    metrics=[
                        Metric(name="screenPageViews"),
                        Metric(name="activeUsers"),
                        Metric(name="sessions"),
                        Metric(name="averageSessionDuration"),
                        Metric(name="bounceRate")
                    ]
                )
                
                response = fetcher.client.run_report(request)
                
                if response.rows:
                    row = response.rows[0]
                    views = int(row.metric_values[0].value)
                    users = int(row.metric_values[1].value)
                    sessions = int(row.metric_values[2].value)
                    avg_duration = float(row.metric_values[3].value)
                    bounce_rate = float(row.metric_values[4].value)
                    
                    total_views += views
                    total_users += users
                    total_sessions += sessions
                    total_avg_duration += avg_duration * sessions  # Weighted average
                    total_bounce_rate += bounce_rate * sessions  # Weighted average
                    
                    # Find label
                    label = next((c['label'] for c in self.property_configs if c['property_id'] == prop_id), prop_id)
                    
                    property_data.append({
                        'property_id': prop_id,
                        'label': label,
                        'views': views,
                        'users': users,
                        'sessions': sessions
                    })
                    
                    print(f"  [{label}] {views:,} views, {users:,} users")
                    
            except Exception as e:
                print(f"  [WARN] Property {prop_id}: {str(e)[:80]}")
        
        # Calculate weighted averages
        if total_sessions > 0:
            avg_session_duration = total_avg_duration / total_sessions
            avg_bounce_rate = total_bounce_rate / total_sessions
        else:
            avg_session_duration = 0
            avg_bounce_rate = 0
        
        result = {
            'total_views': total_views,
            'total_users': total_users,
            'total_sessions': total_sessions,
            'avg_session_duration': avg_session_duration,
            'bounce_rate': avg_bounce_rate,
            'properties': property_data
        }
        
        print(f"\n[TOTAL] {total_views:,} views, {total_users:,} users across all properties")
        
        return result
    
    def get_aggregated_traffic_sources(self, days_back: int = 7) -> Dict:
        """
        Get aggregated traffic sources
        """
        print(f"\n[INFO] Fetching aggregated traffic sources...")
        
        combined_sources = {}
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        for prop_id, fetcher in self.fetchers.items():
            try:
                request = RunReportRequest(
                    property=fetcher.property_id,
                    date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                    dimensions=[Dimension(name="sessionDefaultChannelGroup")],
                    metrics=[Metric(name="sessions")]
                )
                
                response = fetcher.client.run_report(request)
                
                for row in response.rows:
                    channel = row.dimension_values[0].value
                    sessions = int(row.metric_values[0].value)
                    
                    if channel in combined_sources:
                        combined_sources[channel] += sessions
                    else:
                        combined_sources[channel] = sessions
                        
            except Exception as e:
                print(f"  [WARN] Property {prop_id}: {str(e)[:80]}")
        
        return combined_sources
    
    def get_aggregated_daily_traffic(self, days_back: int = 7) -> Dict:
        """
        Get aggregated daily traffic for all properties
        
        Returns:
            Dict mapping dates (YYYYMMDD) to user counts
        """
        print(f"\n[INFO] Fetching aggregated daily traffic...")
        
        combined_daily = {}
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        for prop_id, fetcher in self.fetchers.items():
            try:
                request = RunReportRequest(
                    property=fetcher.property_id,
                    date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                    dimensions=[Dimension(name="date")],
                    metrics=[Metric(name="activeUsers")],
                    order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))]
                )
                
                response = fetcher.client.run_report(request)
                
                for row in response.rows:
                    date = row.dimension_values[0].value
                    users = int(row.metric_values[0].value)
                    
                    if date in combined_daily:
                        combined_daily[date] += users
                    else:
                        combined_daily[date] = users
                        
            except Exception as e:
                print(f"  [WARN] Property {prop_id}: {str(e)[:80]}")
        
        return combined_daily
    
    def get_aggregated_top_pages(self, days_back: int = 7, limit: int = 20) -> List[Dict]:
        """
        Get top pages across all properties
        """
        print(f"\n[INFO] Fetching top pages from all properties...")
        
        all_pages = []
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        for prop_id, fetcher in self.fetchers.items():
            try:
                # Find label
                label = next((c['label'] for c in self.property_configs if c['property_id'] == prop_id), prop_id)
                
                request = RunReportRequest(
                    property=fetcher.property_id,
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
                
                response = fetcher.client.run_report(request)
                
                for row in response.rows:
                    page_path = row.dimension_values[0].value
                    page_title = row.dimension_values[1].value
                    views = int(row.metric_values[0].value)
                    users = int(row.metric_values[1].value)
                    avg_duration = float(row.metric_values[2].value)
                    bounce_rate = float(row.metric_values[3].value)
                    
                    all_pages.append({
                        'property': label,
                        'property_id': prop_id,
                        'page_path': page_path,
                        'page_title': page_title,
                        'views': views,
                        'users': users,
                        'avg_duration': avg_duration,
                        'bounce_rate': bounce_rate
                    })
                    
            except Exception as e:
                print(f"  [WARN] Property {prop_id}: {str(e)[:80]}")
        
        # Sort by views and return top N
        all_pages.sort(key=lambda x: x['views'], reverse=True)
        return all_pages[:limit]


def load_multi_property_config() -> Optional[Dict]:
    """Load multi-property configuration"""
    try:
        with open('google_analytics_config.json', 'r') as f:
            config = json.load(f)
        
        # Check if it's multi-property config
        if 'aggregate_properties' in config:
            return config
        
        # Single property - convert to multi-property format
        return {
            'aggregate_properties': [config['property_id']],
            'property_labels': {config['property_id']: 'Main Property'},
            'credentials_file': config.get('credentials_file', 'google_analytics_credentials.json')
        }
    except FileNotFoundError:
        return None


def main():
    """Test multi-property aggregation"""
    print("="*80)
    print("Multi-Property Analytics Test")
    print("="*80)
    
    # Define properties
    properties = [
        {'property_id': '476208509', 'label': 'triesteallnews.it'},
        {'property_id': '316181048', 'label': 'www.triesteallnews.it'},
        {'property_id': '257131451', 'label': 'FVG.news'}
    ]
    
    analytics = MultiPropertyAnalytics(
        credentials_file='google_analytics_credentials.json',
        property_configs=properties
    )
    
    # Test aggregated metrics
    metrics = analytics.get_aggregated_metrics(days_back=7)
    
    print("\n" + "="*80)
    print("AGGREGATED RESULTS (Last 7 Days)")
    print("="*80)
    print(f"Total Page Views: {metrics['total_views']:,}")
    print(f"Total Users: {metrics['total_users']:,}")
    print(f"Total Sessions: {metrics['total_sessions']:,}")
    print(f"Avg Session Duration: {metrics['avg_session_duration']:.1f}s")
    print(f"Bounce Rate: {metrics['bounce_rate']:.2f}%")
    
    # Test traffic sources
    sources = analytics.get_aggregated_traffic_sources(days_back=7)
    print("\n" + "="*80)
    print("COMBINED TRAFFIC SOURCES")
    print("="*80)
    for channel, sessions in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {channel}: {sessions:,} sessions")
    
    # Test top pages
    top_pages = analytics.get_aggregated_top_pages(days_back=7, limit=10)
    print("\n" + "="*80)
    print("TOP PAGES (All Properties)")
    print("="*80)
    for i, page in enumerate(top_pages, 1):
        print(f"\n{i}. {page['page_title'][:60]}")
        print(f"   Property: {page['property']}")
        print(f"   Views: {page['views']:,}, Users: {page['users']:,}")


if __name__ == "__main__":
    main()

