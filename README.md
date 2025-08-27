# Club-Stride-Prop-64-Impact-Tool

## 📊 KPI Dashboard System with AI Integration

A streamlined KPI tracking and analytics dashboard powered by OpenAI GPT-4 and Claude 3.5 Sonnet.

## ✨ Core Features

- **KPI Management**: Track, monitor, and analyze key performance indicators
- **Excel Import/Export**: Load existing KPI data and generate comprehensive reports
- **AI-Powered Insights**: Get intelligent recommendations using OpenAI and Claude
- **Interactive Visualizations**: Charts and graphs powered by Plotly
- **Real-time Analytics**: Health scores, risk assessments, and predictions

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ClubStrideSolutions/Club-Stride-Prop-64-Impact-Tool.git
cd Club-Stride-Prop-64-Impact-Tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up AI API keys (optional)**

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

4. **Run the application**
```bash
streamlit run main.py
```

The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
enhanced_kpi_system/
├── main.py                    # Main application entry point
├── modules/                   # Core modules
│   ├── ai_orchestrator.py    # AI integration (OpenAI & Claude)
│   ├── analytics_engine.py   # Analytics and predictions
│   ├── data_validator.py     # Data validation
│   ├── document_processor.py # Document parsing
│   ├── excel_generator.py    # Excel report generation
│   └── visualization_engine.py # Chart creation
├── data/                      # Sample data files
├── .env.example              # Example environment variables
└── requirements.txt          # Python dependencies
```

## 📊 How to Use

1. **Load Data**: 
   - Upload an Excel file with your KPIs
   - Or use the sample data to explore features
   - Or manually add KPIs

2. **View Dashboard**:
   - **Overview**: Status distribution and performance metrics
   - **Analytics**: Risk analysis and predictions
   - **Performance**: Track KPI performance over time
   - **AI Insights**: Get AI-powered recommendations (requires API keys)
   - **Data Table**: Edit and manage KPI data directly

3. **Export Reports**:
   - Generate comprehensive Excel reports
   - Download formatted dashboards with charts

## 🔧 Configuration

The AI features are optional. The dashboard works fully without API keys, but you won't get AI-powered insights.

To enable AI features:
1. Get API keys from [OpenAI](https://platform.openai.com) and/or [Anthropic](https://console.anthropic.com)
2. Add them to your `.env` file
3. Restart the application

## 📈 KPI Data Format

Your Excel file should include these columns:
- `kpi_name`: Name of the KPI
- `current_value`: Current performance value
- `target_value`: Target/goal value
- `status`: Current status (On Track, At Risk, Achieved, Not Started)
- `owner`: Responsible person/department
- `last_updated`: Date of last update

## 🤝 Support

For issues or questions, please create an issue on the [GitHub repository](https://github.com/ClubStrideSolutions/Club-Stride-Prop-64-Impact-Tool/issues).

---

**Built with Streamlit, Pandas, and Plotly for comprehensive KPI management.**