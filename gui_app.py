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
        
        # Main content frame with notebook
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_website_analysis_tab()
        self.create_article_analytics_tab()
    
    def create_website_analysis_tab(self):
        """Create the website analysis tab"""
        # Website analysis tab
        website_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(website_tab, text="🌐 Website Analysis")
        
        # Left panel - Site selection and controls
        left_panel = tk.Frame(website_tab, bg='#f0f0f0', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Results and charts
        right_panel = tk.Frame(website_tab, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_site_selection(left_panel)
        self.create_preview_windows(left_panel)
        self.create_traffic_sources_section(left_panel)
        self.create_controls(left_panel)
        self.create_results_area(right_panel)
        self.create_charts_area(right_panel)
    
    def create_article_analytics_tab(self):
        """Create the article analytics tab"""
        # Article analytics tab
        article_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(article_tab, text="📰 Article Analytics")
        
        # Left panel - Controls and filters
        left_panel = tk.Frame(article_tab, bg='#f0f0f0', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Results and charts
        right_panel = tk.Frame(article_tab, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_article_controls(left_panel)
        self.create_article_results_area(right_panel)
        self.create_article_charts_area(right_panel)
    
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
