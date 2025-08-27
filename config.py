"""
Configuration Module
====================
Central configuration for the Enhanced KPI System.
"""

import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # Application settings
    APP_NAME = "Enhanced KPI Dashboard System"
    APP_VERSION = "2.0.0"
    APP_TITLE = "📊 KPI Intelligence Dashboard"
    APP_SUBTITLE = "Transform Your KPI Tracking with AI-Powered Insights"
    APP_ICON = "📊"
    
    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    REPORTS_DIR = BASE_DIR / "reports"
    TEMP_DIR = BASE_DIR / "temp"
    UPLOADS_DIR = BASE_DIR / "uploads"
    
    # Create directories if they don't exist
    for dir_path in [DATA_DIR, REPORTS_DIR, TEMP_DIR, UPLOADS_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # Database settings (if using MongoDB or other DB)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///kpi_data.db")
    
    # File upload settings
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {
        'excel': ['.xlsx', '.xls', '.xlsm'],
        'document': ['.pdf', '.docx', '.txt', '.md'],
        'data': ['.csv', '.json', '.xml']
    }
    
    # Analytics settings
    INSIGHT_THRESHOLDS = {
        'critical_health': 50,
        'warning_health': 70,
        'good_health': 80,
        'stale_days': 14,
        'critical_stale_days': 30,
        'at_risk_threshold': 0.3,
        'success_threshold': 0.7
    }
    
    # Visualization settings
    COLOR_SCHEME = {
        'primary': '#2C57FA',
        'secondary': '#FA962C',
        'success': '#1B5E20',
        'warning': '#F57C00',
        'danger': '#C62828',
        'info': '#0288D1',
        'light': '#F8F9FA',
        'dark': '#343A40'
    }
    
    # Status mappings
    STATUS_LABELS = {
        'G': '🟢 On Track',
        'Y': '🟡 Needs Attention',
        'R': '🔴 At Risk'
    }
    
    STATUS_ICONS = {
        'G': '🟢',
        'Y': '🟡',
        'R': '🔴'
    }
    
    # Progress levels
    PROGRESS_LEVELS = {
        1: 'Limited engagement; critical actions not initiated',
        2: 'Targets unmet; requires urgent support and redirection',
        3: 'Partial progress; improvement plan underway',
        4: 'Steady development; more consistency required',
        5: 'Strong momentum; measurable impact aligned with goals'
    }
    
    # Risk levels
    RISK_LEVELS = {
        'Low': {'min': 0, 'max': 30, 'color': '#1B5E20'},
        'Medium': {'min': 30, 'max': 70, 'color': '#F57C00'},
        'High': {'min': 70, 'max': 100, 'color': '#C62828'}
    }
    
    # Default preferences
    DEFAULT_PREFERENCES = {
        'theme': 'Light',
        'auto_save': False,
        'notifications': True,
        'advanced_analytics': True,
        'chart_type': 'interactive',
        'export_format': 'excel'
    }
    
    # Column configuration for data editor
    COLUMN_CONFIG = {
        "kpi_name": {
            "label": "KPI Name",
            "type": "text",
            "required": True,
            "help": "Name or title of the KPI"
        },
        "project": {
            "label": "Project",
            "type": "text",
            "required": True,
            "help": "Project or program name"
        },
        "goal": {
            "label": "Goal",
            "type": "text",
            "help": "Primary goal or objective"
        },
        "description": {
            "label": "Description",
            "type": "text",
            "help": "Detailed description of the KPI"
        },
        "owner": {
            "label": "Owner",
            "type": "text",
            "required": True,
            "help": "Person responsible for this KPI"
        },
        "status": {
            "label": "Status",
            "type": "select",
            "options": ["G", "Y", "R"],
            "required": True,
            "help": "Current status (Green/Yellow/Red)"
        },
        "progress": {
            "label": "Progress",
            "type": "number",
            "min": 1,
            "max": 5,
            "step": 1,
            "required": True,
            "help": "Progress level (1-5 scale)"
        },
        "target_value": {
            "label": "Target Value",
            "type": "number",
            "min": 0,
            "help": "Target numeric value"
        },
        "actual_value": {
            "label": "Actual Value",
            "type": "number",
            "min": 0,
            "help": "Current actual value"
        },
        "last_updated": {
            "label": "Last Updated",
            "type": "datetime",
            "required": True,
            "help": "Date of last update"
        },
        "health_score": {
            "label": "Health Score",
            "type": "number",
            "min": 0,
            "max": 100,
            "readonly": True,
            "help": "Calculated health score (0-100)"
        },
        "risk_score": {
            "label": "Risk Score",
            "type": "number",
            "min": 0,
            "max": 100,
            "readonly": True,
            "help": "Calculated risk score (0-100)"
        }
    }
    
    # Sample data templates
    SAMPLE_TEMPLATES = {
        'Youth Health Program': {
            'description': 'KPIs for youth health and wellness initiatives',
            'kpi_count': 5,
            'categories': ['Health Education', 'STI Prevention', 'Peer Support', 'Community Outreach']
        },
        'Digital Transformation': {
            'description': 'Technology modernization and digital adoption KPIs',
            'kpi_count': 4,
            'categories': ['System Migration', 'Training', 'User Adoption', 'Performance']
        },
        'Sustainability Initiative': {
            'description': 'Environmental and sustainability program KPIs',
            'kpi_count': 4,
            'categories': ['Carbon Reduction', 'Energy', 'Waste Management', 'Water Conservation']
        }
    }
    
    # Export formats
    EXPORT_FORMATS = {
        'excel_advanced': {
            'name': 'Excel (Advanced)',
            'extension': '.xlsx',
            'mime': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        },
        'excel_simple': {
            'name': 'Excel (Simple)',
            'extension': '.xlsx',
            'mime': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        },
        'csv': {
            'name': 'CSV',
            'extension': '.csv',
            'mime': 'text/csv'
        },
        'json': {
            'name': 'JSON',
            'extension': '.json',
            'mime': 'application/json'
        }
    }
    
    # Custom CSS for Streamlit - Simplified and safer
    CUSTOM_CSS = """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Main container adjustments */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Metric improvements */
        [data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        /* Button styles */
        .stButton > button {
            border-radius: 0.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Expander improvements */
        .streamlit-expanderHeader {
            font-weight: 500;
            border-radius: 0.5rem;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 0.5rem 0.5rem 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(44, 87, 250, 0.1);
        }
        
        /* Info, warning, error boxes */
        .stAlert {
            border-radius: 0.5rem;
            border-left-width: 4px;
        }
        
        /* Dataframe styling */
        .dataframe {
            font-size: 14px;
        }
        
        /* Sidebar improvements */
        section[data-testid="stSidebar"] {
            background-color: rgba(248, 249, 250, 0.5);
        }
        
        /* Custom container styles */
        div[data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }
        
        /* Progress bar colors */
        .stProgress > div > div > div > div {
            background-color: #2C57FA;
        }
        
        /* Select box improvements */
        .stSelectbox > div > div {
            border-radius: 0.5rem;
        }
        
        /* Text input improvements */
        .stTextInput > div > div {
            border-radius: 0.5rem;
        }
        
        /* File uploader improvements */
        .stFileUploader > div {
            border-radius: 0.5rem;
        }
    </style>
    """