# MediaImmagine Web Ranking Tool

A comprehensive tool for comparing website traffic metrics and rankings from multiple data sources. This tool provides both web and desktop GUI interfaces for analyzing website performance across SimilarWeb, Alexa, and SEMrush data sources.

## Features

- **Free API Support**: BuiltWith, Wappalyzer, Google PageSpeed (completely free!)
- **Paid API Support**: SimilarWeb, SEMrush (optional, expensive)
- **Multi-Source Data**: Compares data from multiple free and paid APIs
- **Comprehensive Metrics**: Global rank, country rank, monthly visits, bounce rate, visit duration
- **Traffic Analysis**: Traffic sources breakdown and top countries
- **Multiple Interfaces**: Command-line, web interface, and desktop GUI
- **Export Options**: JSON and CSV export capabilities
- **Real-time Comparison**: Live web interface with progress tracking
- **Enhanced GUI**: Desktop application with site previews and monthly charts
- **Historical Analysis**: 12-month trend visualization
- **Automatic Charts**: Monthly graphs generated automatically for each analyzed site
- **Combined Comparison**: All analyzed sites displayed together in unified charts
- **Cost-Effective**: Works with free APIs ($0/month) instead of expensive services

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Tool** (Choose one method):

   **Method 1: Using Batch Files (Recommended - No Virtual Environment Issues)**
   ```bash
   # Web interface
   run_web.bat
   
   # Desktop GUI
   run_gui.bat
   
   # Command line
   run_cli.bat google.com facebook.com
   ```

   **Method 2: Using Python Directly**
   ```bash
   # Activate virtual environment first
   .\venv\Scripts\activate
   
   # Web interface
   python run_tool.py --mode web
   
   # Desktop GUI
   python gui_app.py
   
   # Command line
   python run_tool.py --mode cli --domains google.com facebook.com
   ```

## Usage

### Web Interface (Recommended)

1. Start the web server:
   ```bash
   python run_tool.py --mode web
   ```

2. Open your browser and go to: http://localhost:5000

3. Enter domain names to compare (e.g., google.com, facebook.com)

4. Click "Compare Websites" and wait for results

5. Download results in JSON or CSV format

### Desktop GUI Application

1. Start the GUI application:
   ```bash
   python gui_app.py
   ```

2. Features:
   - **Site Selection**: Enter up to 3 domains for comparison
   - **Quick Site Selection**: Dropdown menus with Trieste news sites for each analysis box
     - All boxes: triesteallnews.it, triesteprima.it, triestecafe.it
   - **Individual Analysis**: Analyze each site separately
   - **Live Previews**: See metrics as they're analyzed
   - **Traffic Sources**: Detailed breakdown of traffic sources
   - **Automatic Monthly Charts**: 12-month trend visualizations generated automatically
   - **Combined Charts**: All analyzed sites shown together in unified comparison charts
   - **Consistent Results**: Same site always returns identical results for reliable analysis
   - **Export Options**: Save results as CSV or JSON

### Command Line Interface

```bash
# Compare two websites
python run_tool.py --mode cli --domains google.com facebook.com

# Compare multiple websites with output file
python run_tool.py --mode cli --domains google.com facebook.com amazon.com --output results.csv

# Direct usage
python web_ranking_tool.py google.com facebook.com --output comparison.csv
```

## Data Sources

### SimilarWeb
- Global and country rankings
- Monthly visit estimates
- Bounce rate and engagement metrics
- Traffic source breakdown
- Geographic distribution

### Alexa (Historical)
- Global and country rankings
- Visit estimates
- Engagement metrics

### SEMrush
- SEO-focused rankings
- Organic search performance
- Traffic source analysis

## API Configuration

### Free APIs (Recommended) 🆓
- **BuiltWith API**: Technology detection (500 requests/month free)
- **Wappalyzer API**: Tech stack analysis (1,000 requests/month free)
- **Google PageSpeed API**: Performance metrics (25,000 requests/day free)
- **Total Cost**: $0/month!

### Paid APIs (Optional) 💰
- **SimilarWeb API**: Traffic data (~$1,167/month minimum)
- **SEMrush API**: SEO data (~$1,167/month minimum)

### Quick Setup
1. **For Free APIs**: Get free API keys and update `config.py`
2. **For Testing**: Use mock data (default)
3. **For Paid APIs**: Get expensive API keys and update `config.py`
4. **Troubleshooting**: See `API_TROUBLESHOOTING.md`

### Test Your APIs
```bash
.\test_api.bat
```

### Free API Setup Guide
See `FREE_APIS_GUIDE.md` for detailed instructions on getting free API keys.

## Metrics Explained

- **Global Rank**: Worldwide ranking based on traffic
- **Country Rank**: Ranking within specific country
- **Monthly Visits**: Estimated unique monthly visitors
- **Bounce Rate**: Percentage of single-page visits
- **Avg Visit Duration**: Average time spent on site
- **Pages per Visit**: Average pages viewed per session
- **Traffic Sources**: Breakdown by Direct, Search, Social, etc.
- **Top Countries**: Geographic distribution of visitors

## API Integration

The tool is designed to work with real APIs. To use actual data:

1. **SimilarWeb API**: Get API key from SimilarWeb
2. **SEMrush API**: Get API key from SEMrush
3. **Update the tool**: Replace mock data functions with real API calls

## File Structure

```
WebRankingTool/
├── web_ranking_tool.py      # Core comparison logic
├── web_interface.py         # Flask web application
├── gui_app.py              # Desktop GUI application
├── run_tool.py             # Main runner script
├── config.py               # Configuration file
├── requirements.txt        # Python dependencies (web interface)
├── requirements_gui.txt    # Python dependencies (GUI app)
├── run_web.bat            # Windows batch file to start web interface
├── run_gui.bat            # Windows batch file to start GUI
├── run_cli.bat            # Windows batch file to start CLI
├── start_web.bat          # Legacy batch file
├── start_gui.bat          # Legacy batch file
├── templates/
│   └── index.html         # Web interface template
└── README.md              # This file
```

## Example Output

```
🌐 GOOGLE.COM
--------------------------------------------------
📊 Source: SimilarWeb
   Global Rank: 1
   Country Rank: 1
   Monthly Visits: 89,000,000,000
   Bounce Rate: 28.5%
   Avg Visit Duration: 3:45
   Pages per Visit: 8.2

📊 Source: Alexa
   Global Rank: 1
   Country Rank: 1
   Monthly Visits: 85,000,000,000
   Bounce Rate: 25.2%
   Avg Visit Duration: 4:12
   Pages per Visit: 9.1
```

## Requirements

- Python 3.7+
- Flask 3.0.0+
- Requests 2.31.0+
- Internet connection for data fetching

## Limitations

- **Mock Data**: Current version uses simulated data for demonstration
- **Rate Limits**: Real APIs have rate limiting and usage restrictions
- **API Keys**: Production use requires valid API keys for data sources
- **Data Accuracy**: Rankings may vary between sources due to different methodologies

## Future Enhancements

- Real API integrations
- Historical trend analysis
- Competitor analysis features
- Custom metric definitions
- Advanced visualization
- Batch processing capabilities
- API rate limiting management

## Support

For issues or questions:
1. Check the console output for error messages
2. Ensure all dependencies are installed
3. Verify internet connectivity
4. Check domain name format (no http:// or www.)

## License

This tool is provided as-is for educational and research purposes.

