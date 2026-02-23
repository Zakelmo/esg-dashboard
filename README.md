# ESG Company Analyzer Dashboard - Enhanced Edition

A comprehensive, professional-grade ESG (Environmental, Social, Governance) analytics dashboard built with Python and Streamlit. This advanced tool analyzes, visualizes, and predicts ESG performance metrics, helping investors, analysts, and sustainability professionals make data-driven decisions.

Dashboard Preview: https://esg2.smartdeploy.net

## ✨ Enhanced Features

### Core Analytics
- **ESG Score Overview**: View comprehensive E, S, G scores with interactive visualizations
- **Trend Analysis**: Track ESG performance evolution with multi-year historical data
- **Company Deep Dive**: Detailed analysis of individual company ESG performance
- **Risk Assessment**: Automated identification of ESG risks with severity classification
- **Sector Benchmarking**: Statistical comparison against industry peers

### 🎯 Advanced Features (NEW)

#### 1. Dual Theme System
- **Light & Dark Modes**: Professional themes optimized for different viewing conditions
- **Dynamic Switching**: Toggle between themes with a single click
- **Theme-Aware Charts**: All visualizations automatically adapt to the selected theme

#### 2. ESG Score Simulator
- **What-If Analysis**: Model the impact of ESG improvements on overall scores
- **5-Year Projections**: Predict future ESG trajectories based on improvement targets
- **Interactive Sliders**: Adjust improvement parameters in real-time
- **Impact Metrics**: See how changes affect ESG ratings and percentile rankings
- **Visual Comparisons**: Side-by-side charts of current vs projected scores

#### 3. Advanced Peer Benchmarking
- **Sector Benchmarking**: Compare against all companies in the same sector
- **Custom Peer Groups**: Select specific competitors for detailed comparison
- **Percentile Rankings**: Understand where a company stands relative to peers
- **Statistical Analysis**: Z-scores, quartiles, and sector distribution metrics
- **Competitive Insights**: Automated identification of strengths and weaknesses
- **Heatmap Visualizations**: Multi-dimensional performance comparison matrix
- **Spider Charts**: Radar plots comparing multiple companies across ESG pillars

#### 4. Professional PDF Report Generator
- **Company Reports**: Comprehensive PDF reports with:
  - Executive summary with key insights
  - Complete ESG score breakdown
  - Environmental, Social, and Governance metrics
  - Risk assessment and severity levels
  - Actionable recommendations
  - Professional formatting and styling
- **Portfolio Reports**: Multi-company comparison reports
- **One-Click Export**: Generate and download PDF reports instantly
- **Presentation-Ready**: Formatted for stakeholder presentations and compliance

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.9+** - Programming language
- **Streamlit 1.29.0** - Web application framework with enhanced UI components
- **Pandas 2.1.3** - Data manipulation and analysis
- **Plotly 5.18.0** - Interactive, theme-aware visualizations
- **NumPy 1.26.2** - Numerical computing and statistical operations

### Enhanced Modules
- **ReportLab 4.0.7** - Professional PDF generation
- **Pillow 10.1.0** - Image processing for reports
- **Kaleido 0.2.1** - Static image export for charts

## 📁 Project Structure

```
esg-dashboard/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── app.py                       # Main Streamlit application (enhanced)
├── src/
│   ├── __init__.py
│   ├── data_loader.py           # Data loading and processing
│   ├── esg_analyzer.py          # ESG analysis functions
│   ├── visualizations.py        # Enhanced charts with theme support
│   ├── pdf_generator.py         # NEW: PDF report generator
│   ├── esg_simulator.py         # NEW: ESG score simulation engine
│   └── peer_benchmark.py        # NEW: Advanced benchmarking analytics
├── data/
│   └── esg_data.csv             # Sample ESG dataset
└── assets/
    └── style.css                # Enhanced CSS with dual theme support
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/esg-dashboard.git
cd esg-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Data Sources

This demo uses synthetic ESG data that simulates real-world ESG ratings. The data includes:

- **Environmental Score**: Carbon emissions, energy efficiency, waste management
- **Social Score**: Labor practices, community relations, diversity & inclusion
- **Governance Score**: Board composition, executive compensation, shareholder rights

For production use, you can integrate with:
- Yahoo Finance ESG data
- Refinitiv ESG scores
- MSCI ESG ratings
- Sustainalytics

## 📈 ESG Scoring Methodology

| Score Range | Rating | Description |
|-------------|--------|-------------|
| 80-100 | AAA/AA | Leader - Best in class ESG performance |
| 60-79 | A/BBB | Above Average - Strong ESG practices |
| 40-59 | BB/B | Average - Room for improvement |
| 20-39 | CCC | Below Average - Significant ESG risks |
| 0-19 | CC/C | Laggard - Poor ESG performance |

## 📖 User Guide

### Getting Started

1. **Theme Selection**: Use the theme toggle in the sidebar to switch between Light and Dark modes
2. **Filters**: Select sectors, countries, and year ranges to focus your analysis
3. **Navigation**: Use the 8 tabs to access different features:
   - **Overview**: Market-wide ESG metrics and trends
   - **Company Analysis**: Deep dive into individual companies
   - **Trends & Comparison**: Historical analysis and multi-company comparison
   - **Risk Assessment**: Identify and categorize ESG risks
   - **Rankings**: Company rankings by various ESG metrics
   - **ESG Simulator**: Model improvement scenarios
   - **Peer Benchmarking**: Advanced competitive analysis
   - **PDF Reports**: Generate professional reports

### Using the ESG Simulator

1. Select a company from the dropdown
2. Adjust the improvement sliders for E, S, and G pillars (0-50%)
3. View real-time updates showing:
   - Current vs. projected scores
   - Rating changes
   - 5-year trajectory projections
4. Use insights to set realistic ESG improvement targets

### Creating PDF Reports

**Company Reports:**
1. Navigate to the PDF Reports tab
2. Select "Company Report"
3. Choose a company
4. Click "Generate PDF Report"
5. Download the professional PDF with one click

**Portfolio Reports:**
1. Select "Portfolio Report"
2. Choose multiple companies to compare
3. Generate a consolidated portfolio analysis

### Peer Benchmarking Options

- **Sector Benchmarking**: Compare against all sector peers with statistical metrics
- **Custom Peer Group**: Select 2-5 specific competitors for detailed comparison
- **Percentile Analysis**: Understand ranking across multiple ESG dimensions

## 🎨 Screenshots

### Main Dashboard
View overall ESG scores and key metrics at a glance with enhanced styling.

### ESG Simulator
Model what-if scenarios with interactive controls and 5-year projections.

### Peer Benchmarking
Advanced competitive analysis with heatmaps and percentile rankings.

### PDF Reports
Generate professional, presentation-ready reports with comprehensive ESG analytics.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Zakaria El Morabit**
- LinkedIn: [Your LinkedIn Profile]
- Email: elmorabitzakaria@gmail.com

---

*Built as a portfolio project demonstrating ESG analytics and data visualization skills.*
