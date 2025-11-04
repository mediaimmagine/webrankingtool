#!/usr/bin/env python3
"""
Enhanced GUI Web Ranking Comparison Tool
Features: Site selection boxes, preview windows, monthly comparison charts
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import json
    import csv
    import threading
    import time
    from web_ranking_tool import WebRankingTool, WebsiteMetrics
    from article_analytics import ArticleAnalyticsEngine, ArticleData, ArticleAnalytics
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory and all dependencies are installed.")
    print("Try running: pip install -r requirements_gui.txt")
    input("Press Enter to exit...")
    sys.exit(1)

class WebRankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediaImmagine Web Ranking Tool - Enhanced GUI")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize the web ranking tool
        self.tool = WebRankingTool()
        
        # Initialize the article analytics engine
        self.article_engine = ArticleAnalyticsEngine()
        
        # Data storage
        self.site1_data = None
        self.site2_data = None
        self.site3_data = None
        self.historical_data = {}
        
        # Article analytics data storage
        self.daily_articles = []
        self.last_7_days_articles = []
        self.article_analytics = None
        
        # Create main interface
        self.create_widgets()
        
        # Style configuration
        self.setup_styles()
    
    def setup_styles(self):
        """Configure GUI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        style.configure('Custom.TEntry', font=('Arial', 10))
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main title with logo
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        # Create horizontal layout for logo and title
        title_content = tk.Frame(title_frame, bg='#2c3e50')
        title_content.pack(expand=True)
        
        # Load and display MediaImmagine logo
        try:
            logo_image = tk.PhotoImage(file="mediaimmagine_logo.png")
            # Resize logo to fit nicely in the header (maintain aspect ratio)
            logo_image = logo_image.subsample(2, 2)  # Make it smaller
            
            logo_label = tk.Label(title_content, image=logo_image, bg='#2c3e50')
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(side='left', padx=(10, 20), pady=10)
        except Exception as e:
            print(f"Could not load MediaImmagine logo: {e}")
            # Continue without logo if it fails to load
        
        # Title label
        title_label = tk.Label(title_content, text="Web Ranking Tool", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(side='left', expand=True)
        
        # Status bar with IP and API info
        status_frame = tk.Frame(self.root, bg='#34495e', height=25)
        status_frame.pack(fill='x', padx=10, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        # Get current IP
        try:
            import requests
            response = requests.get("https://api.ipify.org", timeout=3)
            current_ip = response.text.strip() if response.status_code == 200 else "Unknown"
        except:
            current_ip = "Unknown"
        
        # Check API configuration and Cloudflare connection
        try:
            from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
            from cloudflare_article_analytics import CloudflareArticleAnalytics
            
            if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID:
                # Test actual Cloudflare connection
                cf = CloudflareArticleAnalytics()
                cf_insights = cf.get_cloudflare_insights()
                
                if cf_insights['cloudflare_connected']:
                    api_status = f"Cloudflare Analytics ({cf_insights['zone_plan']})"
                    api_color = "#27ae60"
                else:
                    api_status = "Cloudflare API Configured (Zone Access Limited)"
                    api_color = "#f39c12"
            else:
                api_status = "Using Fallback Methods"
                api_color = "#e74c3c"
        except:
            api_status = "Using Fallback Methods"
            api_color = "#e74c3c"
        
        # Status labels
        tk.Label(status_frame, text=f"IP: {current_ip}", font=('Arial', 9), 
                fg='white', bg='#34495e').pack(side='left', padx=(10, 0))
        
        tk.Label(status_frame, text="|", font=('Arial', 9), 
                fg='white', bg='#34495e').pack(side='left', padx=5)
        
        tk.Label(status_frame, text=f"Status: {api_status}", font=('Arial', 9), 
                fg=api_color, bg='#34495e').pack(side='left')
        
        # Main content frame with notebook (don't expand fully to show footer)
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=(5, 0))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_website_analysis_tab()
        self.create_article_analytics_tab()
        self.create_analytics_dashboard_tab()
        self.create_marketing_dashboard_tab()
        self.create_seozoom_keywords_tab()
        
        # Footer with credits
        footer_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        footer_frame.pack(fill='x', padx=10, pady=(5, 10))
        footer_frame.pack_propagate(False)
        
        credits_text = "mediaimmagine s.r.l. - COED Digital Editor IA CUP D97H24001840007 PR FESR 2021-27 contributo di Regione Friuli-Venezia Giulia sviluppato con l'ausilio di IA"
        
        credits_label = tk.Label(footer_frame, text=credits_text,
                                font=('Arial', 8), bg='#2c3e50', fg='#ecf0f1',
                                wraplength=1300, justify='center')
        credits_label.pack(expand=True, pady=10)
    
    def create_website_analysis_tab(self):
        """Create the website analysis tab"""
        # Website analysis tab with scrollbar
        website_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(website_tab, text="🌐 Website Analysis")
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(website_tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(website_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Left panel - Site selection and controls
        left_panel = tk.Frame(scrollable_frame, bg='#f0f0f0', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Results and charts
        right_panel = tk.Frame(scrollable_frame, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_site_selection(left_panel)
        self.create_preview_windows(left_panel)
        self.create_traffic_sources_section(left_panel)
        self.create_controls(left_panel)
        self.create_results_area(right_panel)
        self.create_charts_area(right_panel)
    
    def create_article_analytics_tab(self):
        """Create the article analytics tab"""
        # Article analytics tab with scrollbar
        article_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(article_tab, text="📰 Article Analytics")
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(article_tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(article_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Left panel - Controls and filters
        left_panel = tk.Frame(scrollable_frame, bg='#f0f0f0', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Results and charts
        right_panel = tk.Frame(scrollable_frame, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_article_controls(left_panel)
        self.create_article_results_area(right_panel)
        self.create_article_charts_area(right_panel)
    
    def create_analytics_dashboard_tab(self):
        """Create the Google Analytics dashboard tab"""
        # Analytics dashboard tab
        dashboard_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(dashboard_tab, text="📖 Article Visits (GA)")
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(dashboard_tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main container (now inside scrollable frame)
        main_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Info banner - Multi-property aggregation notice
        info_frame = tk.Frame(main_container, bg='#e3f2fd', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 10))
        
        info_icon = tk.Label(info_frame, text="ℹ️", font=('Arial', 14), bg='#e3f2fd')
        info_icon.pack(side='left', padx=(10, 5), pady=8)
        
        info_text = tk.Label(info_frame, 
                            text="Multi-Property Aggregation: Combining data from 3 GA4 properties for triesteallnews.it",
                            font=('Arial', 10, 'bold'), bg='#e3f2fd', fg='#1976d2', anchor='w')
        info_text.pack(side='left', padx=(0, 10), pady=8, fill='x', expand=True)
        
        # Properties details label
        self.properties_info_label = tk.Label(info_frame, 
                                             text="Loading properties...",
                                             font=('Arial', 8), bg='#e3f2fd', fg='#555', anchor='w')
        self.properties_info_label.pack(side='left', padx=(0, 10), pady=8)
        
        # Date range label (NEW)
        self.date_range_label = tk.Label(info_frame,
                                         text="Last 28 days",
                                         font=('Arial', 9, 'bold'), bg='#e3f2fd', fg='#1976d2')
        self.date_range_label.pack(side='right', padx=(0, 10), pady=8)
        
        # Top section - Metrics cards
        metrics_frame = tk.Frame(main_container, bg='#f0f0f0')
        metrics_frame.pack(fill='x', pady=(0, 10))
        
        # Create metric cards (like Site Kit)
        self.create_metric_card(metrics_frame, "All Visitors", "0", "#4285f4", 0)
        self.create_metric_card(metrics_frame, "Page Views", "0", "#34a853", 1)
        self.create_metric_card(metrics_frame, "Avg. Session", "0s", "#fbbc04", 2)
        self.create_metric_card(metrics_frame, "Bounce Rate", "0%", "#ea4335", 3)
        
        # Middle section - Traffic sources chart
        charts_frame = tk.Frame(main_container, bg='#f0f0f0')
        charts_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Configure columns for better space distribution
        charts_frame.grid_columnconfigure(0, weight=1)  # Traffic sources
        charts_frame.grid_columnconfigure(1, weight=2)  # Daily visitors (2x wider)
        
        # Left - Traffic Sources Pie Chart
        sources_frame = tk.LabelFrame(charts_frame, text="Traffic Sources", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        sources_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=0)
        
        # Create matplotlib figure for traffic sources
        from matplotlib.figure import Figure
        self.traffic_sources_fig = Figure(figsize=(5, 4), dpi=100)
        self.traffic_sources_ax = self.traffic_sources_fig.add_subplot(111)
        
        self.traffic_sources_canvas = FigureCanvasTkAgg(self.traffic_sources_fig, sources_frame)
        self.traffic_sources_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Right - Daily Traffic Chart (BIGGER)
        daily_frame = tk.LabelFrame(charts_frame, text="Daily Visitors - Multi-Period (3 Time Scales)",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        daily_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0), pady=0)
        
        self.daily_traffic_fig = Figure(figsize=(9, 5), dpi=100)
        self.daily_traffic_ax = self.daily_traffic_fig.add_subplot(111)
        
        self.daily_traffic_canvas = FigureCanvasTkAgg(self.daily_traffic_fig, daily_frame)
        self.daily_traffic_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Trieste section - Dedicated charts
        trieste_section = tk.LabelFrame(main_container, text="📍 TRIESTE.NEWS / TRIESTEALLNEWS.IT - Dedicated Analytics",
                                       font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        trieste_section.pack(fill='x', pady=(10, 10))
        
        # Trieste header with metrics
        trieste_header = tk.Frame(trieste_section, bg='#f0f0f0')
        trieste_header.pack(fill='x', padx=10, pady=(10, 5))
        
        # Trieste 28-day metrics box
        trieste_metrics_frame = tk.Frame(trieste_header, bg='#e3f2fd', relief='solid', bd=1)
        trieste_metrics_frame.pack(side='left', padx=(0, 10))
        
        tk.Label(trieste_metrics_frame, text="Last 28 Days:", font=('Arial', 9, 'bold'),
                bg='#e3f2fd', fg='#1976d2').pack(side='left', padx=(10, 5), pady=5)
        
        self.trieste_visitors_label = tk.Label(trieste_metrics_frame, text="Loading...", 
                                               font=('Arial', 11, 'bold'),
                                               bg='#e3f2fd', fg='#4285f4')
        self.trieste_visitors_label.pack(side='left', padx=(0, 10), pady=5)
        
        trieste_charts = tk.Frame(trieste_section, bg='#f0f0f0')
        trieste_charts.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure columns - give more space to daily chart
        trieste_charts.grid_columnconfigure(0, weight=1)
        trieste_charts.grid_columnconfigure(1, weight=2)
        
        # Left - Trieste Traffic Sources
        trieste_sources_frame = tk.LabelFrame(trieste_charts, text="Traffic Sources (Last 7 Days)",
                                             font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        trieste_sources_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        self.trieste_sources_fig = Figure(figsize=(4, 3), dpi=100)
        self.trieste_sources_ax = self.trieste_sources_fig.add_subplot(111)
        self.trieste_sources_canvas = FigureCanvasTkAgg(self.trieste_sources_fig, trieste_sources_frame)
        self.trieste_sources_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Right - Trieste Daily Traffic (BIGGER)
        trieste_daily_frame = tk.LabelFrame(trieste_charts, text="Daily Visitors - Multi-Period (3 Scales)",
                                           font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        trieste_daily_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.trieste_daily_fig = Figure(figsize=(8, 4), dpi=100)
        self.trieste_daily_ax = self.trieste_daily_fig.add_subplot(111)
        self.trieste_daily_canvas = FigureCanvasTkAgg(self.trieste_daily_fig, trieste_daily_frame)
        self.trieste_daily_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pordenone section - Dedicated charts
        pordenone_section = tk.LabelFrame(main_container, text="📍 PORDENONEOGGI.IT - Dedicated Analytics",
                                         font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pordenone_section.pack(fill='x', pady=(10, 10))
        
        # Pordenone header with metrics
        pordenone_header = tk.Frame(pordenone_section, bg='#f0f0f0')
        pordenone_header.pack(fill='x', padx=10, pady=(10, 5))
        
        # Pordenone 28-day metrics box
        pordenone_metrics_frame = tk.Frame(pordenone_header, bg='#ffebee', relief='solid', bd=1)
        pordenone_metrics_frame.pack(side='left', padx=(0, 10))
        
        tk.Label(pordenone_metrics_frame, text="Last 28 Days:", font=('Arial', 9, 'bold'),
                bg='#ffebee', fg='#c62828').pack(side='left', padx=(10, 5), pady=5)
        
        self.pordenone_visitors_label = tk.Label(pordenone_metrics_frame, text="Loading...", 
                                                 font=('Arial', 11, 'bold'),
                                                 bg='#ffebee', fg='#ea4335')
        self.pordenone_visitors_label.pack(side='left', padx=(0, 10), pady=5)
        
        pordenone_charts = tk.Frame(pordenone_section, bg='#f0f0f0')
        pordenone_charts.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure columns - give more space to daily chart
        pordenone_charts.grid_columnconfigure(0, weight=1)
        pordenone_charts.grid_columnconfigure(1, weight=2)
        
        # Left - Pordenone Traffic Sources
        pordenone_sources_frame = tk.LabelFrame(pordenone_charts, text="Traffic Sources (Last 7 Days)",
                                               font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pordenone_sources_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        self.pordenone_sources_fig = Figure(figsize=(4, 3), dpi=100)
        self.pordenone_sources_ax = self.pordenone_sources_fig.add_subplot(111)
        self.pordenone_sources_canvas = FigureCanvasTkAgg(self.pordenone_sources_fig, pordenone_sources_frame)
        self.pordenone_sources_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Right - Pordenone Daily Traffic (BIGGER)
        pordenone_daily_frame = tk.LabelFrame(pordenone_charts, text="Daily Visitors - Multi-Period (3 Scales)",
                                             font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pordenone_daily_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.pordenone_daily_fig = Figure(figsize=(8, 4), dpi=100)
        self.pordenone_daily_ax = self.pordenone_daily_fig.add_subplot(111)
        self.pordenone_daily_canvas = FigureCanvasTkAgg(self.pordenone_daily_fig, pordenone_daily_frame)
        self.pordenone_daily_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bottom section - Top pages table
        pages_frame = tk.LabelFrame(main_container, text="Top Pages (Last 28 Days)",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pages_frame.pack(fill='both', expand=True)
        
        # Create treeview for top pages
        columns = ('Page', 'Views', 'Users', 'Avg Time', 'Bounce %')
        self.top_pages_tree = ttk.Treeview(pages_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        self.top_pages_tree.heading('Page', text='Page Title / URL')
        self.top_pages_tree.heading('Views', text='Page Views')
        self.top_pages_tree.heading('Users', text='Users')
        self.top_pages_tree.heading('Avg Time', text='Avg. Time')
        self.top_pages_tree.heading('Bounce %', text='Bounce %')
        
        self.top_pages_tree.column('Page', width=400)
        self.top_pages_tree.column('Views', width=100, anchor='center')
        self.top_pages_tree.column('Users', width=100, anchor='center')
        self.top_pages_tree.column('Avg Time', width=100, anchor='center')
        self.top_pages_tree.column('Bounce %', width=100, anchor='center')
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(pages_frame, orient='vertical', command=self.top_pages_tree.yview)
        self.top_pages_tree.configure(yscrollcommand=scrollbar.set)
        
        self.top_pages_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10, padx=(0, 10))
        
        # Control buttons
        controls_frame = tk.Frame(main_container, bg='#f0f0f0')
        controls_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(controls_frame, text="🔄 Refresh Analytics Data", 
                  command=self.refresh_analytics_dashboard,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(controls_frame, text="📊 Export Dashboard Data", 
                  command=self.export_dashboard_data,
                  style='Custom.TButton').pack(side='left')
        
        # Status label
        self.dashboard_status = tk.Label(controls_frame, text="Ready to load data", 
                                        font=('Arial', 9), bg='#f0f0f0', fg='#666')
        self.dashboard_status.pack(side='right', padx=10)
        
        # Initial load
        self.refresh_analytics_dashboard()
    
    def create_metric_card(self, parent, title, value, color, column):
        """Create a metric card (like Site Kit style)"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        card.grid(row=0, column=column, padx=5, pady=5, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        
        # Title
        tk.Label(card, text=title, font=('Arial', 10), 
                bg='white', fg='#666').pack(pady=(15, 5))
        
        # Value (large number)
        value_label = tk.Label(card, text=value, font=('Arial', 24, 'bold'), 
                              bg='white', fg=color)
        value_label.pack(pady=(0, 15))
        
        # Store reference for updating
        setattr(self, f'metric_{title.lower().replace(" ", "_").replace(".", "")}', value_label)
    
    def refresh_analytics_dashboard(self):
        """Refresh the analytics dashboard with real data from Google Analytics"""
        self.dashboard_status.config(text="Loading analytics data...", fg='#f39c12')
        self.root.update()
        
        def fetch_data():
            try:
                # Try to load Google Analytics data
                from google_analytics_fetcher import GoogleAnalyticsFetcher, load_config
                
                ga_config = load_config()
                
                if not ga_config:
                    # No GA configured yet
                    self.dashboard_status.config(
                        text="Google Analytics API not configured. See quick_ga_setup.md", 
                        fg='#e74c3c'
                    )
                    self._show_setup_placeholder()
                    return
                
                # Update properties info label
                if 'aggregate_properties' in ga_config and len(ga_config['aggregate_properties']) > 1:
                    # Multi-property mode
                    property_labels = ga_config.get('property_labels', {})
                    props_text = " | ".join([
                        f"{property_labels.get(pid, pid)} (GA4: {pid})" 
                        for pid in ga_config['aggregate_properties']
                    ])
                    self.properties_info_label.config(text=props_text)
                else:
                    # Single property mode
                    prop_id = ga_config.get('property_id', 'N/A')
                    self.properties_info_label.config(text=f"GA4 Property: {prop_id}")
                
                # Check if multi-property aggregation is enabled
                if ga_config.get('use_aggregation') and 'aggregate_properties' in ga_config:
                    # Use multi-property analytics
                    from multi_property_analytics import MultiPropertyAnalytics
                    
                    property_configs = [
                        {'property_id': pid, 'label': ga_config['property_labels'].get(pid, pid)}
                        for pid in ga_config['aggregate_properties']
                    ]
                    
                    analytics = MultiPropertyAnalytics(
                        credentials_file=ga_config['credentials_file'],
                        property_configs=property_configs
                    )
                    
                    # Get aggregated metrics (28 days to match Site Kit default)
                    metrics = analytics.get_aggregated_metrics(days_back=28)
                    
                    if metrics:
                        # Convert to format expected by _update_metric_cards
                        formatted_metrics = {
                            'users': metrics['total_users'],
                            'pageviews': metrics['total_views'],
                            'avg_session': metrics['avg_session_duration'],
                            'bounce_rate': metrics['bounce_rate']
                        }
                        self._update_metric_cards(formatted_metrics)
                        
                        # Update traffic sources
                        sources = analytics.get_aggregated_traffic_sources(days_back=28)
                        if sources:
                            self._update_traffic_sources_chart(sources)
                        
                        # Update daily traffic (multi-period)
                        self._update_daily_traffic_chart(analytics)
                        
                        # Update Trieste-specific charts (last 7 days)
                        self._update_trieste_charts(analytics)
                        
                        # Update Pordenone-specific charts (last 7 days)
                        self._update_pordenone_charts(analytics)
                        
                        # Update top pages
                        top_pages = analytics.get_aggregated_top_pages(days_back=28, limit=20)
                        if top_pages:
                            self._update_top_pages_table_aggregated(top_pages)
                        
                        self.dashboard_status.config(
                            text=f"Last updated: {datetime.now().strftime('%H:%M:%S')} - Aggregated from {len(property_configs)} properties", 
                            fg='#27ae60'
                        )
                    else:
                        self.dashboard_status.config(
                            text="No aggregated data available yet", 
                            fg='#f39c12'
                        )
                    return
                
                # Single property mode (fallback)
                ga_fetcher = GoogleAnalyticsFetcher(
                    credentials_file=ga_config['credentials_file'],
                    property_id=ga_config.get('primary_property_id', ga_config['property_id'])
                )
                
                # Get overall metrics (last 7 days)
                metrics = self._fetch_ga_overall_metrics(ga_fetcher)
                
                if metrics:
                    # Update metric cards
                    self._update_metric_cards(metrics)
                    
                    # Update traffic sources chart
                    sources = self._fetch_ga_traffic_sources(ga_fetcher)
                    if sources:
                        self._update_traffic_sources_chart(sources)
                    
                    # Update daily traffic chart
                    daily_data = self._fetch_ga_daily_traffic(ga_fetcher)
                    if daily_data:
                        self._update_daily_traffic_chart(daily_data)
                    
                    # Update top pages table
                    top_pages = self._fetch_ga_top_pages(ga_fetcher)
                    if top_pages:
                        self._update_top_pages_table(top_pages)
                    
                    self.dashboard_status.config(
                        text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}", 
                        fg='#27ae60'
                    )
                else:
                    self.dashboard_status.config(
                        text="No data available yet. Wait 24-48h after GA installation.", 
                        fg='#f39c12'
                    )
                    
            except ImportError:
                self.dashboard_status.config(
                    text="Install: pip install google-analytics-data", 
                    fg='#e74c3c'
                )
            except FileNotFoundError as e:
                self.dashboard_status.config(
                    text="Credentials file not found. Run google_analytics_setup.py", 
                    fg='#e74c3c'
                )
            except Exception as e:
                self.dashboard_status.config(
                    text=f"Error: {str(e)[:50]}", 
                    fg='#e74c3c'
                )
        
        # Run in thread to avoid blocking GUI
        thread = threading.Thread(target=fetch_data, daemon=True)
        thread.start()
    
    def _show_setup_placeholder(self):
        """Show placeholder when GA not configured"""
        # Clear existing chart
        self.traffic_sources_ax.clear()
        self.traffic_sources_ax.text(0.5, 0.5, 'Google Analytics\nNot Configured\n\nSee: quick_ga_setup.md',
                                     ha='center', va='center', fontsize=14, color='#999')
        self.traffic_sources_ax.axis('off')
        self.traffic_sources_canvas.draw()
        
        self.daily_traffic_ax.clear()
        self.daily_traffic_ax.text(0.5, 0.5, 'Awaiting\nConfiguration',
                                   ha='center', va='center', fontsize=14, color='#999')
        self.daily_traffic_ax.axis('off')
        self.daily_traffic_canvas.draw()
    
    def _fetch_ga_overall_metrics(self, ga_fetcher):
        """Fetch overall metrics from GA"""
        try:
            from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
            
            request = RunReportRequest(
                property=ga_fetcher.property_id,
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
                metrics=[
                    Metric(name="activeUsers"),
                    Metric(name="screenPageViews"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="bounceRate")
                ]
            )
            
            response = ga_fetcher.client.run_report(request)
            
            if response.rows:
                row = response.rows[0]
                return {
                    'users': int(row.metric_values[0].value),
                    'pageviews': int(row.metric_values[1].value),
                    'avg_session': float(row.metric_values[2].value),
                    'bounce_rate': float(row.metric_values[3].value)
                }
            
            return None
        except Exception as e:
            print(f"[ERROR] Fetching metrics: {str(e)}")
            return None
    
    def _fetch_ga_traffic_sources(self, ga_fetcher):
        """Fetch traffic sources from GA"""
        try:
            from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
            
            request = RunReportRequest(
                property=ga_fetcher.property_id,
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
                dimensions=[Dimension(name="sessionDefaultChannelGroup")],
                metrics=[Metric(name="sessions")]
            )
            
            response = ga_fetcher.client.run_report(request)
            
            sources = {}
            for row in response.rows:
                channel = row.dimension_values[0].value
                sessions = int(row.metric_values[0].value)
                sources[channel] = sessions
            
            return sources
        except Exception as e:
            print(f"[ERROR] Fetching traffic sources: {str(e)}")
            return None
    
    def _fetch_ga_daily_traffic(self, ga_fetcher):
        """Fetch daily traffic for last 7 days"""
        try:
            from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric, OrderBy
            
            request = RunReportRequest(
                property=ga_fetcher.property_id,
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
                dimensions=[Dimension(name="date")],
                metrics=[Metric(name="activeUsers")],
                order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))]
            )
            
            response = ga_fetcher.client.run_report(request)
            
            daily_data = {}
            for row in response.rows:
                date = row.dimension_values[0].value
                users = int(row.metric_values[0].value)
                daily_data[date] = users
            
            return daily_data
        except Exception as e:
            print(f"[ERROR] Fetching daily traffic: {str(e)}")
            return None
    
    def _fetch_ga_top_pages(self, ga_fetcher):
        """Fetch top pages from GA"""
        try:
            from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric, OrderBy
            
            request = RunReportRequest(
                property=ga_fetcher.property_id,
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
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
                limit=20,
                order_bys=[
                    OrderBy(
                        metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"),
                        desc=True
                    )
                ]
            )
            
            response = ga_fetcher.client.run_report(request)
            
            top_pages = []
            for row in response.rows:
                page_path = row.dimension_values[0].value
                page_title = row.dimension_values[1].value
                views = int(row.metric_values[0].value)
                users = int(row.metric_values[1].value)
                avg_time = float(row.metric_values[2].value)
                bounce = float(row.metric_values[3].value)
                
                top_pages.append({
                    'path': page_path,
                    'title': page_title,
                    'views': views,
                    'users': users,
                    'avg_time': avg_time,
                    'bounce': bounce
                })
            
            return top_pages
        except Exception as e:
            print(f"[ERROR] Fetching top pages: {str(e)}")
            return None
    
    def _update_metric_cards(self, metrics):
        """Update metric card values"""
        try:
            # Update All Visitors
            self.metric_all_visitors.config(text=f"{metrics['users']:,}")
            
            # Update Page Views
            self.metric_page_views.config(text=f"{metrics['pageviews']:,}")
            
            # Update Avg Session (convert seconds to readable format)
            avg_sec = int(metrics['avg_session'])
            mins = avg_sec // 60
            secs = avg_sec % 60
            self.metric_avg_session.config(text=f"{mins}m {secs}s")
            
            # Update Bounce Rate
            self.metric_bounce_rate.config(text=f"{metrics['bounce_rate']:.1f}%")
            
        except Exception as e:
            print(f"[ERROR] Updating metrics: {str(e)}")
    
    def _update_traffic_sources_chart(self, sources):
        """Update traffic sources pie chart"""
        try:
            self.traffic_sources_ax.clear()
            
            # Prepare data with better labels
            label_map = {
                'Organic Search': 'Organic Search',
                'Organic Social': 'Social Media',
                'Direct': 'Direct Traffic',
                'Referral': 'Referrals',
                'Cross-network': 'Google Network',
                'Paid Search': 'Paid Ads',
                'Unassigned': 'Other'
            }
            
            labels = [label_map.get(k, k) for k in sources.keys()]
            sizes = list(sources.values())
            
            # Better color palette with distinct colors for organic types
            color_map = {
                'Organic Search': '#34a853',  # Green
                'Social Media': '#4285f4',    # Blue
                'Direct Traffic': '#fbbc04',  # Yellow
                'Referrals': '#ea4335',       # Red
                'Google Network': '#9c27b0',  # Purple
                'Paid Ads': '#00bcd4',        # Cyan
                'Other': '#999999'            # Gray
            }
            colors = [color_map.get(label, '#cccccc') for label in labels]
            
            # Create pie chart with better formatting
            wedges, texts, autotexts = self.traffic_sources_ax.pie(
                sizes, labels=labels, autopct='%1.1f%%',
                colors=colors, startangle=90,
                textprops={'fontsize': 9},
                pctdistance=0.85
            )
            
            # Make percentage text smaller and bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(8)
                autotext.set_weight('bold')
            
            # Make labels smaller to avoid overlap
            for text in texts:
                text.set_fontsize(8)
            
            self.traffic_sources_ax.set_title('Traffic Sources\n(Google Network = Google properties & partner sites)', 
                                             fontsize=10, pad=10)
            
            self.traffic_sources_canvas.draw()
            
        except Exception as e:
            print(f"[ERROR] Updating traffic sources chart: {str(e)}")
    
    def _update_daily_traffic_chart(self, analytics):
        """Update daily traffic with three lines using normalized x-axis (0-100%) and 3 time scales"""
        try:
            # Clear and recreate
            self.daily_traffic_fig.clear()
            ax = self.daily_traffic_fig.add_subplot(111)
            
            # Get data for different time periods
            daily_7d = analytics.get_aggregated_daily_traffic(days_back=7)
            daily_28d = analytics.get_aggregated_daily_traffic(days_back=28)
            daily_90d = analytics.get_aggregated_daily_traffic(days_back=90)
            
            # Normalize to 0-100 scale (percentage of period)
            x_normalized = list(range(100, -1, -1))  # 100% to 0%
            
            # Plot each line with normalized x-axis
            # GREEN - 90 days
            if daily_90d:
                sorted_dates = sorted(daily_90d.keys())
                users = [daily_90d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=2, color='#34a853', alpha=0.8, label='90 days')
            
            # BLUE - 28 days  
            if daily_28d:
                sorted_dates = sorted(daily_28d.keys())
                users = [daily_28d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=2.5, color='#4285f4', alpha=0.8, label='28 days')
            
            # ORANGE - 7 days (no markers)
            if daily_7d:
                sorted_dates = sorted(daily_7d.keys())
                users = [daily_7d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=3, 
                       color='#ff9800', alpha=0.9, label='7 days')
            
            # Add grey trend line for 90-day reference (no label)
            if daily_90d:
                sorted_dates = sorted(daily_90d.keys())
                users = [daily_90d[date] for date in sorted_dates]
                if len(users) > 1:
                    # Calculate linear trend
                    import numpy as np
                    x_trend = np.array([100 - (i * 100 / (len(users)-1)) for i in range(len(users))])
                    y_trend = np.array(users)
                    z = np.polyfit(x_trend, y_trend, 1)
                    p = np.poly1d(z)
                    
                    # Plot solid grey line
                    ax.plot(x_trend, p(x_trend), '-', linewidth=2, 
                           color='#808080', alpha=0.6)
                    
                    # Calculate percentage change over 90 days
                    start_value = p(100)
                    end_value = p(0)
                    pct_change = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                    
                    # Add text showing percentage at the end (right side)
                    sign = '+' if pct_change > 0 else ''
                    ax.text(0.98, end_value, f'{sign}{pct_change:.1f}%', 
                           color='#666', fontsize=9, weight='bold',
                           ha='left', va='center',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                    edgecolor='#999', alpha=0.8))
            
            # Shared Y-axis
            ax.set_ylabel('Visitors', fontsize=10)
            ax.set_title('Daily Visitors - 3 Time Scales', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper left', fontsize=9)
            
            # Create 3 x-axis labels at bottom
            ax.set_xlabel('')
            ax.set_xlim(100, 0)
            
            # Main x-axis (bottom) - percentage
            ax.set_xticks([100, 75, 50, 25, 0])
            ax.set_xticklabels(['', '', '', '', ''], fontsize=1)  # Hide main labels
            
            # Create 3 x-axis scales below the chart
            # Orange (7 days) - bottom-most
            ax.text(0.00, -0.08, '7d:', transform=ax.transAxes, fontsize=8, color='#ff9800', weight='bold')
            ax.text(0.05, -0.08, '7', transform=ax.transAxes, fontsize=7, color='#ff9800')
            ax.text(0.27, -0.08, '5', transform=ax.transAxes, fontsize=7, color='#ff9800')
            ax.text(0.52, -0.08, '4', transform=ax.transAxes, fontsize=7, color='#ff9800')
            ax.text(0.77, -0.08, '2', transform=ax.transAxes, fontsize=7, color='#ff9800')
            ax.text(0.98, -0.08, '0', transform=ax.transAxes, fontsize=7, color='#ff9800')
            
            # Blue (28 days) - middle
            ax.text(0.00, -0.13, '28d:', transform=ax.transAxes, fontsize=8, color='#4285f4', weight='bold')
            ax.text(0.05, -0.13, '28', transform=ax.transAxes, fontsize=7, color='#4285f4')
            ax.text(0.27, -0.13, '21', transform=ax.transAxes, fontsize=7, color='#4285f4')
            ax.text(0.52, -0.13, '14', transform=ax.transAxes, fontsize=7, color='#4285f4')
            ax.text(0.77, -0.13, '7', transform=ax.transAxes, fontsize=7, color='#4285f4')
            ax.text(0.98, -0.13, '0', transform=ax.transAxes, fontsize=7, color='#4285f4')
            
            # Green (90 days) - top-most
            ax.text(0.00, -0.18, '90d:', transform=ax.transAxes, fontsize=8, color='#34a853', weight='bold')
            ax.text(0.05, -0.18, '90', transform=ax.transAxes, fontsize=7, color='#34a853')
            ax.text(0.27, -0.18, '68', transform=ax.transAxes, fontsize=7, color='#34a853')
            ax.text(0.52, -0.18, '45', transform=ax.transAxes, fontsize=7, color='#34a853')
            ax.text(0.77, -0.18, '23', transform=ax.transAxes, fontsize=7, color='#34a853')
            ax.text(0.98, -0.18, '0', transform=ax.transAxes, fontsize=7, color='#34a853')
            
            self.daily_traffic_fig.tight_layout()
            self.daily_traffic_canvas.draw()
            self.daily_traffic_ax = ax
            
        except Exception as e:
            print(f"[ERROR] Updating daily traffic chart: {str(e)}")
    
    def _update_top_pages_table(self, top_pages):
        """Update top pages table"""
        try:
            # Clear existing items
            for item in self.top_pages_tree.get_children():
                self.top_pages_tree.delete(item)
            
            # Add new items
            for page in top_pages:
                title = page['title'][:60] + '...' if len(page['title']) > 60 else page['title']
                
                # Format average time
                avg_sec = int(page['avg_time'])
                mins = avg_sec // 60
                secs = avg_sec % 60
                avg_time_str = f"{mins}:{secs:02d}"
                
                self.top_pages_tree.insert('', 'end', values=(
                    title,
                    f"{page['views']:,}",
                    f"{page['users']:,}",
                    avg_time_str,
                    f"{page['bounce']:.1f}%"
                ))
            
        except Exception as e:
            print(f"[ERROR] Updating top pages table: {str(e)}")
    
    def _update_top_pages_table_aggregated(self, top_pages):
        """Update top pages table with aggregated multi-property data"""
        try:
            # Clear existing items
            for item in self.top_pages_tree.get_children():
                self.top_pages_tree.delete(item)
            
            # Add new items
            for page in top_pages:
                # Get title and property info
                title = page.get('page_title', page.get('page_path', 'Unknown'))[:50]
                property_label = page.get('property', 'Unknown')
                
                # Add property label to title
                display_title = f"[{property_label}] {title}"
                if len(display_title) > 60:
                    display_title = display_title[:60] + '...'
                
                # Format average time
                avg_sec = int(page.get('avg_duration', 0))
                mins = avg_sec // 60
                secs = avg_sec % 60
                avg_time_str = f"{mins}:{secs:02d}"
                
                self.top_pages_tree.insert('', 'end', values=(
                    display_title,
                    f"{page.get('views', 0):,}",
                    f"{page.get('users', 0):,}",
                    avg_time_str,
                    f"{page.get('bounce_rate', 0):.1f}%"
                ))
            
        except Exception as e:
            print(f"[ERROR] Updating aggregated top pages table: {str(e)}")
    
    def _update_trieste_charts(self, analytics):
        """Update Trieste-specific charts"""
        try:
            from trieste_analytics import get_trieste_traffic_sources, get_trieste_daily_traffic, get_trieste_metrics
            
            # Get Trieste 28-day metrics for the header box
            trieste_metrics_28d = get_trieste_metrics(analytics.fetchers, days_back=28)
            if trieste_metrics_28d and trieste_metrics_28d['users'] > 0:
                self.trieste_visitors_label.config(
                    text=f"{trieste_metrics_28d['users']:,} visitors"
                )
            else:
                self.trieste_visitors_label.config(text="No data")
            
            # Get Trieste traffic sources (last 7 days)
            trieste_sources = get_trieste_traffic_sources(analytics.fetchers, days_back=7)
            
            # Update Trieste traffic sources chart
            if trieste_sources:
                self._update_trieste_sources_chart(trieste_sources)
            else:
                self._show_trieste_no_data(self.trieste_sources_ax, self.trieste_sources_canvas)
            
            # Update Trieste daily chart (multi-period)
            self._update_trieste_daily_chart(analytics)
                
        except Exception as e:
            print(f"[ERROR] Updating Trieste charts: {str(e)}")
    
    def _update_trieste_sources_chart(self, sources):
        """Update Trieste traffic sources pie chart"""
        try:
            self.trieste_sources_ax.clear()
            
            # Prepare data with better labels
            label_map = {
                'Organic Search': 'Search',
                'Organic Social': 'Social',
                'Direct': 'Direct',
                'Referral': 'Referral',
                'Cross-network': 'Google',
                'Paid Search': 'Ads',
                'Unassigned': 'Other'
            }
            
            labels = [label_map.get(k, k) for k in sources.keys()]
            sizes = list(sources.values())
            
            # Colors
            color_map = {
                'Search': '#34a853',
                'Social': '#4285f4',
                'Direct': '#fbbc04',
                'Referral': '#ea4335',
                'Google': '#9c27b0',
                'Ads': '#00bcd4',
                'Other': '#999999'
            }
            colors = [color_map.get(label, '#cccccc') for label in labels]
            
            # Create compact pie chart
            wedges, texts, autotexts = self.trieste_sources_ax.pie(
                sizes, labels=labels, autopct='%1.0f%%',
                colors=colors, startangle=90,
                textprops={'fontsize': 8},
                pctdistance=0.8
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(7)
                autotext.set_weight('bold')
            
            for text in texts:
                text.set_fontsize(7)
            
            self.trieste_sources_ax.set_title('Trieste Traffic Sources', fontsize=9)
            self.trieste_sources_canvas.draw()
            
        except Exception as e:
            print(f"[ERROR] Updating Trieste sources chart: {str(e)}")
    
    def _update_trieste_daily_chart(self, analytics):
        """Update Trieste with 3 time scales on x-axis, 1 y-axis for visitors"""
        try:
            from trieste_analytics import get_trieste_daily_traffic
            
            self.trieste_daily_fig.clear()
            ax = self.trieste_daily_fig.add_subplot(111)
            
            # Get data
            daily_7d = get_trieste_daily_traffic(analytics.fetchers, days_back=7)
            daily_28d = get_trieste_daily_traffic(analytics.fetchers, days_back=28)
            daily_90d = get_trieste_daily_traffic(analytics.fetchers, days_back=90)
            
            # Plot on normalized 0-100% scale
            if daily_90d:
                sorted_dates = sorted(daily_90d.keys())
                users = [daily_90d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=1.5, color='#34a853', alpha=0.8, label='90d')
            
            if daily_28d:
                sorted_dates = sorted(daily_28d.keys())
                users = [daily_28d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=2, color='#4285f4', alpha=0.8, label='28d')
            
            if daily_7d:
                sorted_dates = sorted(daily_7d.keys())
                users = [daily_7d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=2.5,
                       color='#ff9800', alpha=0.9, label='7d')
            
            # Add grey trend line for 90-day reference (no label)
            if daily_90d:
                sorted_dates = sorted(daily_90d.keys())
                users = [daily_90d[date] for date in sorted_dates]
                if len(users) > 1:
                    import numpy as np
                    x_trend = np.array([100 - (i * 100 / (len(users)-1)) for i in range(len(users))])
                    y_trend = np.array(users)
                    z = np.polyfit(x_trend, y_trend, 1)
                    p = np.poly1d(z)
                    
                    # Plot solid grey line
                    ax.plot(x_trend, p(x_trend), '-', linewidth=2,
                           color='#808080', alpha=0.6)
                    
                    # Calculate percentage change over 90 days
                    start_value = p(100)
                    end_value = p(0)
                    pct_change = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                    
                    # Add text showing percentage at the end (right side)
                    sign = '+' if pct_change > 0 else ''
                    ax.text(0.98, end_value, f'{sign}{pct_change:.1f}%',
                           color='#666', fontsize=8, weight='bold',
                           ha='left', va='center',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                    edgecolor='#999', alpha=0.8))
            
            ax.set_ylabel('Visitors', fontsize=8)
            ax.set_title('Trieste 3-Scale', fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper left', fontsize=7)
            ax.set_xlim(100, 0)
            ax.set_xticks([])
            
            # 3 x-axis scales
            ax.text(0.00, -0.10, '7d:', transform=ax.transAxes, fontsize=7, color='#ff9800', weight='bold')
            ax.text(0.98, -0.10, '→0', transform=ax.transAxes, fontsize=6, color='#ff9800', ha='right')
            ax.text(0.00, -0.15, '28d:', transform=ax.transAxes, fontsize=7, color='#4285f4', weight='bold')
            ax.text(0.98, -0.15, '→0', transform=ax.transAxes, fontsize=6, color='#4285f4', ha='right')
            ax.text(0.00, -0.20, '90d:', transform=ax.transAxes, fontsize=7, color='#34a853', weight='bold')
            ax.text(0.98, -0.20, '→0', transform=ax.transAxes, fontsize=6, color='#34a853', ha='right')
            
            self.trieste_daily_fig.tight_layout()
            self.trieste_daily_canvas.draw()
            self.trieste_daily_ax = ax
            
        except Exception as e:
            print(f"[ERROR] Updating Trieste daily chart: {str(e)}")
    
    def _show_trieste_no_data(self, ax, canvas):
        """Show 'no data' message for Trieste charts"""
        ax.clear()
        ax.text(0.5, 0.5, 'No Data\nAvailable',
               ha='center', va='center', fontsize=10, color='#999')
        ax.axis('off')
        canvas.draw()
    
    def _update_pordenone_charts(self, analytics):
        """Update Pordenone-specific charts"""
        try:
            from pordenone_analytics import get_pordenone_traffic_sources, get_pordenone_daily_traffic, get_pordenone_metrics
            
            # Get FVG.news fetcher (pordenoneoggi is part of this property)
            fvg_fetcher = None
            for prop_id, fetcher in analytics.fetchers.items():
                if prop_id == "257131451":  # FVG.news property
                    fvg_fetcher = fetcher
                    break
            
            if not fvg_fetcher:
                print("[WARN] FVG.news property not found for Pordenone data")
                self.pordenone_visitors_label.config(text="No data")
                return
            
            # Get Pordenone 28-day metrics for the header box
            pordenone_metrics_28d = get_pordenone_metrics(fvg_fetcher, days_back=28)
            if pordenone_metrics_28d and pordenone_metrics_28d['users'] > 0:
                self.pordenone_visitors_label.config(
                    text=f"{pordenone_metrics_28d['users']:,} visitors"
                )
            else:
                self.pordenone_visitors_label.config(text="No data")
            
            # Get Pordenone traffic sources (last 7 days)
            pordenone_sources = get_pordenone_traffic_sources(fvg_fetcher, days_back=7)
            
            # Update Pordenone traffic sources chart
            if pordenone_sources:
                self._update_pordenone_sources_chart(pordenone_sources)
            else:
                self._show_pordenone_no_data(self.pordenone_sources_ax, self.pordenone_sources_canvas)
            
            # Update Pordenone daily chart (multi-period)
            self._update_pordenone_daily_chart(fvg_fetcher)
                
        except Exception as e:
            print(f"[ERROR] Updating Pordenone charts: {str(e)}")
    
    def _update_pordenone_sources_chart(self, sources):
        """Update Pordenone traffic sources pie chart"""
        try:
            self.pordenone_sources_ax.clear()
            
            # Prepare data with better labels
            label_map = {
                'Organic Search': 'Search',
                'Organic Social': 'Social',
                'Direct': 'Direct',
                'Referral': 'Referral',
                'Cross-network': 'Google',
                'Paid Search': 'Ads',
                'Unassigned': 'Other'
            }
            
            labels = [label_map.get(k, k) for k in sources.keys()]
            sizes = list(sources.values())
            
            # Colors
            color_map = {
                'Search': '#34a853',
                'Social': '#4285f4',
                'Direct': '#fbbc04',
                'Referral': '#ea4335',
                'Google': '#9c27b0',
                'Ads': '#00bcd4',
                'Other': '#999999'
            }
            colors = [color_map.get(label, '#cccccc') for label in labels]
            
            # Create compact pie chart
            wedges, texts, autotexts = self.pordenone_sources_ax.pie(
                sizes, labels=labels, autopct='%1.0f%%',
                colors=colors, startangle=90,
                textprops={'fontsize': 8},
                pctdistance=0.8
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(7)
                autotext.set_weight('bold')
            
            for text in texts:
                text.set_fontsize(7)
            
            self.pordenone_sources_ax.set_title('Pordenone Traffic Sources', fontsize=9)
            self.pordenone_sources_canvas.draw()
            
        except Exception as e:
            print(f"[ERROR] Updating Pordenone sources chart: {str(e)}")
    
    def _update_pordenone_daily_chart(self, fvg_fetcher):
        """Update Pordenone with 3 time scales on x-axis, 1 y-axis for visitors"""
        try:
            from pordenone_analytics import get_pordenone_daily_traffic
            
            self.pordenone_daily_fig.clear()
            ax = self.pordenone_daily_fig.add_subplot(111)
            
            # Get data
            daily_7d = get_pordenone_daily_traffic(fvg_fetcher, days_back=7)
            daily_28d = get_pordenone_daily_traffic(fvg_fetcher, days_back=28)
            daily_90d = get_pordenone_daily_traffic(fvg_fetcher, days_back=90)
            
            # Plot on normalized 0-100% scale
            if daily_90d:
                sorted_dates = sorted(daily_90d.keys())
                users = [daily_90d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=1.5, color='#34a853', alpha=0.8, label='90d')
            
            if daily_28d:
                sorted_dates = sorted(daily_28d.keys())
                users = [daily_28d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=2, color='#4285f4', alpha=0.8, label='28d')
            
            if daily_7d:
                sorted_dates = sorted(daily_7d.keys())
                users = [daily_7d[date] for date in sorted_dates]
                x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                ax.plot(x_points, users, linewidth=2.5,
                       color='#ff9800', alpha=0.9, label='7d')
            
            # Add grey trend line for 90-day reference (no label)
            if daily_90d:
                sorted_dates = sorted(daily_90d.keys())
                users = [daily_90d[date] for date in sorted_dates]
                if len(users) > 1:
                    import numpy as np
                    x_trend = np.array([100 - (i * 100 / (len(users)-1)) for i in range(len(users))])
                    y_trend = np.array(users)
                    z = np.polyfit(x_trend, y_trend, 1)
                    p = np.poly1d(z)
                    
                    # Plot solid grey line
                    ax.plot(x_trend, p(x_trend), '-', linewidth=2,
                           color='#808080', alpha=0.6)
                    
                    # Calculate percentage change over 90 days
                    start_value = p(100)
                    end_value = p(0)
                    pct_change = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                    
                    # Add text showing percentage at the end (right side)
                    sign = '+' if pct_change > 0 else ''
                    ax.text(0.98, end_value, f'{sign}{pct_change:.1f}%',
                           color='#666', fontsize=8, weight='bold',
                           ha='left', va='center',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                    edgecolor='#999', alpha=0.8))
            
            ax.set_ylabel('Visitors', fontsize=8)
            ax.set_title('Pordenone 3-Scale', fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper left', fontsize=7)
            ax.set_xlim(100, 0)
            ax.set_xticks([])
            
            # 3 x-axis scales
            ax.text(0.00, -0.10, '7d:', transform=ax.transAxes, fontsize=7, color='#ff9800', weight='bold')
            ax.text(0.98, -0.10, '→0', transform=ax.transAxes, fontsize=6, color='#ff9800', ha='right')
            ax.text(0.00, -0.15, '28d:', transform=ax.transAxes, fontsize=7, color='#4285f4', weight='bold')
            ax.text(0.98, -0.15, '→0', transform=ax.transAxes, fontsize=6, color='#4285f4', ha='right')
            ax.text(0.00, -0.20, '90d:', transform=ax.transAxes, fontsize=7, color='#34a853', weight='bold')
            ax.text(0.98, -0.20, '→0', transform=ax.transAxes, fontsize=6, color='#34a853', ha='right')
            
            self.pordenone_daily_fig.tight_layout()
            self.pordenone_daily_canvas.draw()
            self.pordenone_daily_ax = ax
            
        except Exception as e:
            print(f"[ERROR] Updating Pordenone daily chart: {str(e)}")
    
    def _show_pordenone_no_data(self, ax, canvas):
        """Show 'no data' message for Pordenone charts"""
        ax.clear()
        ax.text(0.5, 0.5, 'No Data\nAvailable',
               ha='center', va='center', fontsize=10, color='#999')
        ax.axis('off')
        canvas.draw()
    
    def export_dashboard_data(self):
        """Export dashboard data to CSV"""
        try:
            import csv
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"analytics_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                # Export top pages data
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Page Title', 'Page Views', 'Users', 'Avg. Time (seconds)', 'Bounce Rate %'])
                    
                    for item in self.top_pages_tree.get_children():
                        values = self.top_pages_tree.item(item)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("Success", f"Dashboard data exported to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def create_site_selection(self, parent):
        """Create site selection boxes"""
        # Site 1 selection
        site1_frame = tk.LabelFrame(parent, text="Website 1", font=('Arial', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        site1_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(site1_frame, text="Domain:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 5))
        
        self.site1_entry = ttk.Entry(site1_frame, font=('Arial', 10), width=30)
        self.site1_entry.pack(padx=10, pady=(0, 5))
        self.site1_entry.insert(0, "triesteallnews.it")
        
        # Add default site selection
        tk.Label(site1_frame, text="Quick Select:", font=('Arial', 9, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(5, 0))
        self.site1_defaults = ["triesteallnews.it", "triesteprima.it", "triestecafe.it"]
        self.site1_combo = ttk.Combobox(site1_frame, values=self.site1_defaults, font=('Arial', 9), width=28, state="readonly")
        self.site1_combo.pack(padx=10, pady=(0, 5))
        self.site1_combo.set("triesteallnews.it")
        self.site1_combo.bind('<<ComboboxSelected>>', lambda e: self.site1_entry.delete(0, tk.END) or self.site1_entry.insert(0, self.site1_combo.get()))
        
        self.site1_analyze_btn = ttk.Button(site1_frame, text="Analyze Site 1", 
                                           command=lambda: self.analyze_site(1),
                                           style='Custom.TButton')
        self.site1_analyze_btn.pack(padx=10, pady=(0, 10))
        
        # Site 2 selection
        site2_frame = tk.LabelFrame(parent, text="Website 2", font=('Arial', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        site2_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(site2_frame, text="Domain:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 5))
        
        self.site2_entry = ttk.Entry(site2_frame, font=('Arial', 10), width=30)
        self.site2_entry.pack(padx=10, pady=(0, 5))
        self.site2_entry.insert(0, "triesteprima.it")
        
        # Add default site selection
        tk.Label(site2_frame, text="Quick Select:", font=('Arial', 9, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(5, 0))
        self.site2_defaults = ["triesteallnews.it", "triesteprima.it", "triestecafe.it"]
        self.site2_combo = ttk.Combobox(site2_frame, values=self.site2_defaults, font=('Arial', 9), width=28, state="readonly")
        self.site2_combo.pack(padx=10, pady=(0, 5))
        self.site2_combo.set("triesteprima.it")
        self.site2_combo.bind('<<ComboboxSelected>>', lambda e: self.site2_entry.delete(0, tk.END) or self.site2_entry.insert(0, self.site2_combo.get()))
        
        self.site2_analyze_btn = ttk.Button(site2_frame, text="Analyze Site 2", 
                                           command=lambda: self.analyze_site(2),
                                           style='Custom.TButton')
        self.site2_analyze_btn.pack(padx=10, pady=(0, 10))
        
        # Site 3 selection
        site3_frame = tk.LabelFrame(parent, text="Website 3", font=('Arial', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        site3_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(site3_frame, text="Domain:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 5))
        
        self.site3_entry = ttk.Entry(site3_frame, font=('Arial', 10), width=30)
        self.site3_entry.pack(padx=10, pady=(0, 5))
        self.site3_entry.insert(0, "triestecafe.it")
        
        # Add default site selection
        tk.Label(site3_frame, text="Quick Select:", font=('Arial', 9, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(5, 0))
        self.site3_defaults = ["triesteallnews.it", "triesteprima.it", "triestecafe.it"]
        self.site3_combo = ttk.Combobox(site3_frame, values=self.site3_defaults, font=('Arial', 9), width=28, state="readonly")
        self.site3_combo.pack(padx=10, pady=(0, 5))
        self.site3_combo.set("triestecafe.it")
        self.site3_combo.bind('<<ComboboxSelected>>', lambda e: self.site3_entry.delete(0, tk.END) or self.site3_entry.insert(0, self.site3_combo.get()))
        
        self.site3_analyze_btn = ttk.Button(site3_frame, text="Analyze Site 3", 
                                           command=lambda: self.analyze_site(3),
                                           style='Custom.TButton')
        self.site3_analyze_btn.pack(padx=10, pady=(0, 10))
    
    def create_preview_windows(self, parent):
        """Create preview windows for selected sites"""
        preview_frame = tk.LabelFrame(parent, text="Site Previews", font=('Arial', 12, 'bold'), 
                                     bg='#f0f0f0', fg='#2c3e50')
        preview_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Site 1 preview
        tk.Label(preview_frame, text="Site 1 Preview:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 5))
        
        self.site1_preview = tk.Text(preview_frame, height=6, width=40, 
                                    font=('Consolas', 9), bg='#f8f9fa', 
                                    relief='sunken', bd=1)
        self.site1_preview.pack(padx=10, pady=(0, 10), fill='x')
        
        # Site 2 preview
        tk.Label(preview_frame, text="Site 2 Preview:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(0, 5))
        
        self.site2_preview = tk.Text(preview_frame, height=6, width=40, 
                                    font=('Consolas', 9), bg='#f8f9fa', 
                                    relief='sunken', bd=1)
        self.site2_preview.pack(padx=10, pady=(0, 10), fill='x')
        
        # Site 3 preview
        tk.Label(preview_frame, text="Site 3 Preview:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(0, 5))
        
        self.site3_preview = tk.Text(preview_frame, height=6, width=40, 
                                    font=('Consolas', 9), bg='#f8f9fa', 
                                    relief='sunken', bd=1)
        self.site3_preview.pack(padx=10, pady=(0, 10), fill='x')
    
    def create_traffic_sources_section(self, parent):
        """Create traffic sources display section"""
        traffic_frame = tk.LabelFrame(parent, text="Traffic Sources Analysis", font=('Arial', 12, 'bold'), 
                                     bg='#f0f0f0', fg='#2c3e50')
        traffic_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create notebook for tabbed interface
        self.traffic_notebook = ttk.Notebook(traffic_frame)
        self.traffic_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs for each site
        self.traffic_tabs = {}
        for site_num in [1, 2, 3]:
            tab_frame = tk.Frame(self.traffic_notebook, bg='#f8f9fa')
            self.traffic_notebook.add(tab_frame, text=f"Site {site_num}")
            self.traffic_tabs[site_num] = tab_frame
            
            # Create traffic sources display for this site
            self.create_traffic_display(tab_frame, site_num)
    
    def create_traffic_display(self, parent, site_num):
        """Create traffic sources display for a specific site"""
        # Title
        title_label = tk.Label(parent, text=f"Top 3 Traffic Sources", 
                              font=('Arial', 11, 'bold'), bg='#f8f9fa', fg='#2c3e50')
        title_label.pack(pady=(10, 5))
        
        # Traffic sources list
        traffic_list_frame = tk.Frame(parent, bg='#f8f9fa')
        traffic_list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create listbox with scrollbar
        listbox_frame = tk.Frame(traffic_list_frame, bg='#f8f9fa')
        listbox_frame.pack(fill='both', expand=True)
        
        traffic_listbox = tk.Listbox(listbox_frame, font=('Consolas', 10), 
                                   bg='white', relief='sunken', bd=1, height=8)
        traffic_scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=traffic_listbox.yview)
        traffic_listbox.configure(yscrollcommand=traffic_scrollbar.set)
        
        traffic_listbox.pack(side='left', fill='both', expand=True)
        traffic_scrollbar.pack(side='right', fill='y')
        
        # Store reference to listbox
        setattr(self, f'traffic_listbox_{site_num}', traffic_listbox)
        
        # Initial placeholder text
        traffic_listbox.insert(tk.END, "No data available")
        traffic_listbox.insert(tk.END, "Analyze the website to see")
        traffic_listbox.insert(tk.END, "traffic sources breakdown")
        
        # Traffic sources summary
        summary_frame = tk.Frame(parent, bg='#f8f9fa')
        summary_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        summary_label = tk.Label(summary_frame, text="Traffic Sources Summary:", 
                                font=('Arial', 10, 'bold'), bg='#f8f9fa', fg='#2c3e50')
        summary_label.pack(anchor='w')
        
        summary_text = tk.Text(summary_frame, height=3, font=('Consolas', 9), 
                              bg='#e9ecef', relief='sunken', bd=1, wrap='word')
        summary_text.pack(fill='x', pady=(5, 0))
        summary_text.insert(tk.END, "Analyze website to see traffic sources summary")
        
        # Store reference to summary text
        setattr(self, f'traffic_summary_{site_num}', summary_text)
    
    def create_controls(self, parent):
        """Create control buttons"""
        controls_frame = tk.Frame(parent, bg='#f0f0f0')
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Compare button
        self.compare_btn = ttk.Button(controls_frame, text="🔄 Compare All Websites", 
                                     command=self.compare_websites,
                                     style='Custom.TButton')
        self.compare_btn.pack(fill='x', pady=(0, 5))
        
        # Generate monthly chart button
        self.monthly_btn = ttk.Button(controls_frame, text="📊 Generate Monthly Chart", 
                                     command=self.generate_monthly_chart,
                                     style='Custom.TButton')
        self.monthly_btn.pack(fill='x', pady=(0, 5))
        
        # Export buttons
        export_frame = tk.Frame(controls_frame, bg='#f0f0f0')
        export_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(export_frame, text="Export CSV", 
                  command=self.export_csv).pack(side='left', fill='x', expand=True, padx=(0, 2))
        ttk.Button(export_frame, text="Export JSON", 
                  command=self.export_json).pack(side='right', fill='x', expand=True, padx=(2, 0))
    
    def create_results_area(self, parent):
        """Create results display area"""
        results_frame = tk.LabelFrame(parent, text="Comparison Results", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        results_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Results text area with scrollbar
        text_frame = tk.Frame(results_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(text_frame, font=('Consolas', 9), 
                                   bg='#f8f9fa', relief='sunken', bd=1)
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_charts_area(self, parent):
        """Create charts display area"""
        charts_frame = tk.LabelFrame(parent, text="Monthly Comparison Charts", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        charts_frame.pack(fill='both', expand=True)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, charts_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial empty chart
        self.show_empty_chart()
    
    def show_empty_chart(self):
        """Show empty chart placeholder"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Analyze websites to see automatic monthly charts', 
                ha='center', va='center', fontsize=14, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
    
    def analyze_site(self, site_num):
        """Analyze a single site"""
        if site_num == 1:
            entry = self.site1_entry
            preview = self.site1_preview
            btn = self.site1_analyze_btn
        elif site_num == 2:
            entry = self.site2_entry
            preview = self.site2_preview
            btn = self.site2_analyze_btn
        else:  # site_num == 3
            entry = self.site3_entry
            preview = self.site3_preview
            btn = self.site3_analyze_btn
        
        domain = entry.get().strip().lower()
        if not domain:
            messagebox.showerror("Error", "Please enter a domain name")
            return
        
        # Clean domain name
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
        
        btn.config(text="Analyzing...", state='disabled')
        preview.delete(1.0, tk.END)
        preview.insert(tk.END, f"Analyzing {domain}...\nPlease wait...")
        
        def analyze_thread():
            try:
                tool = WebRankingTool()
                results = tool.compare_websites([domain])
                metrics = results[domain][0]  # Get first result
                
                # Store data
                if site_num == 1:
                    self.site1_data = metrics
                elif site_num == 2:
                    self.site2_data = metrics
                else:  # site_num == 3
                    self.site3_data = metrics
                
                # Update preview
                preview_text = self.format_metrics_preview(metrics)
                self.root.after(0, lambda: self.update_preview(preview, preview_text, btn))
                
                # Automatically generate combined monthly chart for all analyzed sites
                self.root.after(0, lambda: self.auto_generate_combined_chart())
                
            except Exception as e:
                error_msg = f"Error analyzing {domain}: {str(e)}"
                self.root.after(0, lambda: self.update_preview(preview, error_msg, btn))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def update_preview(self, preview, text, btn):
        """Update preview text and button state"""
        preview.delete(1.0, tk.END)
        preview.insert(tk.END, text)
        btn.config(text="Analyze Site", state='normal')
    
    def auto_generate_combined_chart(self):
        """Automatically generate combined monthly chart for all analyzed sites"""
        try:
            # Collect all analyzed sites
            sites_analyzed = []
            if self.site1_data:
                sites_analyzed.append((1, self.site1_data))
            if self.site2_data:
                sites_analyzed.append((2, self.site2_data))
            if self.site3_data:
                sites_analyzed.append((3, self.site3_data))
            
            if len(sites_analyzed) == 0:
                # Show empty chart if no sites analyzed
                self.show_empty_chart()
                return
            
            # Generate combined historical data
            historical_data = self.generate_combined_historical_data(sites_analyzed)
            
            # Create combined chart
            self.create_combined_monthly_chart(historical_data, sites_analyzed)
            
        except Exception as e:
            print(f"Error generating combined chart: {e}")
    
    def generate_combined_historical_data(self, sites_analyzed):
        """Generate 12 months of estimated historical data for all analyzed sites - based on current analysis"""
        months = []
        sites_visits = {}
        sites_ranks = {}
        
        # Generate data for last 12 months
        for i in range(12):
            date = datetime.now() - timedelta(days=30 * i)
            months.append(date.strftime('%Y-%m'))
            
            # Generate data for each analyzed site
            for site_num, site_data in sites_analyzed:
                base_visits = site_data.monthly_visits or 1000000
                base_rank = site_data.global_rank or 10000
                
                # Use domain hash for consistent variation
                domain_hash = hash(site_data.domain) % 1000000
                
                # Add realistic seasonal variation and growth trends
                # More realistic variation: 10-30% monthly fluctuation
                seasonal_factor = 1 + 0.1 * np.sin(i * np.pi / 6)  # Seasonal variation
                growth_factor = 1 + (i * 0.02)  # Slight growth trend over time
                random_factor = 1 + (domain_hash * 0.000001) % 0.2 - 0.1  # Random variation
                
                variation = seasonal_factor * growth_factor * random_factor
                rank_variation = 1 + 0.1 * np.sin(i * np.pi / 4) + (domain_hash * 0.0000005) % 0.1 - 0.05
                
                if site_num not in sites_visits:
                    sites_visits[site_num] = []
                    sites_ranks[site_num] = []
                
                sites_visits[site_num].append(int(base_visits * variation))
                sites_ranks[site_num].append(int(base_rank * rank_variation))
        
        # Reverse to show chronological order (oldest to newest)
        months.reverse()
        for site_num in sites_visits:
            sites_visits[site_num].reverse()
            sites_ranks[site_num].reverse()
        
        return {
            'months': months,
            'sites_visits': sites_visits,
            'sites_ranks': sites_ranks,
            'sites_analyzed': sites_analyzed
        }
    
    def create_combined_monthly_chart(self, data, sites_analyzed):
        """Create combined monthly chart for all analyzed sites"""
        try:
            self.fig.clear()
            
            # Create subplots
            ax1 = self.fig.add_subplot(2, 1, 1)
            ax2 = self.fig.add_subplot(2, 1, 2)
            
            # Define colors and markers for different sites
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            markers = ['o', 's', '^', 'D', 'v', '<']
            
            # Chart 1: Monthly Visits
            for i, (site_num, site_data) in enumerate(sites_analyzed):
                color = colors[i % len(colors)]
                marker = markers[i % len(markers)]
                ax1.plot(data['months'], data['sites_visits'][site_num], 
                        color=color, marker=marker, linestyle='-', label=f"{site_data.domain}", 
                        linewidth=2, markersize=6)
            
            ax1.set_title('Monthly Visits Comparison (12 Months) - Estimated Data', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Monthly Visits', fontsize=12)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
            
            # Chart 2: Global Rankings
            for i, (site_num, site_data) in enumerate(sites_analyzed):
                color = colors[i % len(colors)]
                marker = markers[i % len(markers)]
                ax2.plot(data['months'], data['sites_ranks'][site_num], 
                        color=color, marker=marker, linestyle='-', label=f"{site_data.domain}", 
                        linewidth=2, markersize=6)
            
            ax2.set_title('Global Ranking Comparison (12 Months) - Estimated Data', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Global Rank (Lower is Better)', fontsize=12)
            ax2.set_xlabel('Month', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            
            # Format y-axis for visits (add commas)
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            # Format y-axis for ranks (add commas)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            # Adjust layout
            self.fig.tight_layout()
            self.canvas.draw()
            
            print(f"Combined chart generated successfully for {len(sites_analyzed)} sites")
            
        except Exception as e:
            print(f"Error creating combined chart: {e}")
            # Show error message in chart area
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Error generating combined chart:\n{str(e)}', 
                    ha='center', va='center', fontsize=12, color='red')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
    
    def generate_single_site_historical_data(self, site_num, metrics):
        """Generate 12 months of historical data for a single site"""
        months = []
        visits_data = []
        ranks_data = []
        
        # Generate data for last 12 months
        for i in range(12):
            date = datetime.now() - timedelta(days=30 * i)
            months.append(date.strftime('%Y-%m'))
            
            # Generate data based on current metrics
            base_visits = metrics.monthly_visits or 1000000
            base_rank = metrics.global_rank or 10000
            
            # Add seasonal variation and random fluctuation
            variation = 1 + 0.2 * np.sin(i * np.pi / 6) + np.random.normal(0, 0.1)
            rank_variation = 1 + 0.15 * np.sin(i * np.pi / 4) + np.random.normal(0, 0.05)
            
            visits_data.append(int(base_visits * variation))
            ranks_data.append(int(base_rank * rank_variation))
        
        # Reverse to show chronological order
        months.reverse()
        visits_data.reverse()
        ranks_data.reverse()
        
        return {
            'months': months,
            'visits': visits_data,
            'ranks': ranks_data,
            'site_num': site_num,
            'domain': metrics.domain
        }
    
    def create_single_site_monthly_chart(self, data, site_num, metrics):
        """Create monthly chart for a single site"""
        try:
            self.fig.clear()
            
            # Create subplots
            ax1 = self.fig.add_subplot(2, 1, 1)
            ax2 = self.fig.add_subplot(2, 1, 2)
            
            # Define colors for different sites
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            color = colors[(site_num - 1) % len(colors)]
            
            # Chart 1: Monthly Visits
            ax1.plot(data['months'], data['visits'], 
                    color=color, marker='o', linestyle='-', label=f"{metrics.domain}", 
                    linewidth=2, markersize=6)
            
            ax1.set_title(f'Monthly Visits Trend - {metrics.domain.upper()}', 
                         fontsize=14, fontweight='bold')
            ax1.set_ylabel('Monthly Visits', fontsize=12)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
            
            # Chart 2: Global Rankings
            ax2.plot(data['months'], data['ranks'], 
                    color=color, marker='s', linestyle='-', label=f"{metrics.domain}", 
                    linewidth=2, markersize=6)
            
            ax2.set_title(f'Global Ranking Trend - {metrics.domain.upper()}', 
                         fontsize=14, fontweight='bold')
            ax2.set_ylabel('Global Rank (Lower is Better)', fontsize=12)
            ax2.set_xlabel('Month', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            
            # Format y-axis for visits (add commas)
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            # Format y-axis for ranks (add commas)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            # Adjust layout
            self.fig.tight_layout()
            self.canvas.draw()
            
            print(f"Chart generated successfully for {metrics.domain}")
            
        except Exception as e:
            print(f"Error creating chart for {metrics.domain}: {e}")
            # Show error message in chart area
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Error generating chart for {metrics.domain}:\n{str(e)}', 
                    ha='center', va='center', fontsize=12, color='red')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
    
    def format_metrics_preview(self, metrics):
        """Format metrics for preview display"""
        preview = f"Domain: {metrics.domain}\n"
        # Add data type indicator based on actual data source
        if "Mock" in metrics.data_source or "mock" in metrics.data_source.lower():
            data_type = "MOCK DATA"
        else:
            data_type = "REAL DATA"
        preview += f"Data Source: {metrics.data_source} ({data_type})\n"
        preview += f"Global Rank: {metrics.global_rank:,}\n" if metrics.global_rank else "Global Rank: N/A\n"
        preview += f"Country Rank: {metrics.country_rank:,}\n" if metrics.country_rank else "Country Rank: N/A\n"
        preview += f"Monthly Visits: {metrics.monthly_visits:,}\n" if metrics.monthly_visits else "Monthly Visits: N/A\n"
        preview += f"Bounce Rate: {metrics.bounce_rate:.1f}%\n" if metrics.bounce_rate else "Bounce Rate: N/A\n"
        preview += f"Visit Duration: {metrics.avg_visit_duration:.1f}s\n" if metrics.avg_visit_duration else "Visit Duration: N/A\n"
        preview += f"Pages per Visit: {metrics.pages_per_visit:.1f}\n" if metrics.pages_per_visit else "Pages per Visit: N/A\n"
        return preview
    
    def compare_websites(self):
        """Compare the selected websites"""
        sites_analyzed = []
        if self.site1_data:
            sites_analyzed.append(1)
        if self.site2_data:
            sites_analyzed.append(2)
        if self.site3_data:
            sites_analyzed.append(3)
        
        if len(sites_analyzed) < 2:
            messagebox.showerror("Error", "Please analyze at least 2 sites first")
            return
        
        self.compare_btn.config(text="Comparing...", state='disabled')
        
        def compare_thread():
            try:
                # Generate comparison report
                comparison = self.generate_comparison_report()
                
                # Update results display
                self.root.after(0, lambda: self.update_results(comparison))
                
            except Exception as e:
                error_msg = f"Error during comparison: {str(e)}"
                self.root.after(0, lambda: self.update_results(error_msg))
        
        threading.Thread(target=compare_thread, daemon=True).start()
    
    def generate_comparison_report(self):
        """Generate detailed comparison report"""
        report = "=" * 80 + "\n"
        report += "MEDIAIMMAGINE WEB RANKING COMPARISON REPORT\n"
        report += "=" * 80 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 80 + "\n\n"
        
        # Collect all analyzed sites
        sites_data = []
        if self.site1_data:
            sites_data.append((1, self.site1_data))
        if self.site2_data:
            sites_data.append((2, self.site2_data))
        if self.site3_data:
            sites_data.append((3, self.site3_data))
        
        # Generate report for each site
        for site_num, site_data in sites_data:
            report += f"🌐 {site_data.domain.upper()}\n"
            report += "-" * 50 + "\n"
            report += f"Data Source: {site_data.data_source}\n"
            report += f"Global Rank: {site_data.global_rank:,}\n" if site_data.global_rank else "Global Rank: N/A\n"
            report += f"Country Rank: {site_data.country_rank:,}\n" if site_data.country_rank else "Country Rank: N/A\n"
            report += f"Monthly Visits: {site_data.monthly_visits:,}\n" if site_data.monthly_visits else "Monthly Visits: N/A\n"
            report += f"Bounce Rate: {site_data.bounce_rate:.1f}%\n" if site_data.bounce_rate else "Bounce Rate: N/A\n"
            report += f"Avg Visit Duration: {site_data.avg_visit_duration:.1f}s\n" if site_data.avg_visit_duration else "Avg Visit Duration: N/A\n"
            report += f"Pages per Visit: {site_data.pages_per_visit:.1f}\n" if site_data.pages_per_visit else "Pages per Visit: N/A\n"
            
            if site_data.traffic_sources:
                report += "\nTraffic Sources:\n"
                for source, percentage in site_data.traffic_sources.items():
                    report += f"  {source}: {percentage:.1f}%\n"
            
            report += "\n" + "=" * 50 + "\n\n"
        
        # Summary comparison
        report += "\n" + "=" * 80 + "\n"
        report += "SUMMARY COMPARISON\n"
        report += "=" * 80 + "\n"
        
        # Find best performers
        if sites_data:
            # Best global rank (lowest number)
            valid_ranks = [(site_data.domain, site_data.global_rank) for _, site_data in sites_data if site_data.global_rank]
            if valid_ranks:
                best_rank_domain = min(valid_ranks, key=lambda x: x[1])[0]
                report += f"Best Global Rank: {best_rank_domain}\n"
            
            # Most monthly visits
            valid_visits = [(site_data.domain, site_data.monthly_visits) for _, site_data in sites_data if site_data.monthly_visits]
            if valid_visits:
                most_visits_domain = max(valid_visits, key=lambda x: x[1])[0]
                report += f"Most Monthly Visits: {most_visits_domain}\n"
            
            # Lowest bounce rate
            valid_bounce = [(site_data.domain, site_data.bounce_rate) for _, site_data in sites_data if site_data.bounce_rate]
            if valid_bounce:
                lowest_bounce_domain = min(valid_bounce, key=lambda x: x[1])[0]
                report += f"Lowest Bounce Rate: {lowest_bounce_domain}\n"
            
            # Longest visit duration
            valid_duration = [(site_data.domain, site_data.avg_visit_duration) for _, site_data in sites_data if site_data.avg_visit_duration]
            if valid_duration:
                longest_duration_domain = max(valid_duration, key=lambda x: x[1])[0]
                report += f"Longest Visit Duration: {longest_duration_domain}\n"
        
        return report
    
    def update_results(self, text):
        """Update results display"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        self.compare_btn.config(text="🔄 Compare All Websites", state='normal')
    
    def generate_monthly_chart(self):
        """Generate 12-month comparison chart"""
        sites_analyzed = []
        if self.site1_data:
            sites_analyzed.append((1, self.site1_data))
        if self.site2_data:
            sites_analyzed.append((2, self.site2_data))
        if self.site3_data:
            sites_analyzed.append((3, self.site3_data))
        
        if len(sites_analyzed) < 1:
            messagebox.showerror("Error", "Please analyze at least 1 site first")
            return
        
        self.monthly_btn.config(text="Generating...", state='disabled')
        
        def chart_thread():
            try:
                # Generate historical data
                historical_data = self.generate_combined_historical_data(sites_analyzed)
                
                # Create chart
                self.root.after(0, lambda: self.create_combined_monthly_chart(historical_data, sites_analyzed))
                
            except Exception as e:
                error_msg = f"Error generating chart: {str(e)}"
                self.root.after(0, lambda: self.update_chart_error(error_msg))
        
        threading.Thread(target=chart_thread, daemon=True).start()
    
    def generate_historical_data(self, sites_analyzed):
        """Generate 12 months of historical data"""
        months = []
        sites_visits = {}
        sites_ranks = {}
        
        # Generate data for last 12 months
        for i in range(12):
            date = datetime.now() - timedelta(days=30 * i)
            months.append(date.strftime('%Y-%m'))
            
            # Generate data for each analyzed site
            for site_num, site_data in sites_analyzed:
                base_visits = site_data.monthly_visits or 1000000
                base_rank = site_data.global_rank or 10000
                
                # Add seasonal variation and random fluctuation
                variation = 1 + 0.2 * np.sin(i * np.pi / 6) + np.random.normal(0, 0.1)
                rank_variation = 1 + 0.15 * np.sin(i * np.pi / 4) + np.random.normal(0, 0.05)
                
                if site_num not in sites_visits:
                    sites_visits[site_num] = []
                    sites_ranks[site_num] = []
                
                sites_visits[site_num].append(int(base_visits * variation))
                sites_ranks[site_num].append(int(base_rank * rank_variation))
        
        # Reverse to show chronological order
        months.reverse()
        for site_num in sites_visits:
            sites_visits[site_num].reverse()
            sites_ranks[site_num].reverse()
        
        return {
            'months': months,
            'sites_visits': sites_visits,
            'sites_ranks': sites_ranks,
            'sites_analyzed': sites_analyzed
        }
    
    def create_monthly_chart(self, data, sites_analyzed):
        """Create the monthly comparison chart"""
        self.fig.clear()
        
        # Create subplots
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 1, 2)
        
        # Define colors and markers for different sites
        colors = ['b', 'r', 'g', 'm', 'c', 'y']
        markers = ['o', 's', '^', 'D', 'v', '<']
        
        # Chart 1: Monthly Visits
        for i, (site_num, site_data) in enumerate(sites_analyzed):
            color = colors[i % len(colors)]
            marker = markers[i % len(markers)]
            ax1.plot(data['months'], data['sites_visits'][site_num], 
                    color=color, marker=marker, linestyle='-', label=f"{site_data.domain}", 
                    linewidth=2, markersize=6)
        
        ax1.set_title('Monthly Visits Comparison (12 Months)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Monthly Visits', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Chart 2: Global Rankings
        for i, (site_num, site_data) in enumerate(sites_analyzed):
            color = colors[i % len(colors)]
            marker = markers[i % len(markers)]
            ax2.plot(data['months'], data['sites_ranks'][site_num], 
                    color=color, marker=marker, linestyle='-', label=f"{site_data.domain}", 
                    linewidth=2, markersize=6)
        
        ax2.set_title('Global Ranking Comparison (12 Months)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Global Rank (Lower is Better)', fontsize=12)
        ax2.set_xlabel('Month', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # Format y-axis for visits (add commas)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
        
        # Format y-axis for ranks (add commas)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
        
        # Adjust layout
        self.fig.tight_layout()
        self.canvas.draw()
        
        self.monthly_btn.config(text="📊 Generate Monthly Chart", state='normal')
    
    def update_chart_error(self, error_msg):
        """Update chart with error message"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, error_msg, ha='center', va='center', fontsize=12, color='red')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
        
        self.monthly_btn.config(text="📊 Generate Monthly Chart", state='normal')
    
    def export_csv(self):
        """Export results to CSV"""
        sites_analyzed = []
        if self.site1_data:
            sites_analyzed.append((1, self.site1_data))
        if self.site2_data:
            sites_analyzed.append((2, self.site2_data))
        if self.site3_data:
            sites_analyzed.append((3, self.site3_data))
        
        if len(sites_analyzed) < 2:
            messagebox.showerror("Error", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Metric', 'Site 1', 'Site 2', 'Winner']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    # Create comparison table for all sites
                    metric_names = ['Global Rank', 'Country Rank', 'Monthly Visits', 'Bounce Rate', 'Visit Duration', 'Pages per Visit']
                    
                    # Write header with all sites
                    header = ['Metric'] + [f'Site {site_num} ({site_data.domain})' for site_num, site_data in sites_analyzed] + ['Winner']
                    writer.writerow(header)
                    
                    # Compare each metric
                    for metric_name in metric_names:
                        values = []
                        for site_num, site_data in sites_analyzed:
                            if metric_name == 'Global Rank':
                                val = site_data.global_rank
                            elif metric_name == 'Country Rank':
                                val = site_data.country_rank
                            elif metric_name == 'Monthly Visits':
                                val = site_data.monthly_visits
                            elif metric_name == 'Bounce Rate':
                                val = site_data.bounce_rate
                            elif metric_name == 'Visit Duration':
                                val = site_data.avg_visit_duration
                            elif metric_name == 'Pages per Visit':
                                val = site_data.pages_per_visit
                            else:
                                val = None
                            values.append(val)
                        
                        # Find winner
                        valid_values = [(i, val) for i, val in enumerate(values) if val is not None]
                        if valid_values:
                            if 'Rank' in metric_name:  # Lower is better
                                winner_idx, _ = min(valid_values, key=lambda x: x[1])
                            else:  # Higher is better
                                winner_idx, _ = max(valid_values, key=lambda x: x[1])
                            winner = sites_analyzed[winner_idx][1].domain
                        else:
                            winner = 'N/A'
                        
                        # Write row
                        row = [metric_name] + [val if val is not None else 'N/A' for val in values] + [winner]
                        writer.writerow(dict(zip(header, row)))
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")
    
    def export_json(self):
        """Export results to JSON"""
        sites_analyzed = []
        if self.site1_data:
            sites_analyzed.append((1, self.site1_data))
        if self.site2_data:
            sites_analyzed.append((2, self.site2_data))
        if self.site3_data:
            sites_analyzed.append((3, self.site3_data))
        
        if len(sites_analyzed) < 2:
            messagebox.showerror("Error", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = {
                    'comparison_date': datetime.now().isoformat(),
                    'sites': {}
                }
                
                # Add data for each analyzed site
                for site_num, site_data in sites_analyzed:
                    data['sites'][f'site{site_num}'] = {
                        'domain': site_data.domain,
                        'global_rank': site_data.global_rank,
                        'country_rank': site_data.country_rank,
                        'monthly_visits': site_data.monthly_visits,
                        'bounce_rate': site_data.bounce_rate,
                        'avg_visit_duration': site_data.avg_visit_duration,
                        'pages_per_visit': site_data.pages_per_visit,
                        'data_source': site_data.data_source
                    }
                
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")
    def create_marketing_dashboard_tab(self):
        """Create the Page Visits & Impressions dashboard (Cloudflare-based)"""
        # Marketing dashboard tab
        marketing_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(marketing_tab, text="📊 Page Visits & Impressions (CF)")
        
        # Create scrollable canvas
        canvas = tk.Canvas(marketing_tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(marketing_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main container
        main_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Info banner
        info_frame = tk.Frame(main_container, bg='#fff3cd', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 10))
        
        info_icon = tk.Label(info_frame, text="💼", font=('Arial', 14), bg='#fff3cd')
        info_icon.pack(side='left', padx=(10, 5), pady=8)
        
        info_text = tk.Label(info_frame, 
                            text="Marketing Metrics: Total page visits & ad impressions from Cloudflare (bot-filtered)",
                            font=('Arial', 10, 'bold'), bg='#fff3cd', fg='#856404', anchor='w')
        info_text.pack(side='left', padx=(0, 10), pady=8, fill='x', expand=True)
        
        self.marketing_info_label = tk.Label(info_frame, 
                                             text="Last 28 days",
                                             font=('Arial', 9, 'bold'), bg='#fff3cd', fg='#856404')
        self.marketing_info_label.pack(side='right', padx=(0, 10), pady=8)
        
        # Metrics cards
        metrics_frame = tk.Frame(main_container, bg='#f0f0f0')
        metrics_frame.pack(fill='x', pady=(0, 10))
        
        self.create_marketing_metric_card(metrics_frame, "Total Page Visits", "0", "#ff9800", 0)
        self.create_marketing_metric_card(metrics_frame, "Ad Impressions", "0", "#9c27b0", 1)
        self.create_marketing_metric_card(metrics_frame, "Image Views", "0", "#00bcd4", 2)
        self.create_marketing_metric_card(metrics_frame, "Unique Visitors", "0", "#4caf50", 3)
        
        # Comparison section
        comparison_frame = tk.LabelFrame(main_container, text="📊 Marketing vs Content Analytics Comparison",
                                        font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        comparison_frame.pack(fill='x', pady=(0, 10))
        
        # Create comparison table
        comp_container = tk.Frame(comparison_frame, bg='white', relief='solid', bd=1)
        comp_container.pack(fill='x', padx=10, pady=10)
        
        # Headers
        headers_frame = tk.Frame(comp_container, bg='#f8f9fa')
        headers_frame.pack(fill='x')
        
        tk.Label(headers_frame, text="Metric", font=('Arial', 10, 'bold'),
                bg='#f8f9fa', width=25, anchor='w').grid(row=0, column=0, padx=10, pady=8, sticky='w')
        tk.Label(headers_frame, text="Page Visits (CF)", font=('Arial', 10, 'bold'),
                bg='#f8f9fa', fg='#ff9800', width=20).grid(row=0, column=1, padx=10, pady=8)
        tk.Label(headers_frame, text="Article Visits (GA)", font=('Arial', 10, 'bold'),
                bg='#f8f9fa', fg='#4285f4', width=20).grid(row=0, column=2, padx=10, pady=8)
        tk.Label(headers_frame, text="Difference", font=('Arial', 10, 'bold'),
                bg='#f8f9fa', width=15).grid(row=0, column=3, padx=10, pady=8)
        
        # Data rows
        self.marketing_comparison_data = tk.Frame(comp_container, bg='white')
        self.marketing_comparison_data.pack(fill='x', padx=10, pady=5)
        
        # Explanation section
        explain_frame = tk.LabelFrame(main_container, text="💡 Understanding the Metrics",
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        explain_frame.pack(fill='x', pady=(0, 10))
        
        explain_text = tk.Text(explain_frame, height=10, wrap=tk.WORD, font=('Arial', 9),
                              bg='#f8f9fa', relief='flat', padx=15, pady=10)
        explain_text.pack(fill='x', padx=10, pady=10)
        
        explanation = """📖 Article Visits (Google Analytics):
• Tracks users who read article CONTENT
• JavaScript-based tracking
• Measures engagement (time, bounce, sources)
• ~35% of total visitors (ad blockers reduce this)
• USE FOR: Editorial strategy, content performance

📊 Page Visits (Cloudflare - Bot Filtered):
• Tracks ALL page loads (HTML + assets)
• Includes ad impressions delivered
• Includes image views (even if ad-blocked)
• ~100% of human traffic (bots filtered)
• USE FOR: Marketing reach, ad sales, sponsor reporting

💼 Why Both Matter:
• Ad impression was DELIVERED (CF counts it)
• User may have ad blocker (GA doesn't count it)
• Both metrics are TRUE for different purposes!
• Marketing: Use CF for CPM/impressions
• Content: Use GA for engagement/performance"""
        
        explain_text.insert('1.0', explanation)
        explain_text.config(state='disabled')
        
        # Global charts section (similar to GA dashboard)
        global_charts_frame = tk.LabelFrame(main_container, text="🌐 Overall Marketing Metrics (All Sites)",
                                           font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        global_charts_frame.pack(fill='x', pady=(0, 10))
        
        charts_container = tk.Frame(global_charts_frame, bg='#f0f0f0')
        charts_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure columns
        charts_container.grid_columnconfigure(0, weight=1)
        charts_container.grid_columnconfigure(1, weight=2)
        
        # Left - Traffic type pie chart
        traffic_type_frame = tk.LabelFrame(charts_container, text="Traffic Breakdown",
                                          font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        traffic_type_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        from matplotlib.figure import Figure
        self.marketing_traffic_fig = Figure(figsize=(5, 4), dpi=100)
        self.marketing_traffic_ax = self.marketing_traffic_fig.add_subplot(111)
        self.marketing_traffic_canvas = FigureCanvasTkAgg(self.marketing_traffic_fig, traffic_type_frame)
        self.marketing_traffic_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Right - Daily visits multi-period
        daily_marketing_frame = tk.LabelFrame(charts_container, text="Daily Page Visits - Multi-Period (3 Scales)",
                                             font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        daily_marketing_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.marketing_daily_fig = Figure(figsize=(9, 5), dpi=100)
        self.marketing_daily_ax = self.marketing_daily_fig.add_subplot(111)
        self.marketing_daily_canvas = FigureCanvasTkAgg(self.marketing_daily_fig, daily_marketing_frame)
        self.marketing_daily_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Trieste section
        trieste_marketing_section = tk.LabelFrame(main_container, text="📍 TRIESTE.NEWS / TRIESTEALLNEWS.IT - Marketing Metrics",
                                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        trieste_marketing_section.pack(fill='x', pady=(10, 10))
        
        # Trieste header with metrics
        trieste_mkt_header = tk.Frame(trieste_marketing_section, bg='#f0f0f0')
        trieste_mkt_header.pack(fill='x', padx=10, pady=(10, 5))
        
        trieste_mkt_metrics_frame = tk.Frame(trieste_mkt_header, bg='#e3f2fd', relief='solid', bd=1)
        trieste_mkt_metrics_frame.pack(side='left', padx=(0, 10))
        
        tk.Label(trieste_mkt_metrics_frame, text="Last 28 Days - Page Visits:", font=('Arial', 9, 'bold'),
                bg='#e3f2fd', fg='#1976d2').pack(side='left', padx=(10, 5), pady=5)
        
        self.trieste_marketing_visits_label = tk.Label(trieste_mkt_metrics_frame, text="Loading...",
                                                       font=('Arial', 11, 'bold'),
                                                       bg='#e3f2fd', fg='#4285f4')
        self.trieste_marketing_visits_label.pack(side='left', padx=(0, 10), pady=5)
        
        trieste_mkt_charts = tk.Frame(trieste_marketing_section, bg='#f0f0f0')
        trieste_mkt_charts.pack(fill='both', expand=True, padx=10, pady=10)
        
        trieste_mkt_charts.grid_columnconfigure(0, weight=1)
        trieste_mkt_charts.grid_columnconfigure(1, weight=2)
        
        # Trieste charts (placeholder - will be populated with CF data)
        trieste_mkt_pie_frame = tk.LabelFrame(trieste_mkt_charts, text="Impression Types",
                                             font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        trieste_mkt_pie_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        self.trieste_mkt_pie_fig = Figure(figsize=(4, 3), dpi=100)
        self.trieste_mkt_pie_ax = self.trieste_mkt_pie_fig.add_subplot(111)
        self.trieste_mkt_pie_canvas = FigureCanvasTkAgg(self.trieste_mkt_pie_fig, trieste_mkt_pie_frame)
        self.trieste_mkt_pie_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        trieste_mkt_daily_frame = tk.LabelFrame(trieste_mkt_charts, text="Daily Page Visits - Multi-Period (3 Scales)",
                                               font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        trieste_mkt_daily_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.trieste_mkt_daily_fig = Figure(figsize=(8, 4), dpi=100)
        self.trieste_mkt_daily_ax = self.trieste_mkt_daily_fig.add_subplot(111)
        self.trieste_mkt_daily_canvas = FigureCanvasTkAgg(self.trieste_mkt_daily_fig, trieste_mkt_daily_frame)
        self.trieste_mkt_daily_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pordenone section
        pordenone_marketing_section = tk.LabelFrame(main_container, text="📍 PORDENONEOGGI.IT - Marketing Metrics",
                                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pordenone_marketing_section.pack(fill='x', pady=(10, 10))
        
        # Pordenone header
        pordenone_mkt_header = tk.Frame(pordenone_marketing_section, bg='#f0f0f0')
        pordenone_mkt_header.pack(fill='x', padx=10, pady=(10, 5))
        
        pordenone_mkt_metrics_frame = tk.Frame(pordenone_mkt_header, bg='#ffebee', relief='solid', bd=1)
        pordenone_mkt_metrics_frame.pack(side='left', padx=(0, 10))
        
        tk.Label(pordenone_mkt_metrics_frame, text="Last 28 Days - Page Visits:", font=('Arial', 9, 'bold'),
                bg='#ffebee', fg='#c62828').pack(side='left', padx=(10, 5), pady=5)
        
        self.pordenone_marketing_visits_label = tk.Label(pordenone_mkt_metrics_frame, text="Loading...",
                                                         font=('Arial', 11, 'bold'),
                                                         bg='#ffebee', fg='#ea4335')
        self.pordenone_marketing_visits_label.pack(side='left', padx=(0, 10), pady=5)
        
        pordenone_mkt_charts = tk.Frame(pordenone_marketing_section, bg='#f0f0f0')
        pordenone_mkt_charts.pack(fill='both', expand=True, padx=10, pady=10)
        
        pordenone_mkt_charts.grid_columnconfigure(0, weight=1)
        pordenone_mkt_charts.grid_columnconfigure(1, weight=2)
        
        # Pordenone charts
        pordenone_mkt_pie_frame = tk.LabelFrame(pordenone_mkt_charts, text="Impression Types",
                                               font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pordenone_mkt_pie_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        self.pordenone_mkt_pie_fig = Figure(figsize=(4, 3), dpi=100)
        self.pordenone_mkt_pie_ax = self.pordenone_mkt_pie_fig.add_subplot(111)
        self.pordenone_mkt_pie_canvas = FigureCanvasTkAgg(self.pordenone_mkt_pie_fig, pordenone_mkt_pie_frame)
        self.pordenone_mkt_pie_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        pordenone_mkt_daily_frame = tk.LabelFrame(pordenone_mkt_charts, text="Daily Page Visits - Multi-Period (3 Scales)",
                                                 font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        pordenone_mkt_daily_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.pordenone_mkt_daily_fig = Figure(figsize=(8, 4), dpi=100)
        self.pordenone_mkt_daily_ax = self.pordenone_mkt_daily_fig.add_subplot(111)
        self.pordenone_mkt_daily_canvas = FigureCanvasTkAgg(self.pordenone_mkt_daily_fig, pordenone_mkt_daily_frame)
        self.pordenone_mkt_daily_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Control buttons
        controls_frame = tk.Frame(main_container, bg='#f0f0f0')
        controls_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(controls_frame, text="🔄 Refresh Marketing Data", 
                  command=self.refresh_marketing_dashboard,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        self.marketing_status = tk.Label(controls_frame, text="Ready to load data", 
                                        font=('Arial', 9), bg='#f0f0f0', fg='#666')
        self.marketing_status.pack(side='right', padx=10)
        
        # Initial load
        self.refresh_marketing_dashboard()
    
    def create_marketing_metric_card(self, parent, title, value, color, column):
        """Create a marketing metric card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        card.grid(row=0, column=column, padx=5, pady=5, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        
        tk.Label(card, text=title, font=('Arial', 10), 
                bg='white', fg='#666').pack(pady=(15, 5))
        
        value_label = tk.Label(card, text=value, font=('Arial', 24, 'bold'), 
                              bg='white', fg=color)
        value_label.pack(pady=(0, 15))
        
        # Store reference
        attr_name = f'marketing_metric_{title.lower().replace(" ", "_")}'
        setattr(self, attr_name, value_label)
    
    def refresh_marketing_dashboard(self):
        """Refresh marketing dashboard with Cloudflare data"""
        self.marketing_status.config(text="Loading Cloudflare data...", fg='#f39c12')
        self.root.update()
        
        def fetch_data():
            try:
                from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID
                from cloudflare_marketing_analytics import CloudflareMarketingAnalytics
                from google_analytics_fetcher import load_config
                from multi_property_analytics import MultiPropertyAnalytics
                from trieste_analytics import get_trieste_metrics
                from pordenone_analytics import get_pordenone_metrics
                
                # Get Cloudflare marketing data (28 days)
                cf_analytics = CloudflareMarketingAnalytics(CLOUDFLARE_ZONE_ID, CLOUDFLARE_API_TOKEN)
                cf_data_28d = cf_analytics.get_total_visits(days_back=28)
                cf_data_7d = cf_analytics.get_total_visits(days_back=7)
                cf_data_90d = cf_analytics.get_total_visits(days_back=90)
                
                if cf_data_28d:
                    # Update metric cards
                    self.marketing_metric_total_page_visits.config(
                        text=f"{cf_data_28d['estimated_html_pages']:,}"
                    )
                    self.marketing_metric_ad_impressions.config(
                        text=f"{cf_data_28d['estimated_ad_impressions']:,}"
                    )
                    self.marketing_metric_image_views.config(
                        text=f"{cf_data_28d['estimated_image_impressions']:,}"
                    )
                    self.marketing_metric_unique_visitors.config(
                        text=f"{cf_data_28d['human_uniques']:,}"
                    )
                    
                    # Update comparison table
                    self._update_marketing_comparison(cf_data_28d)
                    
                    # Update charts
                    self._update_marketing_charts(cf_data_7d, cf_data_28d, cf_data_90d)
                    
                    self.marketing_status.config(
                        text=f"Last updated: {datetime.now().strftime('%H:%M:%S')} - Cloudflare Zone Data (Bot-Filtered)", 
                        fg='#27ae60'
                    )
                else:
                    self.marketing_status.config(
                        text="Error loading Cloudflare data", 
                        fg='#e74c3c'
                    )
                    
            except Exception as e:
                self.marketing_status.config(
                    text=f"Error: {str(e)[:50]}", 
                    fg='#e74c3c'
                )
                print(f"[ERROR] Marketing dashboard: {str(e)}")
        
        # Run in thread
        thread = threading.Thread(target=fetch_data, daemon=True)
        thread.start()
    
    def _update_marketing_comparison(self, cf_data):
        """Update comparison table between CF and GA"""
        try:
            # Clear existing rows
            for widget in self.marketing_comparison_data.winfo_children():
                widget.destroy()
            
            # Get GA data for comparison
            from google_analytics_fetcher import GoogleAnalyticsFetcher, load_config
            from multi_property_analytics import MultiPropertyAnalytics
            
            ga_config = load_config()
            if ga_config and 'aggregate_properties' in ga_config:
                property_configs = [
                    {'property_id': pid, 'label': ga_config['property_labels'].get(pid, pid)}
                    for pid in ga_config['aggregate_properties']
                ]
                
                analytics = MultiPropertyAnalytics(
                    credentials_file=ga_config['credentials_file'],
                    property_configs=property_configs
                )
                
                ga_metrics = analytics.get_aggregated_metrics(days_back=28)
                
                # Comparison rows
                rows = [
                    ("Page Visits", cf_data['estimated_html_pages'], ga_metrics['total_views']),
                    ("Unique Visitors", cf_data['human_uniques'], ga_metrics['total_users']),
                ]
                
                for i, (metric, cf_val, ga_val) in enumerate(rows):
                    row_bg = '#ffffff' if i % 2 == 0 else '#f8f9fa'
                    
                    row_frame = tk.Frame(self.marketing_comparison_data, bg=row_bg)
                    row_frame.pack(fill='x', pady=2)
                    
                    tk.Label(row_frame, text=metric, font=('Arial', 9),
                            bg=row_bg, width=25, anchor='w').grid(row=0, column=0, padx=10, pady=5, sticky='w')
                    tk.Label(row_frame, text=f"{cf_val:,}", font=('Arial', 9, 'bold'),
                            bg=row_bg, fg='#ff9800', width=20).grid(row=0, column=1, padx=10, pady=5)
                    tk.Label(row_frame, text=f"{ga_val:,}", font=('Arial', 9, 'bold'),
                            bg=row_bg, fg='#4285f4', width=20).grid(row=0, column=2, padx=10, pady=5)
                    
                    # Calculate coverage
                    if cf_val > 0:
                        coverage = (ga_val / cf_val * 100)
                        tk.Label(row_frame, text=f"GA: {coverage:.1f}%", font=('Arial', 9),
                                bg=row_bg, fg='#666', width=15).grid(row=0, column=3, padx=10, pady=5)
                
        except Exception as e:
            print(f"[ERROR] Updating comparison: {str(e)}")
    
    def _update_marketing_charts(self, cf_data_7d, cf_data_28d, cf_data_90d):
        """Update all marketing charts with Cloudflare data"""
        try:
            from google_analytics_fetcher import load_config
            from multi_property_analytics import MultiPropertyAnalytics
            from trieste_analytics import get_trieste_metrics
            from pordenone_analytics import get_pordenone_metrics
            
            # Get GA data to determine site proportions
            ga_config = load_config()
            if not ga_config:
                return
            
            property_configs = [
                {'property_id': pid, 'label': ga_config['property_labels'].get(pid, pid)}
                for pid in ga_config['aggregate_properties']
            ]
            
            analytics = MultiPropertyAnalytics(
                credentials_file=ga_config['credentials_file'],
                property_configs=property_configs
            )
            
            # Get GA metrics to calculate proportions
            ga_metrics_28d = analytics.get_aggregated_metrics(days_back=28)
            trieste_ga_28d = get_trieste_metrics(analytics.fetchers, days_back=28)
            
            # Get FVG fetcher for Pordenone
            fvg_fetcher = analytics.fetchers.get("257131451")
            pordenone_ga_28d = get_pordenone_metrics(fvg_fetcher, days_back=28) if fvg_fetcher else {'views': 0, 'users': 0}
            
            # Calculate proportions from GA
            total_ga_views = ga_metrics_28d['total_views']
            trieste_proportion = trieste_ga_28d['views'] / total_ga_views if total_ga_views > 0 else 0.6
            pordenone_proportion = pordenone_ga_28d['views'] / total_ga_views if total_ga_views > 0 else 0.4
            
            # Apply proportions to Cloudflare data
            if cf_data_28d:
                trieste_cf_visits = int(cf_data_28d['estimated_html_pages'] * trieste_proportion)
                pordenone_cf_visits = int(cf_data_28d['estimated_html_pages'] * pordenone_proportion)
                
                # Update site-specific visitor labels
                self.trieste_marketing_visits_label.config(text=f"{trieste_cf_visits:,} visits")
                self.pordenone_marketing_visits_label.config(text=f"{pordenone_cf_visits:,} visits")
            
            # Update global traffic pie chart
            self._update_marketing_traffic_pie(cf_data_28d)
            
            # Update global daily chart (multi-period)
            self._update_marketing_daily_chart(cf_data_7d, cf_data_28d, cf_data_90d)
            
            # Update Trieste charts
            self._update_trieste_marketing_charts(cf_data_7d, cf_data_28d, cf_data_90d, trieste_proportion)
            
            # Update Pordenone charts
            self._update_pordenone_marketing_charts(cf_data_7d, cf_data_28d, cf_data_90d, pordenone_proportion)
            
        except Exception as e:
            print(f"[ERROR] Updating marketing charts: {str(e)}")
    
    def _update_marketing_traffic_pie(self, cf_data):
        """Update marketing traffic breakdown pie chart"""
        try:
            self.marketing_traffic_ax.clear()
            
            # Breakdown by impression type
            if cf_data:
                labels = ['Page Visits', 'Ad Impressions', 'Image Views']
                sizes = [
                    cf_data['estimated_html_pages'],
                    cf_data['estimated_ad_impressions'] - cf_data['estimated_html_pages'],
                    cf_data['estimated_image_impressions']
                ]
                colors = ['#ff9800', '#9c27b0', '#00bcd4']
                
                wedges, texts, autotexts = self.marketing_traffic_ax.pie(
                    sizes, labels=labels, autopct='%1.1f%%',
                    colors=colors, startangle=90,
                    textprops={'fontsize': 9},
                    pctdistance=0.85
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(8)
                    autotext.set_weight('bold')
                
                for text in texts:
                    text.set_fontsize(8)
                
                self.marketing_traffic_ax.set_title('Impression Types Distribution', fontsize=10)
                
            self.marketing_traffic_canvas.draw()
            
        except Exception as e:
            print(f"[ERROR] Updating marketing traffic pie: {str(e)}")
    
    def _update_marketing_daily_chart(self, cf_7d, cf_28d, cf_90d):
        """Update marketing daily chart with multi-period overlay"""
        try:
            self.marketing_daily_fig.clear()
            ax = self.marketing_daily_fig.add_subplot(111)
            
            # Since Cloudflare returns aggregated data, we'll use GA daily patterns
            # but scale them to CF total volumes
            from google_analytics_fetcher import load_config
            from multi_property_analytics import MultiPropertyAnalytics
            
            ga_config = load_config()
            if ga_config:
                property_configs = [
                    {'property_id': pid, 'label': ga_config['property_labels'].get(pid, pid)}
                    for pid in ga_config['aggregate_properties']
                ]
                
                analytics = MultiPropertyAnalytics(
                    credentials_file=ga_config['credentials_file'],
                    property_configs=property_configs
                )
                
                # Get GA daily patterns
                ga_daily_7d = analytics.get_aggregated_daily_traffic(days_back=7)
                ga_daily_28d = analytics.get_aggregated_daily_traffic(days_back=28)
                ga_daily_90d = analytics.get_aggregated_daily_traffic(days_back=90)
                
                # Calculate scaling factors
                ga_total_7d = sum(ga_daily_7d.values()) if ga_daily_7d else 1
                ga_total_28d = sum(ga_daily_28d.values()) if ga_daily_28d else 1
                ga_total_90d = sum(ga_daily_90d.values()) if ga_daily_90d else 1
                
                cf_total_7d = cf_7d['estimated_html_pages'] if cf_7d else 0
                cf_total_28d = cf_28d['estimated_html_pages'] if cf_28d else 0
                cf_total_90d = cf_90d['estimated_html_pages'] if cf_90d else 0
                
                scale_7d = cf_total_7d / ga_total_7d if ga_total_7d > 0 else 1
                scale_28d = cf_total_28d / ga_total_28d if ga_total_28d > 0 else 1
                scale_90d = cf_total_90d / ga_total_90d if ga_total_90d > 0 else 1
                
                # Plot scaled data
                # 90-day (GREEN)
                if ga_daily_90d and cf_90d:
                    sorted_dates = sorted(ga_daily_90d.keys())
                    users = [ga_daily_90d[date] * scale_90d for date in sorted_dates]
                    x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                    ax.plot(x_points, users, linewidth=2, color='#34a853', alpha=0.8, label='90 days')
                
                # 28-day (BLUE)
                if ga_daily_28d and cf_28d:
                    sorted_dates = sorted(ga_daily_28d.keys())
                    users = [ga_daily_28d[date] * scale_28d for date in sorted_dates]
                    x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                    ax.plot(x_points, users, linewidth=2.5, color='#4285f4', alpha=0.8, label='28 days')
                
                # 7-day (ORANGE)
                if ga_daily_7d and cf_7d:
                    sorted_dates = sorted(ga_daily_7d.keys())
                    users = [ga_daily_7d[date] * scale_7d for date in sorted_dates]
                    x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                    ax.plot(x_points, users, linewidth=3, color='#ff9800', alpha=0.9, label='7 days')
                
                # Grey trend line
                if ga_daily_90d and cf_90d:
                    sorted_dates = sorted(ga_daily_90d.keys())
                    users = [ga_daily_90d[date] * scale_90d for date in sorted_dates]
                    if len(users) > 1:
                        import numpy as np
                        x_trend = np.array([100 - (i * 100 / (len(users)-1)) for i in range(len(users))])
                        y_trend = np.array(users)
                        z = np.polyfit(x_trend, y_trend, 1)
                        p = np.poly1d(z)
                        ax.plot(x_trend, p(x_trend), '-', linewidth=2, color='#808080', alpha=0.6)
                        
                        # Add percentage text
                        start_value = p(100)
                        end_value = p(0)
                        pct_change = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                        sign = '+' if pct_change > 0 else ''
                        ax.text(0.98, end_value, f'{sign}{pct_change:.1f}%',
                               color='#666', fontsize=9, weight='bold',
                               ha='left', va='center',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                        edgecolor='#999', alpha=0.8))
                
                ax.set_ylabel('Page Visits (CF)', fontsize=10)
                ax.set_title('Daily Page Visits - 3 Time Scales (Marketing)', fontsize=10)
                ax.grid(True, alpha=0.3)
                ax.legend(loc='upper left', fontsize=9)
                ax.set_xlim(100, 0)
                ax.set_xticks([])
                
                # Add 3 x-axis scales
                ax.text(0.00, -0.08, '7d:', transform=ax.transAxes, fontsize=8, color='#ff9800', weight='bold')
                ax.text(0.98, -0.08, '→0', transform=ax.transAxes, fontsize=6, color='#ff9800', ha='right')
                ax.text(0.00, -0.13, '28d:', transform=ax.transAxes, fontsize=8, color='#4285f4', weight='bold')
                ax.text(0.98, -0.13, '→0', transform=ax.transAxes, fontsize=6, color='#4285f4', ha='right')
                ax.text(0.00, -0.18, '90d:', transform=ax.transAxes, fontsize=8, color='#34a853', weight='bold')
                ax.text(0.98, -0.18, '→0', transform=ax.transAxes, fontsize=6, color='#34a853', ha='right')
            
            self.marketing_daily_fig.tight_layout()
            self.marketing_daily_canvas.draw()
            
        except Exception as e:
            print(f"[ERROR] Updating marketing daily chart: {str(e)}")
    
    def _update_trieste_marketing_charts(self, cf_7d, cf_28d, cf_90d, trieste_proportion):
        """Update Trieste-specific marketing charts"""
        try:
            # Pie chart - Impression types for Trieste
            self.trieste_mkt_pie_ax.clear()
            
            if cf_28d:
                trieste_pages = int(cf_28d['estimated_html_pages'] * trieste_proportion)
                trieste_ads = int(cf_28d['estimated_ad_impressions'] * trieste_proportion)
                trieste_images = int(cf_28d['estimated_image_impressions'] * trieste_proportion)
                
                labels = ['Pages', 'Ads', 'Images']
                sizes = [trieste_pages, trieste_ads - trieste_pages, trieste_images]
                colors = ['#4285f4', '#9c27b0', '#00bcd4']
                
                wedges, texts, autotexts = self.trieste_mkt_pie_ax.pie(
                    sizes, labels=labels, autopct='%1.0f%%',
                    colors=colors, startangle=90,
                    textprops={'fontsize': 8}, pctdistance=0.8
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(7)
                    autotext.set_weight('bold')
                
                for text in texts:
                    text.set_fontsize(7)
                
                self.trieste_mkt_pie_ax.set_title('Trieste Impressions', fontsize=9)
            
            self.trieste_mkt_pie_canvas.draw()
            
            # Daily chart - use same approach as global but scaled
            self._update_site_specific_marketing_daily(
                self.trieste_mkt_daily_fig, self.trieste_mkt_daily_ax, self.trieste_mkt_daily_canvas,
                cf_7d, cf_28d, cf_90d, trieste_proportion, 'Trieste'
            )
            
        except Exception as e:
            print(f"[ERROR] Updating Trieste marketing charts: {str(e)}")
    
    def _update_pordenone_marketing_charts(self, cf_7d, cf_28d, cf_90d, pordenone_proportion):
        """Update Pordenone-specific marketing charts"""
        try:
            # Pie chart
            self.pordenone_mkt_pie_ax.clear()
            
            if cf_28d:
                pordenone_pages = int(cf_28d['estimated_html_pages'] * pordenone_proportion)
                pordenone_ads = int(cf_28d['estimated_ad_impressions'] * pordenone_proportion)
                pordenone_images = int(cf_28d['estimated_image_impressions'] * pordenone_proportion)
                
                labels = ['Pages', 'Ads', 'Images']
                sizes = [pordenone_pages, pordenone_ads - pordenone_pages, pordenone_images]
                colors = ['#ea4335', '#9c27b0', '#00bcd4']
                
                wedges, texts, autotexts = self.pordenone_mkt_pie_ax.pie(
                    sizes, labels=labels, autopct='%1.0f%%',
                    colors=colors, startangle=90,
                    textprops={'fontsize': 8}, pctdistance=0.8
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(7)
                    autotext.set_weight('bold')
                
                for text in texts:
                    text.set_fontsize(7)
                
                self.pordenone_mkt_pie_ax.set_title('Pordenone Impressions', fontsize=9)
            
            self.pordenone_mkt_pie_canvas.draw()
            
            # Daily chart
            self._update_site_specific_marketing_daily(
                self.pordenone_mkt_daily_fig, self.pordenone_mkt_daily_ax, self.pordenone_mkt_daily_canvas,
                cf_7d, cf_28d, cf_90d, pordenone_proportion, 'Pordenone'
            )
            
        except Exception as e:
            print(f"[ERROR] Updating Pordenone marketing charts: {str(e)}")
    
    def _update_site_specific_marketing_daily(self, fig, ax_obj, canvas, cf_7d, cf_28d, cf_90d, proportion, site_name):
        """Update site-specific daily marketing chart"""
        try:
            from google_analytics_fetcher import load_config
            from multi_property_analytics import MultiPropertyAnalytics
            from trieste_analytics import get_trieste_daily_traffic
            from pordenone_analytics import get_pordenone_daily_traffic
            
            fig.clear()
            ax = fig.add_subplot(111)
            
            ga_config = load_config()
            if ga_config:
                property_configs = [
                    {'property_id': pid, 'label': ga_config['property_labels'].get(pid, pid)}
                    for pid in ga_config['aggregate_properties']
                ]
                
                analytics = MultiPropertyAnalytics(
                    credentials_file=ga_config['credentials_file'],
                    property_configs=property_configs
                )
                
                # Get GA daily pattern for this site
                if site_name == 'Trieste':
                    ga_daily_7d = get_trieste_daily_traffic(analytics.fetchers, days_back=7)
                    ga_daily_28d = get_trieste_daily_traffic(analytics.fetchers, days_back=28)
                    ga_daily_90d = get_trieste_daily_traffic(analytics.fetchers, days_back=90)
                else:  # Pordenone
                    fvg_fetcher = analytics.fetchers.get("257131451")
                    if fvg_fetcher:
                        ga_daily_7d = get_pordenone_daily_traffic(fvg_fetcher, days_back=7)
                        ga_daily_28d = get_pordenone_daily_traffic(fvg_fetcher, days_back=28)
                        ga_daily_90d = get_pordenone_daily_traffic(fvg_fetcher, days_back=90)
                    else:
                        ga_daily_7d = ga_daily_28d = ga_daily_90d = {}
                
                # Calculate scaling factors
                if ga_daily_90d and cf_90d:
                    ga_total = sum(ga_daily_90d.values())
                    cf_total = cf_90d['estimated_html_pages'] * proportion
                    scale_90d = cf_total / ga_total if ga_total > 0 else 1
                    
                    sorted_dates = sorted(ga_daily_90d.keys())
                    users = [ga_daily_90d[date] * scale_90d for date in sorted_dates]
                    x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                    ax.plot(x_points, users, linewidth=2, color='#34a853', alpha=0.8, label='90d')
                    
                    # Grey trend
                    if len(users) > 1:
                        import numpy as np
                        x_trend = np.array(x_points)
                        y_trend = np.array(users)
                        z = np.polyfit(x_trend, y_trend, 1)
                        p = np.poly1d(z)
                        ax.plot(x_trend, p(x_trend), '-', linewidth=2, color='#808080', alpha=0.6)
                        
                        start_value = p(100)
                        end_value = p(0)
                        pct_change = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                        sign = '+' if pct_change > 0 else ''
                        ax.text(0.98, end_value, f'{sign}{pct_change:.1f}%',
                               color='#666', fontsize=8, weight='bold', ha='left', va='center',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#999', alpha=0.8))
                
                # 28-day (BLUE)
                if ga_daily_28d and cf_28d:
                    ga_total = sum(ga_daily_28d.values())
                    cf_total = cf_28d['estimated_html_pages'] * proportion
                    scale_28d = cf_total / ga_total if ga_total > 0 else 1
                    
                    sorted_dates = sorted(ga_daily_28d.keys())
                    users = [ga_daily_28d[date] * scale_28d for date in sorted_dates]
                    x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                    ax.plot(x_points, users, linewidth=2.5, color='#4285f4', alpha=0.8, label='28d')
                
                # 7-day (ORANGE)
                if ga_daily_7d and cf_7d:
                    ga_total = sum(ga_daily_7d.values())
                    cf_total = cf_7d['estimated_html_pages'] * proportion
                    scale_7d = cf_total / ga_total if ga_total > 0 else 1
                    
                    sorted_dates = sorted(ga_daily_7d.keys())
                    users = [ga_daily_7d[date] * scale_7d for date in sorted_dates]
                    x_points = [100 - (i * 100 / (len(users)-1)) for i in range(len(users))]
                    ax.plot(x_points, users, linewidth=3, color='#ff9800', alpha=0.9, label='7d')
                
                ax.set_ylabel('Page Visits', fontsize=8)
                ax.set_title(f'{site_name} 3-Scale', fontsize=9)
                ax.grid(True, alpha=0.3)
                ax.legend(loc='upper left', fontsize=7)
                ax.set_xlim(100, 0)
                ax.set_xticks([])
                
                # 3 x-axis scales
                ax.text(0.00, -0.10, '7d:', transform=ax.transAxes, fontsize=7, color='#ff9800', weight='bold')
                ax.text(0.98, -0.10, '→0', transform=ax.transAxes, fontsize=6, color='#ff9800', ha='right')
                ax.text(0.00, -0.15, '28d:', transform=ax.transAxes, fontsize=7, color='#4285f4', weight='bold')
                ax.text(0.98, -0.15, '→0', transform=ax.transAxes, fontsize=6, color='#4285f4', ha='right')
                ax.text(0.00, -0.20, '90d:', transform=ax.transAxes, fontsize=7, color='#34a853', weight='bold')
                ax.text(0.98, -0.20, '→0', transform=ax.transAxes, fontsize=6, color='#34a853', ha='right')
            
            fig.tight_layout()
            canvas.draw()
            
        except Exception as e:
            print(f"[ERROR] Updating {site_name} marketing daily: {str(e)}")
    
    def create_seozoom_keywords_tab(self):
        """Create the SEOZoom Keywords tab"""
        # SEOZoom keywords tab
        seozoom_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(seozoom_tab, text="🔍 SEO Keywords")
        
        # Create scrollable canvas
        canvas = tk.Canvas(seozoom_tab, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(seozoom_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main container
        main_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#3498db', relief='solid', bd=1)
        header_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(header_frame, text="🔍 SEOZoom Keyword Analysis",
                font=('Arial', 16, 'bold'), bg='#3498db', fg='white').pack(pady=15)
        
        # Info banner
        info_frame = tk.Frame(main_container, bg='#e8f4f8', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 10))
        
        info_text = tk.Label(info_frame,
                            text="Top performing keywords for triesteallnews.it from SEOZoom database",
                            font=('Arial', 10), bg='#e8f4f8', fg='#2c3e50', anchor='w')
        info_text.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        
        # Domain input section
        domain_frame = tk.LabelFrame(main_container, text="Domain Selection",
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        domain_frame.pack(fill='x', pady=(0, 10))
        
        input_container = tk.Frame(domain_frame, bg='#f0f0f0')
        input_container.pack(fill='x', padx=10, pady=10)
        
        tk.Label(input_container, text="Domain:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.seozoom_domain_entry = tk.Entry(input_container, font=('Arial', 10), width=40)
        self.seozoom_domain_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        self.seozoom_domain_entry.insert(0, "triesteallnews.it")
        
        input_container.grid_columnconfigure(1, weight=1)
        
        tk.Label(input_container, text="Limit:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=(20, 10))
        
        self.seozoom_limit_var = tk.StringVar(value="100")
        limit_spinbox = tk.Spinbox(input_container, from_=10, to=500, increment=10,
                                   textvariable=self.seozoom_limit_var,
                                   font=('Arial', 10), width=10)
        limit_spinbox.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(input_container, text="🔍 Get Keywords",
                  command=self.fetch_seozoom_keywords,
                  style='Custom.TButton').grid(row=0, column=4, padx=(20, 0))
        
        # Summary cards
        summary_frame = tk.Frame(main_container, bg='#f0f0f0')
        summary_frame.pack(fill='x', pady=(0, 10))
        
        # Total keywords card
        card1 = tk.Frame(summary_frame, bg='white', relief='solid', bd=1)
        card1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        summary_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(card1, text="Total Keywords", font=('Arial', 10),
                bg='white', fg='#666').pack(pady=(15, 5))
        
        self.seozoom_total_label = tk.Label(card1, text="0", font=('Arial', 24, 'bold'),
                                           bg='white', fg='#3498db')
        self.seozoom_total_label.pack(pady=(0, 15))
        
        # Avg position card
        card2 = tk.Frame(summary_frame, bg='white', relief='solid', bd=1)
        card2.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        summary_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(card2, text="Avg Position", font=('Arial', 10),
                bg='white', fg='#666').pack(pady=(15, 5))
        
        self.seozoom_avgpos_label = tk.Label(card2, text="N/A", font=('Arial', 24, 'bold'),
                                            bg='white', fg='#27ae60')
        self.seozoom_avgpos_label.pack(pady=(0, 15))
        
        # Top 10 count card
        card3 = tk.Frame(summary_frame, bg='white', relief='solid', bd=1)
        card3.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        summary_frame.grid_columnconfigure(2, weight=1)
        
        tk.Label(card3, text="Top 10 Positions", font=('Arial', 10),
                bg='white', fg='#666').pack(pady=(15, 5))
        
        self.seozoom_top10_label = tk.Label(card3, text="0", font=('Arial', 24, 'bold'),
                                           bg='white', fg='#e74c3c')
        self.seozoom_top10_label.pack(pady=(0, 15))
        
        # Keywords table
        table_frame = tk.LabelFrame(main_container, text="📊 Top Keywords",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        table_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create treeview
        columns = ('Rank', 'Keyword', 'Volume', 'Position', 'Traffic', 'CPC', 'Competition')
        self.seozoom_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        self.seozoom_tree.heading('Rank', text='#')
        self.seozoom_tree.heading('Keyword', text='Keyword')
        self.seozoom_tree.heading('Volume', text='Search Volume')
        self.seozoom_tree.heading('Position', text='Position')
        self.seozoom_tree.heading('Traffic', text='Est. Traffic')
        self.seozoom_tree.heading('CPC', text='CPC (€)')
        self.seozoom_tree.heading('Competition', text='Competition')
        
        self.seozoom_tree.column('Rank', width=50, anchor='center')
        self.seozoom_tree.column('Keyword', width=300, anchor='w')
        self.seozoom_tree.column('Volume', width=120, anchor='center')
        self.seozoom_tree.column('Position', width=100, anchor='center')
        self.seozoom_tree.column('Traffic', width=100, anchor='center')
        self.seozoom_tree.column('CPC', width=100, anchor='center')
        self.seozoom_tree.column('Competition', width=120, anchor='center')
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.seozoom_tree.yview)
        self.seozoom_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.seozoom_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        tree_scrollbar.pack(side='right', fill='y', pady=10, padx=(0, 10))
        
        # Status bar
        status_frame = tk.Frame(main_container, bg='#f0f0f0')
        status_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(status_frame, text="📥 Export Keywords",
                  command=self.export_seozoom_keywords,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        self.seozoom_status = tk.Label(status_frame, text="Ready to fetch keywords",
                                      font=('Arial', 9), bg='#f0f0f0', fg='#666')
        self.seozoom_status.pack(side='right', padx=10)
    
    def fetch_seozoom_keywords(self):
        """Fetch keywords from SEOZoom API"""
        domain = self.seozoom_domain_entry.get().strip()
        
        if not domain:
            messagebox.showerror("Error", "Please enter a domain")
            return
        
        limit = int(self.seozoom_limit_var.get())
        
        self.seozoom_status.config(text="Fetching keywords from SEOZoom...", fg='#f39c12')
        self.root.update()
        
        def fetch_thread():
            try:
                from config import SEOZOOM_API_KEY
                from seozoom_keywords import SEOZoomKeywords
                
                seozoom = SEOZoomKeywords(SEOZOOM_API_KEY)
                keywords_data = seozoom.get_keywords(domain, limit=limit, db='it')
                
                if keywords_data:
                    formatted = seozoom.format_keywords_table(keywords_data)
                    
                    # Update UI on main thread
                    self.root.after(0, lambda: self._update_seozoom_table(formatted))
                    self.seozoom_status.config(
                        text=f"Loaded {len(formatted)} keywords for {domain}",
                        fg='#27ae60'
                    )
                else:
                    self.seozoom_status.config(
                        text="No keywords found - check API key or domain",
                        fg='#e74c3c'
                    )
                    messagebox.showwarning("No Data",
                                         "Could not retrieve keywords.\n\n"
                                         "Possible reasons:\n"
                                         "- Domain not in SEOZoom database\n"
                                         "- API key invalid or expired\n"
                                         "- API endpoint changed")
                
            except Exception as e:
                self.seozoom_status.config(
                    text=f"Error: {str(e)[:50]}",
                    fg='#e74c3c'
                )
                print(f"[ERROR] SEOZoom fetch: {str(e)}")
        
        thread = threading.Thread(target=fetch_thread, daemon=True)
        thread.start()
    
    def _update_seozoom_table(self, keywords):
        """Update the SEOZoom keywords table"""
        try:
            # Clear existing data
            for item in self.seozoom_tree.get_children():
                self.seozoom_tree.delete(item)
            
            if not keywords:
                return
            
            # Calculate statistics
            total = len(keywords)
            positions = [kw['position'] for kw in keywords if isinstance(kw['position'], (int, float))]
            avg_position = sum(positions) / len(positions) if positions else 0
            top10_count = sum(1 for kw in keywords if isinstance(kw['position'], (int, float)) and kw['position'] <= 10)
            
            # Update summary cards
            self.seozoom_total_label.config(text=f"{total}")
            self.seozoom_avgpos_label.config(text=f"{avg_position:.1f}" if avg_position > 0 else "N/A")
            self.seozoom_top10_label.config(text=f"{top10_count}")
            
            # Populate table
            for kw in keywords:
                self.seozoom_tree.insert('', 'end', values=(
                    kw['rank'],
                    kw['keyword'],
                    kw['search_volume'],
                    kw['position'],
                    kw['traffic'],
                    kw['cpc'],
                    kw['competition']
                ))
            
            # Store for export
            self.seozoom_current_keywords = keywords
            
        except Exception as e:
            print(f"[ERROR] Updating SEOZoom table: {str(e)}")
    
    def export_seozoom_keywords(self):
        """Export SEOZoom keywords to CSV"""
        if not hasattr(self, 'seozoom_current_keywords') or not self.seozoom_current_keywords:
            messagebox.showwarning("No Data", "No keywords to export. Fetch keywords first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialname=f"seozoom_keywords_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['rank', 'keyword', 'search_volume', 'position', 'traffic', 'cpc', 'competition', 'url']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for kw in self.seozoom_current_keywords:
                        writer.writerow(kw)
                
                messagebox.showinfo("Success", f"Keywords exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    # Article Analytics Methods
    def create_article_controls(self, parent):
        """Create controls for article analytics"""
        # Period selection
        period_frame = tk.LabelFrame(parent, text="Analysis Period", font=('Arial', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        period_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(period_frame, text="Select Period:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 5))
        
        self.period_var = tk.StringVar(value="daily")
        period_frame_inner = tk.Frame(period_frame, bg='#f0f0f0')
        period_frame_inner.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Radiobutton(period_frame_inner, text="Daily", variable=self.period_var, value="daily",
                      font=('Arial', 10), bg='#f0f0f0').pack(anchor='w')
        tk.Radiobutton(period_frame_inner, text="Last 7 Days", variable=self.period_var, value="last_7_days",
                      font=('Arial', 10), bg='#f0f0f0').pack(anchor='w')
        
        # Analysis controls
        controls_frame = tk.LabelFrame(parent, text="Analysis Controls", font=('Arial', 12, 'bold'), 
                                     bg='#f0f0f0', fg='#2c3e50')
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Fetch articles button
        self.fetch_articles_btn = ttk.Button(controls_frame, text="📰 Fetch Most Read Articles", 
                                           command=self.fetch_articles,
                                           style='Custom.TButton')
        self.fetch_articles_btn.pack(fill='x', padx=10, pady=(10, 5))
        
        # Generate analytics button
        self.generate_analytics_btn = ttk.Button(controls_frame, text="📊 Generate Analytics", 
                                               command=self.generate_article_analytics,
                                               style='Custom.TButton')
        self.generate_analytics_btn.pack(fill='x', padx=10, pady=(0, 10))
        
        # Export buttons
        export_frame = tk.LabelFrame(parent, text="Export Options", font=('Arial', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        export_frame.pack(fill='x', pady=(0, 10))
        
        export_buttons_frame = tk.Frame(export_frame, bg='#f0f0f0')
        export_buttons_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(export_buttons_frame, text="Export Articles CSV", 
                  command=self.export_articles_csv).pack(fill='x', pady=(0, 5))
        ttk.Button(export_buttons_frame, text="Export Analytics CSV", 
                  command=self.export_analytics_csv).pack(fill='x')
        
        # IP Address Reminder
        ip_reminder_frame = tk.LabelFrame(parent, text="Important Notice", font=('Arial', 12, 'bold'), 
                                        bg='#fff3cd', fg='#856404')  # Warning colors
        ip_reminder_frame.pack(fill='x', pady=(0, 10))
        
        reminder_text = tk.Text(ip_reminder_frame, height=4, font=('Arial', 9), 
                               bg='#fff3cd', fg='#856404', relief='flat', bd=0,
                               wrap='word')
        reminder_text.pack(fill='x', padx=10, pady=10)
        
        # Get current IP and add reminder text
        try:
            import requests
            response = requests.get("https://api.ipify.org", timeout=5)
            current_ip = response.text.strip() if response.status_code == 200 else "Unknown"
        except:
            current_ip = "Unknown"
        
        reminder_content = f"""IMPORTANT: Cloudflare API queries must be made from your authorized IP address.

Your current IP: {current_ip}

If using Cloudflare API, ensure this IP is authorized in your API token settings:
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Edit your API token
3. Add this IP to 'IP Address Restriction': {current_ip}

Without proper IP authorization, API calls will fail."""
        
        reminder_text.insert('1.0', reminder_content)
        reminder_text.config(state='disabled')  # Make it read-only
        
        # REST API Authentication Notice (MiniOrange)
        api_auth_frame = tk.LabelFrame(parent, text="REST API Authentication", font=('Arial', 12, 'bold'), 
                                       bg='#d1ecf1', fg='#0c5460')  # Info colors
        api_auth_frame.pack(fill='x', pady=(0, 10))
        
        api_auth_text = tk.Text(api_auth_frame, height=6, font=('Arial', 9), 
                               bg='#d1ecf1', fg='#0c5460', relief='flat', bd=0,
                               wrap='word')
        api_auth_text.pack(fill='x', padx=10, pady=10)
        
        api_auth_content = """NOTE: trieste.news REST API Authentication

The WordPress REST API for triesteallnews.it uses miniOrange API Authentication plugin with OAuth 2.0 client credentials.

Authentication Method: OAuth 2.0 (miniOrange)
- Client ID and Client Secret are required
- Configured in: miniorange_oauth_config.json

For real visit/traffic data: Install a WordPress view counter plugin (WP-PostViews, Post Views Counter) on the website.

Current data: Real titles, URLs, dates, authors + Estimated visit counts"""
        
        api_auth_text.insert('1.0', api_auth_content)
        api_auth_text.config(state='disabled')  # Make it read-only
        
        # Article preview
        preview_frame = tk.LabelFrame(parent, text="Article Preview", font=('Arial', 12, 'bold'), 
                                    bg='#f0f0f0', fg='#2c3e50')
        preview_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Articles listbox
        listbox_frame = tk.Frame(preview_frame, bg='#f0f0f0')
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.articles_listbox = tk.Listbox(listbox_frame, font=('Consolas', 9), 
                                          bg='white', relief='sunken', bd=1)
        articles_scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.articles_listbox.yview)
        self.articles_listbox.configure(yscrollcommand=articles_scrollbar.set)
        
        self.articles_listbox.pack(side='left', fill='both', expand=True)
        articles_scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.articles_listbox.bind('<<ListboxSelect>>', self.on_article_select)
        
        # Initial placeholder
        self.articles_listbox.insert(tk.END, "No articles loaded")
        self.articles_listbox.insert(tk.END, "Click 'Fetch Most Read Articles' to load data")
    
    def create_article_results_area(self, parent):
        """Create results display area for articles"""
        results_frame = tk.LabelFrame(parent, text="Article Analytics Results", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        results_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Results text area with scrollbar
        text_frame = tk.Frame(results_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.article_results_text = tk.Text(text_frame, font=('Consolas', 9), 
                                           bg='#f8f9fa', relief='sunken', bd=1)
        article_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.article_results_text.yview)
        self.article_results_text.configure(yscrollcommand=article_scrollbar.set)
        
        self.article_results_text.pack(side='left', fill='both', expand=True)
        article_scrollbar.pack(side='right', fill='y')
        
        # Initial placeholder
        self.article_results_text.insert(tk.END, "Article analytics results will appear here...")
    
    def create_article_charts_area(self, parent):
        """Create charts display area for articles"""
        charts_frame = tk.LabelFrame(parent, text="Article Performance Charts", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        charts_frame.pack(fill='both', expand=True)
        
        # Create matplotlib figure for articles
        self.article_fig = Figure(figsize=(12, 6), dpi=100)
        self.article_canvas = FigureCanvasTkAgg(self.article_fig, charts_frame)
        self.article_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial empty chart
        self.show_empty_article_chart()
    
    def show_empty_article_chart(self):
        """Show empty chart placeholder for articles"""
        self.article_fig.clear()
        ax = self.article_fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Fetch articles and generate analytics to see charts', 
                ha='center', va='center', fontsize=14, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.article_canvas.draw()
    
    def fetch_articles(self):
        """Fetch most read articles"""
        period = self.period_var.get()
        
        self.fetch_articles_btn.config(text="Fetching...", state='disabled')
        self.articles_listbox.delete(0, tk.END)
        self.articles_listbox.insert(tk.END, f"Fetching {period} most read articles...")
        
        def fetch_thread():
            try:
                articles = self.article_engine.get_most_read_articles(period, 10)
                
                # Store articles
                if period == "daily":
                    self.daily_articles = articles
                else:
                    self.last_7_days_articles = articles
                
                # Update UI
                self.root.after(0, lambda: self.update_articles_list(articles, period))
                
            except Exception as e:
                error_msg = f"Error fetching articles: {str(e)}"
                self.root.after(0, lambda: self.update_articles_error(error_msg))
        
        threading.Thread(target=fetch_thread, daemon=True).start()
    
    def update_articles_list(self, articles, period):
        """Update the articles listbox with fetched articles"""
        self.articles_listbox.delete(0, tk.END)
        
        if not articles:
            self.articles_listbox.insert(tk.END, f"No {period} articles found")
            return
        
        # Add header with info about data source
        data_source = "Real Data" if any("triesteallnews.it" in article.url for article in articles) else "Sample Data"
        
        # Check data source - prioritize Cloudflare-based analytics
        try:
            from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
            if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID:
                data_source = "Cloudflare-Based Analytics"
        except:
            pass
        
        self.articles_listbox.insert(tk.END, f"📰 {period.capitalize()} Most Read Articles ({data_source})")
        self.articles_listbox.insert(tk.END, "=" * 60)
        
        for i, article in enumerate(articles, 1):
            # Format title to fit with read count
            title_text = article.title[:50] if len(article.title) > 50 else article.title
            if len(article.title) > 50:
                title_text += "..."
            
            # Format read count
            read_count_text = f"{article.read_count:,}"
            
            # Create display text with read count
            display_text = f"{i:2d}. {title_text}"
            self.articles_listbox.insert(tk.END, display_text)
            
            # Format publication date for better readability
            try:
                from datetime import datetime
                pub_date = datetime.strptime(article.publish_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pub_date = article.publish_date
            
            # Add read count and publication date on next line (indented)
            read_display = f"    👀 {read_count_text} reads | 📂 {article.category} | 📅 {pub_date}"
            self.articles_listbox.insert(tk.END, read_display)
        
        # Add footer with read count info
        total_reads = sum(article.read_count for article in articles)
        self.articles_listbox.insert(tk.END, "")
        self.articles_listbox.insert(tk.END, f"📊 Total estimated reads: {total_reads:,}")
        self.articles_listbox.insert(tk.END, f"📅 Period: {period.capitalize()}")
        
        self.fetch_articles_btn.config(text="📰 Fetch Most Read Articles", state='normal')
    
    def update_articles_error(self, error_msg):
        """Update articles list with error message"""
        self.articles_listbox.delete(0, tk.END)
        self.articles_listbox.insert(tk.END, error_msg)
        self.fetch_articles_btn.config(text="📰 Fetch Most Read Articles", state='normal')
    
    def on_article_select(self, event):
        """Handle article selection in listbox"""
        selection = self.articles_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        period = self.period_var.get()
        articles = self.daily_articles if period == "daily" else self.last_7_days_articles
        
        # Calculate article index from listbox index
        # Each article takes 2 lines (title + read count), plus header lines
        header_lines = 2  # Header and separator line
        article_index = (index - header_lines) // 2
        
        # Check if it's a valid article line (not read count line)
        if (index - header_lines) % 2 == 0 and article_index >= 0 and article_index < len(articles):
            article = articles[article_index]
            self.display_article_details(article)
    
    def display_article_details(self, article):
        """Display detailed information about selected article"""
        details = f"📰 Article Details:\n"
        details += f"=" * 60 + "\n\n"
        details += f"📝 Title: {article.title}\n\n"
        details += f"🌐 URL: {article.url}\n\n"
        details += f"📂 Category: {article.category}\n"
        details += f"✍️  Author: {article.author}\n"
        
        # Format publication date for better readability
        try:
            from datetime import datetime
            pub_date = datetime.strptime(article.publish_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            pub_date_full = datetime.strptime(article.publish_date, '%Y-%m-%d').strftime('%A, %d %B %Y')
        except:
            pub_date = article.publish_date
            pub_date_full = article.publish_date
        
        details += f"📅 Publish Date: {pub_date} ({pub_date_full})\n\n"
        details += f"📊 Performance Metrics:\n"
        details += f"   👀 READ COUNT: {article.read_count:,} (Primary Metric)\n"
        details += f"   ⭐ Engagement Score: {article.engagement_score:.1f}/10\n"
        details += f"   📤 Social Shares: {article.social_shares}\n"
        details += f"   💬 Comments: {article.comments_count}\n"
        details += f"   📝 Word Count: {article.word_count}\n\n"
        details += f"📈 Engagement Rate: {(article.social_shares + article.comments_count) / max(article.read_count, 1) * 100:.2f}%\n"
        details += f"📊 Read Performance: {'High' if article.read_count > 500 else 'Medium' if article.read_count > 200 else 'Low'} (based on {article.read_count:,} reads)\n"
        
        self.article_results_text.delete(1.0, tk.END)
        self.article_results_text.insert(tk.END, details)
    
    def generate_article_analytics(self):
        """Generate comprehensive article analytics"""
        period = self.period_var.get()
        articles = self.daily_articles if period == "daily" else self.last_7_days_articles
        
        if not articles:
            messagebox.showerror("Error", f"No {period} articles available. Please fetch articles first.")
            return
        
        self.generate_analytics_btn.config(text="Generating...", state='disabled')
        self.article_results_text.delete(1.0, tk.END)
        self.article_results_text.insert(tk.END, f"Generating {period} analytics...")
        
        def analytics_thread():
            try:
                analytics = self.article_engine.get_article_analytics(period)
                self.article_analytics = analytics
                
                # Update UI
                self.root.after(0, lambda: self.update_analytics_display(analytics, period))
                
                # Generate charts
                self.root.after(0, lambda: self.create_article_charts(analytics, period))
                
            except Exception as e:
                error_msg = f"Error generating analytics: {str(e)}"
                self.root.after(0, lambda: self.update_analytics_error(error_msg))
        
        threading.Thread(target=analytics_thread, daemon=True).start()
    
    def update_analytics_display(self, analytics, period):
        """Update analytics display with results"""
        report = f"Article Analytics Report - {period.upper()}\n"
        report += "=" * 60 + "\n"
        report += f"Generated: {analytics.date}\n"
        report += f"Total Articles: {analytics.total_articles}\n"
        report += f"Total Reads: {analytics.total_reads:,}\n"
        report += f"Average Reads per Article: {analytics.engagement_metrics['average_reads_per_article']:.1f}\n"
        report += f"Engagement Rate: {analytics.engagement_metrics['engagement_rate']:.2%}\n"
        report += f"Total Social Shares: {analytics.engagement_metrics['total_social_shares']}\n"
        report += f"Total Comments: {analytics.engagement_metrics['total_comments']}\n"
        report += "\n" + "=" * 60 + "\n"
        
        # Top articles
        report += "\nTOP ARTICLES:\n"
        report += "-" * 40 + "\n"
        for i, article in enumerate(analytics.top_articles[:5], 1):
            report += f"{i}. {article.title[:50]}{'...' if len(article.title) > 50 else ''}\n"
            report += f"   Reads: {article.read_count:,} | Category: {article.category}\n"
            report += f"   Engagement: {article.engagement_score:.1f}/10\n\n"
        
        # Category breakdown
        report += "\nCATEGORY BREAKDOWN:\n"
        report += "-" * 40 + "\n"
        for category, reads in analytics.category_breakdown.items():
            percentage = (reads / analytics.total_reads) * 100 if analytics.total_reads > 0 else 0
            report += f"{category}: {reads:,} reads ({percentage:.1f}%)\n"
        
        # Author performance
        report += "\nAUTHOR PERFORMANCE:\n"
        report += "-" * 40 + "\n"
        for author, reads in analytics.author_performance.items():
            percentage = (reads / analytics.total_reads) * 100 if analytics.total_reads > 0 else 0
            report += f"{author}: {reads:,} reads ({percentage:.1f}%)\n"
        
        self.article_results_text.delete(1.0, tk.END)
        self.article_results_text.insert(tk.END, report)
        self.generate_analytics_btn.config(text="📊 Generate Analytics", state='normal')
    
    def update_analytics_error(self, error_msg):
        """Update analytics display with error message"""
        self.article_results_text.delete(1.0, tk.END)
        self.article_results_text.insert(tk.END, error_msg)
        self.generate_analytics_btn.config(text="📊 Generate Analytics", state='normal')
    
    def create_article_charts(self, analytics, period):
        """Create charts for article analytics"""
        try:
            self.article_fig.clear()
            
            # Create subplots
            ax1 = self.article_fig.add_subplot(2, 2, 1)
            ax2 = self.article_fig.add_subplot(2, 2, 2)
            ax3 = self.article_fig.add_subplot(2, 2, 3)
            ax4 = self.article_fig.add_subplot(2, 2, 4)
            
            # Chart 1: Top Articles by Reads
            if analytics.top_articles:
                top_5_articles = analytics.top_articles[:5]
                titles = [article.title[:20] + '...' if len(article.title) > 20 else article.title 
                         for article in top_5_articles]
                reads = [article.read_count for article in top_5_articles]
                
                ax1.barh(range(len(titles)), reads, color='#1f77b4')
                ax1.set_yticks(range(len(titles)))
                ax1.set_yticklabels(titles, fontsize=8)
                ax1.set_xlabel('Read Count')
                ax1.set_title('Top 5 Articles by Reads')
                ax1.grid(True, alpha=0.3)
            
            # Chart 2: Category Breakdown
            if analytics.category_breakdown:
                categories = list(analytics.category_breakdown.keys())
                category_reads = list(analytics.category_breakdown.values())
                
                ax2.pie(category_reads, labels=categories, autopct='%1.1f%%', startangle=90)
                ax2.set_title('Reads by Category')
            
            # Chart 3: Author Performance
            if analytics.author_performance:
                authors = list(analytics.author_performance.keys())
                author_reads = list(analytics.author_performance.values())
                
                ax3.bar(range(len(authors)), author_reads, color='#2ca02c')
                ax3.set_xticks(range(len(authors)))
                ax3.set_xticklabels(authors, rotation=45, ha='right', fontsize=8)
                ax3.set_ylabel('Total Reads')
                ax3.set_title('Author Performance')
                ax3.grid(True, alpha=0.3)
            
            # Chart 4: Engagement Metrics
            metrics = analytics.engagement_metrics
            metric_names = ['Avg Engagement', 'Social Shares', 'Comments', 'Engagement Rate']
            metric_values = [
                metrics['average_engagement_score'],
                metrics['total_social_shares'] / 100,  # Scale down for visualization
                metrics['total_comments'] / 10,  # Scale down for visualization
                metrics['engagement_rate'] * 100
            ]
            
            ax4.bar(metric_names, metric_values, color=['#d62728', '#ff7f0e', '#9467bd', '#8c564b'])
            ax4.set_ylabel('Score/Count')
            ax4.set_title('Engagement Metrics')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
            
            # Adjust layout
            self.article_fig.tight_layout()
            self.article_canvas.draw()
            
            print(f"Article charts generated successfully for {period} period")
            
        except Exception as e:
            print(f"Error creating article charts: {e}")
            # Show error message in chart area
            self.article_fig.clear()
            ax = self.article_fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Error generating article charts:\n{str(e)}', 
                    ha='center', va='center', fontsize=12, color='red')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.article_canvas.draw()
    
    def export_articles_csv(self):
        """Export articles to CSV"""
        period = self.period_var.get()
        articles = self.daily_articles if period == "daily" else self.last_7_days_articles
        
        if not articles:
            messagebox.showerror("Error", f"No {period} articles to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialname=f"triesteallnews_{period}_articles_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filename:
            try:
                self.article_engine.export_articles_to_csv(articles, filename)
                messagebox.showinfo("Success", f"Articles exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export articles: {str(e)}")
    
    def export_analytics_csv(self):
        """Export analytics to CSV"""
        if not self.article_analytics:
            messagebox.showerror("Error", "No analytics data to export")
            return
        
        period = self.period_var.get()
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialname=f"triesteallnews_{period}_analytics_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filename:
            try:
                self.article_engine.export_analytics_to_csv(self.article_analytics, filename)
                messagebox.showinfo("Success", f"Analytics exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export analytics: {str(e)}")

def test_chart_generation():
    """Test function to verify chart generation works"""
    print("Testing chart generation...")
    
    # Create a test metrics object
    from web_ranking_tool import WebsiteMetrics
    test_metrics = WebsiteMetrics(
        domain="test.com",
        data_source="Test",
        global_rank=1000,
        monthly_visits=5000000,
        bounce_rate=50.0,
        avg_visit_duration=120.0,
        pages_per_visit=3.0
    )
    
    # Create a simple test window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    app = WebRankingGUI(root)
    
    # Test the chart generation
    try:
        historical_data = app.generate_single_site_historical_data(1, test_metrics)
        print(f"Generated historical data: {len(historical_data['months'])} months")
        print(f"Sample visits: {historical_data['visits'][:3]}")
        print(f"Sample ranks: {historical_data['ranks'][:3]}")
        
        app.create_single_site_monthly_chart(historical_data, 1, test_metrics)
        print("Chart generation test successful!")
        
    except Exception as e:
        print(f"Chart generation test failed: {e}")
    
    root.destroy()

def main():
    root = tk.Tk()
    app = WebRankingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # Uncomment the next line to run chart generation test
    # test_chart_generation()
    main()
