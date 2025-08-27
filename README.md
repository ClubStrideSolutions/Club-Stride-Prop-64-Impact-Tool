# Club-Stride-Prop-64-Impact-Tool

## 📊 AI-Enhanced KPI Dashboard System

A sophisticated KPI Dashboard System powered by dual AI intelligence from OpenAI GPT-4 and Claude 3 Opus. This system provides comprehensive KPI management with advanced document processing, Excel generation, and intelligent insights.

## 🚀 Key Features

### Document Intelligence
- **Multi-format Support**: Process SOW, Requirements, Project Charters, Word docs, PDFs, and more
- **Smart Extraction**: Automatically identifies and extracts KPIs, goals, projects, and measurements
- **Pattern Recognition**: Uses advanced regex patterns to find KPI-related information
- **Template Generation**: Creates starter KPIs when none are found in documents

### Excel Excellence
- **8 Professional Sheets**: Dashboard, KPI Details, Performance Matrix, Analytics, Risk Analysis, Timeline, Summary, Raw Data
- **Advanced Formatting**: Conditional formatting, data validation, color coding, charts
- **Interactive Charts**: Pie, Bar, Line, Heatmap, Gauge, and more using Plotly
- **Auto-calculations**: Health scores, risk assessments, completion percentages

### AI-Powered Analytics
- **Health Score Calculation**: Multi-factor scoring (completion, progress, status, recency)
- **Risk Assessment**: Comprehensive risk scoring with mitigation recommendations
- **Predictive Analytics**: Timeline predictions and completion forecasts
- **Smart Insights**: AI-style recommendations based on data patterns
- **Trend Analysis**: Historical tracking and pattern identification

### Interactive Dashboard
- **8 View Modes**: Executive, Analytics, Details, Editor, Performance, Risk, Success, Reports
- **Real-time Updates**: Live data validation and instant calculations
- **Advanced Filtering**: Multi-criteria filtering by project, status, owner, date
- **Search Functionality**: Fast search across all KPI fields
- **Data Editor**: In-line editing with validation

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
```bash
cd "C:\Users\jbclu\OneDrive\Documents\Software Platforms\Python_dev\all_kpi\enhanced_kpi_system"
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## 🎯 Quick Start Guide

### 1. Upload Documents
- Click "Process Document" in the sidebar
- Select document type (SOW, Requirements, etc.)
- Upload your file or paste text
- System automatically extracts KPIs

### 2. Upload Excel Files
- Click "Upload Excel File" in the sidebar
- Select your existing KPI Excel file
- System processes all sheets automatically
- Enriches data with analytics

### 3. Use Sample Data
- Click "Load Sample Data" in the sidebar
- Choose from Youth Health, Digital Transformation, or Sustainability templates
- Explore features with pre-configured data

### 4. Generate Reports
- Navigate to the "Reports" tab
- Select report type (Executive Summary, Risk Assessment, etc.)
- Choose format (PDF, Excel, Word, HTML)
- Click "Generate Report"

## 📁 Project Structure

```
enhanced_kpi_system/
├── main.py                 # Main application entry point
├── document_processor.py   # Document parsing and KPI extraction
├── excel_generator.py      # Advanced Excel generation
├── analytics_engine.py     # AI insights and predictions
├── visualization_engine.py # Interactive chart creation
├── data_validator.py       # Data validation and cleaning
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Data storage directory
├── reports/              # Generated reports directory
├── temp/                 # Temporary files
└── uploads/              # Uploaded files directory
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Thresholds**: Health score limits, risk levels, stale data days
- **Colors**: UI color scheme and status colors
- **Labels**: Status labels, progress descriptions
- **Paths**: Data directories, upload limits
- **Preferences**: Default user preferences

## 📊 Features in Detail

### Document Processing
The system can process:
- **SOW Documents**: Extracts projects, goals, and KPIs
- **Requirements**: Converts requirements to measurable KPIs
- **Project Charters**: Identifies success criteria and metrics
- **Custom Text**: Processes any text with KPI-related content

### Excel Generation
Creates comprehensive Excel workbooks with:
- **Dashboard Sheet**: Key metrics, status charts, top KPIs
- **KPI Details**: Sortable, filterable table with all KPI data
- **Performance Matrix**: Project vs. status heatmap
- **Analytics Sheet**: Statistical summary and insights
- **Risk Analysis**: Risk scores and mitigation recommendations
- **Timeline Sheet**: Gantt-style project timeline
- **Summary Sheet**: Executive summary with charts
- **Raw Data**: Editable data with validation

### Analytics Features
- **Health Score**: 0-100 score based on multiple factors
- **Risk Assessment**: Identifies and scores risk factors
- **Predictions**: Estimates completion dates using ML
- **Insights**: Generates actionable recommendations
- **Correlations**: Analyzes relationships between metrics
- **Trends**: Tracks changes over time

### Visualization Options
- **Health Distribution**: Bar chart of health score ranges
- **Status Breakdown**: Donut chart of KPI statuses
- **Project Performance**: Horizontal bar comparison
- **Performance Matrix**: Heatmap of projects vs. status
- **Risk Distribution**: Gauge charts for risk levels
- **Timeline Analysis**: Line chart of KPI trends
- **Correlation Heatmap**: Relationship analysis
- **Owner Workload**: Bubble chart of responsibilities

## 🎨 Customization

### Adding New Document Types
Edit `document_processor.py`:
```python
def process_custom_doc(self, file):
    # Add your custom parsing logic
    pass
```

### Custom Analytics
Edit `analytics_engine.py`:
```python
def custom_metric(self, data):
    # Add your custom calculations
    pass
```

### New Visualizations
Edit `visualization_engine.py`:
```python
def create_custom_chart(self, data):
    # Add your Plotly chart
    pass
```

## 📈 Best Practices

1. **Regular Updates**: Update KPIs at least weekly for accurate insights
2. **Complete Data**: Fill in all fields for better analytics
3. **Consistent Naming**: Use consistent project and owner names
4. **Target Setting**: Set realistic, measurable targets
5. **Document Quality**: Provide detailed SOW/requirements for better extraction

## 🔍 Troubleshooting

### Common Issues

**Application won't start**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

**Excel generation fails**
- Verify openpyxl is installed: `pip install openpyxl`
- Check data has required columns

**Document parsing errors**
- Ensure document is in supported format
- Check file isn't corrupted
- Try pasting text directly instead

**Charts not displaying**
- Update Plotly: `pip install --upgrade plotly`
- Clear browser cache
- Try different browser

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the configuration in `config.py`
3. Ensure all dependencies are up to date

## 📄 License

This Enhanced KPI Dashboard System is provided as-is for KPI tracking and analytics purposes.

## 🎯 Next Steps

1. **Run the application**: `streamlit run main.py`
2. **Upload your documents**: SOW, requirements, or Excel files
3. **Explore the dashboard**: Navigate through different views
4. **Generate reports**: Export professional Excel dashboards
5. **Customize as needed**: Modify configuration and add features

---

**Built with best practices from multiple KPI tracking systems to exceed requirements and provide comprehensive KPI management capabilities.**