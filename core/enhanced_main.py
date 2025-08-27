"""
Enhanced KPI Dashboard System with Create and Review Modes
===========================================================
Create Mode: Generate new dashboards from documents
Review Mode: Update and interact with existing dashboards
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path
import json
import io
import base64

# Import existing modules
from analytics_engine import AnalyticsEngine
from visualization_engine import VisualizationEngine
from document_processor import DocumentProcessor
from data_validator import DataValidator
from excel_generator import ExcelGenerator
from ui_components import UIComponents
from config import Config

# Import AI Orchestrator
try:
    from ai_orchestrator import get_orchestrator
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("AI Orchestrator not available. Some features will be limited.")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="KPI Dashboard System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(Config.CUSTOM_CSS, unsafe_allow_html=True)

class EnhancedKPIDashboard:
    """Enhanced KPI Dashboard with Create and Review modes"""
    
    def __init__(self):
        self.analytics = AnalyticsEngine()
        self.viz_engine = VisualizationEngine()
        self.doc_processor = DocumentProcessor()
        self.validator = DataValidator()
        self.excel_gen = ExcelGenerator()
        self.ui = UIComponents()
        self.config = Config
        
        # Initialize AI Orchestrator if available
        self.ai = get_orchestrator() if AI_AVAILABLE else None
        
        # Initialize session state
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'mode' not in st.session_state:
            st.session_state.mode = None
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'dashboard_config' not in st.session_state:
            st.session_state.dashboard_config = {}
        if 'generated_code' not in st.session_state:
            st.session_state.generated_code = None
    
    def run(self):
        """Main application entry point"""
        
        # Header with AI status
        ai_status = self._get_ai_status()
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='margin: 0;'>📊 KPI Dashboard System</h1>
            <p style='margin: 0.5rem 0 0 0;'>Create or Review KPI Dashboards with AI Intelligence</p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9em;'>{ai_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mode Selection
        if st.session_state.mode is None:
            self.show_mode_selection()
        else:
            # Show selected mode
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                current_mode = st.session_state.mode
                st.info(f"**Current Mode:** {current_mode}")
                if st.button("🔄 Change Mode", use_container_width=True):
                    st.session_state.mode = None
                    st.session_state.data = None
                    st.session_state.generated_code = None
                    st.rerun()
            
            # Run selected mode
            if st.session_state.mode == "Review":
                self.run_review_mode()
            elif st.session_state.mode == "Create":
                self.run_create_mode()
    
    def show_mode_selection(self):
        """Show mode selection interface"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 300px;'>
                <h2 style='color: #2c5282;'>📝 Review Mode</h2>
                <p>Update and interact with existing KPI dashboards</p>
                <ul>
                    <li>Upload Excel/CSV files</li>
                    <li>View analytics and insights</li>
                    <li>Update KPI values</li>
                    <li>Generate reports</li>
                    <li>Export visualizations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Enter Review Mode", key="review_btn", use_container_width=True):
                st.session_state.mode = "Review"
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style='padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 300px;'>
                <h2 style='color: #2c5282;'>🚀 Create Mode</h2>
                <p>Generate new dashboards from documents</p>
                <ul>
                    <li>Upload requirements documents</li>
                    <li>Auto-generate Python code</li>
                    <li>Follow technical guidelines</li>
                    <li>Create custom visualizations</li>
                    <li>Export complete dashboard</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Enter Create Mode", key="create_btn", use_container_width=True):
                st.session_state.mode = "Create"
                st.rerun()
    
    def run_review_mode(self):
        """Run Review Mode - interact with existing dashboards"""
        st.markdown("## 📝 Review Mode - Manage Existing Dashboards")
        
        # Sidebar for navigation
        with st.sidebar:
            st.markdown("### Navigation")
            page = st.radio(
                "Select Section",
                ["📁 Data Upload", "📊 Overview", "📈 Analytics", "📋 Details", "📄 Reports"]
            )
        
        # Main content area
        if page == "📁 Data Upload":
            self.show_data_upload()
        elif page == "📊 Overview":
            self.show_overview()
        elif page == "📈 Analytics":
            self.show_analytics()
        elif page == "📋 Details":
            self.show_details()
        elif page == "📄 Reports":
            self.show_reports()
    
    def run_create_mode(self):
        """Run Create Mode - generate new dashboards from documents"""
        st.markdown("## 🚀 Create Mode - Generate New Dashboard")
        
        # Create tabs for the workflow
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload Documents", "⚙️ Configure", "🔨 Generate", "📥 Export"])
        
        with tab1:
            self.upload_requirements_docs()
        
        with tab2:
            self.configure_dashboard()
        
        with tab3:
            self.generate_dashboard_code()
        
        with tab4:
            self.export_dashboard()
    
    def show_data_upload(self):
        """Data upload interface for Review mode"""
        st.markdown("### Upload KPI Data")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['xlsx', 'xls', 'csv'],
            help="Upload Excel or CSV file with KPI data"
        )
        
        if uploaded_file:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Validate and process
                validation_results = self.validator.validate_dataframe(df)
                
                if validation_results['is_valid']:
                    st.success(f"✅ Successfully loaded {len(df)} KPIs")
                    st.session_state.data = df
                    
                    # Show preview
                    with st.expander("Data Preview"):
                        st.dataframe(df.head(10))
                    
                    # Show AI-enhanced insights
                    st.markdown("### Key Insights")
                    
                    if self.ai:
                        # AI model selection
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            ai_mode = st.selectbox(
                                "AI Model",
                                ["Both", "OpenAI", "Claude"],
                                key="insight_model"
                            )
                        
                        # Get AI insights
                        with st.spinner("Generating AI insights..."):
                            ai_insights = self.ai.generate_insights(df, context="KPI Dashboard Analysis")
                            
                            # Display insights with source
                            for insight in ai_insights[:5]:
                                source = insight.get('source', 'unknown')
                                icon = "🤖" if source == "openai" else "🧠" if source == "claude" else "💡"
                                st.info(f"{icon} **{insight.get('title', '')}:** {insight.get('message', '')}")
                    else:
                        # Fallback to regular insights
                        insights = self.analytics.generate_insights(df)
                        for insight in insights[:5]:
                            if isinstance(insight, dict):
                                st.info(f"**{insight.get('title', '')}:** {insight.get('message', '')}")
                            else:
                                st.info(str(insight))
                else:
                    st.error("Data validation failed")
                    for error in validation_results['errors']:
                        st.error(f"• {error}")
                        
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
        
        # Sample data option
        if st.button("Load Sample Data"):
            st.session_state.data = self.generate_sample_data()
            st.success("Sample data loaded successfully!")
            st.rerun()
    
    def upload_requirements_docs(self):
        """Upload requirements documents for Create mode"""
        st.markdown("### Upload Requirements Documents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Primary Document")
            main_doc = st.file_uploader(
                "Upload main requirements",
                type=['pdf', 'docx', 'txt', 'md'],
                key="main_doc"
            )
            
            if main_doc:
                st.success(f"Uploaded: {main_doc.name}")
                # Process document
                doc_content = self.doc_processor.process_document(main_doc)
                st.session_state.dashboard_config['main_requirements'] = doc_content
        
        with col2:
            st.markdown("#### Supporting Documents")
            support_docs = st.file_uploader(
                "Upload additional documents",
                type=['pdf', 'docx', 'txt', 'md'],
                accept_multiple_files=True,
                key="support_docs"
            )
            
            if support_docs:
                st.success(f"Uploaded {len(support_docs)} supporting documents")
        
        # Show technical guidelines
        st.markdown("### Technical Guidelines")
        guidelines = st.selectbox(
            "Select guideline template",
            ["General", "Claude-specific", "GPT-specific", "Custom"]
        )
        
        if guidelines != "Custom":
            st.info(f"Using {guidelines} technical requirements template")
        else:
            custom_guide = st.text_area(
                "Enter custom guidelines",
                height=200,
                placeholder="Enter your custom technical requirements..."
            )
    
    def configure_dashboard(self):
        """Configure dashboard settings for Create mode"""
        st.markdown("### Dashboard Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Basic Settings")
            
            dashboard_name = st.text_input("Dashboard Name", "My KPI Dashboard")
            dashboard_type = st.selectbox(
                "Dashboard Type",
                ["Standard KPI", "Project Management", "Sales", "Marketing", "Custom"]
            )
            
            update_frequency = st.selectbox(
                "Update Frequency",
                ["Real-time", "Daily", "Weekly", "Monthly"]
            )
        
        with col2:
            st.markdown("#### Visual Settings")
            
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            chart_types = st.multiselect(
                "Chart Types to Include",
                ["Bar", "Line", "Pie", "Scatter", "Heatmap", "Gauge"],
                default=["Bar", "Line", "Pie"]
            )
            
            enable_animations = st.checkbox("Enable animations", value=True)
        
        # KPI Structure
        st.markdown("#### KPI Structure")
        
        kpi_fields = st.multiselect(
            "Select KPI fields to track",
            ["Name", "Description", "Target", "Actual", "Status", "Owner", 
             "Department", "Start Date", "End Date", "Priority", "Tags"],
            default=["Name", "Target", "Actual", "Status", "Owner"]
        )
        
        # Save configuration
        if st.button("Save Configuration"):
            st.session_state.dashboard_config.update({
                'name': dashboard_name,
                'type': dashboard_type,
                'update_frequency': update_frequency,
                'theme': theme,
                'chart_types': chart_types,
                'animations': enable_animations,
                'kpi_fields': kpi_fields
            })
            st.success("Configuration saved!")
    
    def generate_dashboard_code(self):
        """Generate Python dashboard code using AI"""
        st.markdown("### Generate Dashboard Code with AI")
        
        if not st.session_state.dashboard_config:
            st.warning("Please configure dashboard settings first")
            return
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            framework = st.selectbox(
                "Select Framework",
                ["Streamlit", "Plotly Dash", "Panel", "Bokeh"]
            )
        
        with col2:
            if self.ai:
                ai_model = st.selectbox(
                    "AI Model",
                    ["Both", "OpenAI", "Claude"],
                    key="gen_model"
                )
            else:
                ai_model = "Standard"
        
        with col3:
            if st.button("🔨 Generate Code", use_container_width=True):
                with st.spinner("Generating dashboard code with AI..."):
                    if self.ai and ai_model != "Standard":
                        # Generate using AI
                        mode = ai_model.lower()
                        ai_results = self.ai.generate_dashboard_code(
                            st.session_state.dashboard_config,
                            framework.lower(),
                            mode
                        )
                        
                        # Store results
                        if mode == "both":
                            st.session_state.generated_code = ai_results.get('best_practices', '')
                            st.session_state.ai_codes = ai_results
                        else:
                            key = f"{mode}_code"
                            st.session_state.generated_code = ai_results.get(key, '')
                    else:
                        # Fallback to standard generation
                        code = self.generate_code(framework)
                        st.session_state.generated_code = code
                    
                    st.success("Dashboard code generated successfully!")
        
        # Display generated code
        if st.session_state.generated_code:
            st.markdown("#### Generated Code")
            
            # Code display with syntax highlighting
            st.code(st.session_state.generated_code, language='python')
            
            # Download button
            st.download_button(
                label="📥 Download Code",
                data=st.session_state.generated_code,
                file_name=f"{st.session_state.dashboard_config.get('name', 'dashboard')}.py",
                mime="text/plain"
            )
            
            # Test run option
            if st.button("🚀 Test Dashboard"):
                self.test_generated_dashboard()
    
    def export_dashboard(self):
        """Export complete dashboard package"""
        st.markdown("### Export Dashboard Package")
        
        if not st.session_state.generated_code:
            st.warning("Please generate dashboard code first")
            return
        
        export_options = st.multiselect(
            "Select export components",
            ["Python Code", "Requirements.txt", "Sample Data", "Documentation", "Docker Config"],
            default=["Python Code", "Requirements.txt", "Sample Data"]
        )
        
        if st.button("📦 Create Package"):
            with st.spinner("Creating dashboard package..."):
                # Create package
                package_data = self.create_dashboard_package(export_options)
                
                # Download as zip
                st.download_button(
                    label="📥 Download Dashboard Package",
                    data=package_data,
                    file_name=f"{st.session_state.dashboard_config.get('name', 'dashboard')}_package.zip",
                    mime="application/zip"
                )
                
                st.success("Dashboard package created successfully!")
    
    def generate_code(self, framework):
        """Generate dashboard code based on framework and config"""
        config = st.session_state.dashboard_config
        
        if framework == "Streamlit":
            code = f'''"""
{config.get('name', 'KPI Dashboard')}
Generated on {datetime.now().strftime('%Y-%m-%d')}
Framework: Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="{config.get('name', 'KPI Dashboard')}",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("{config.get('name', 'KPI Dashboard')}")
st.markdown("---")

# Load data function
@st.cache_data
def load_data():
    # Load your data here
    # df = pd.read_excel('your_data.xlsx')
    # return df
    pass

# Main dashboard
def main():
    # Sidebar
    with st.sidebar:
        st.header("Filters")
        # Add filters based on configuration
        {self.generate_filter_code(config.get('kpi_fields', []))}
    
    # Main content
    data = load_data()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total KPIs", len(data) if data is not None else 0)
    with col2:
        st.metric("On Track", "0")
    with col3:
        st.metric("At Risk", "0")
    with col4:
        st.metric("Avg Performance", "0%")
    
    # Charts
    {self.generate_chart_code(config.get('chart_types', []))}
    
    # Data table
    st.subheader("KPI Details")
    if data is not None:
        st.dataframe(data, use_container_width=True)

if __name__ == "__main__":
    main()
'''
        else:
            code = f"# {framework} dashboard code generation not yet implemented"
        
        return code
    
    def generate_filter_code(self, fields):
        """Generate filter code based on fields"""
        filter_code = ""
        for field in fields:
            filter_code += f'''
        # {field} filter
        {field.lower()}_filter = st.selectbox("{field}", ["All"] + data['{field}'].unique().tolist())
'''
        return filter_code
    
    def generate_chart_code(self, chart_types):
        """Generate chart code based on types"""
        chart_code = ""
        
        if "Bar" in chart_types:
            chart_code += '''
    # Bar chart
    fig_bar = px.bar(data, x='category', y='value', title='KPI Performance')
    st.plotly_chart(fig_bar, use_container_width=True)
'''
        
        if "Line" in chart_types:
            chart_code += '''
    # Line chart  
    fig_line = px.line(data, x='date', y='value', title='Trend Analysis')
    st.plotly_chart(fig_line, use_container_width=True)
'''
        
        if "Pie" in chart_types:
            chart_code += '''
    # Pie chart
    fig_pie = px.pie(data, values='value', names='category', title='Distribution')
    st.plotly_chart(fig_pie, use_container_width=True)
'''
        
        return chart_code
    
    def create_dashboard_package(self, components):
        """Create a complete dashboard package"""
        import zipfile
        import io
        
        # Create zip file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add Python code
            if "Python Code" in components:
                zip_file.writestr(
                    'dashboard.py',
                    st.session_state.generated_code
                )
            
            # Add requirements.txt
            if "Requirements.txt" in components:
                requirements = """streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.0.0
openpyxl>=3.0.0
numpy>=1.24.0
"""
                zip_file.writestr('requirements.txt', requirements)
            
            # Add sample data
            if "Sample Data" in components:
                sample_df = self.generate_sample_data()
                csv_buffer = io.StringIO()
                sample_df.to_csv(csv_buffer, index=False)
                zip_file.writestr('sample_data.csv', csv_buffer.getvalue())
            
            # Add documentation
            if "Documentation" in components:
                doc = f"""# {st.session_state.dashboard_config.get('name', 'Dashboard')} Documentation

## Overview
Generated dashboard for KPI tracking and visualization.

## Installation
1. Install requirements: `pip install -r requirements.txt`
2. Run dashboard: `streamlit run dashboard.py`

## Configuration
- Framework: {st.session_state.dashboard_config.get('framework', 'Streamlit')}
- Update Frequency: {st.session_state.dashboard_config.get('update_frequency', 'Daily')}
- Theme: {st.session_state.dashboard_config.get('theme', 'Light')}

## Features
- {', '.join(st.session_state.dashboard_config.get('chart_types', []))} charts
- {', '.join(st.session_state.dashboard_config.get('kpi_fields', []))} tracking

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                zip_file.writestr('README.md', doc)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def test_generated_dashboard(self):
        """Test the generated dashboard code"""
        st.info("Testing generated dashboard...")
        
        # Save code to temporary file and run
        temp_file = "temp_dashboard.py"
        with open(temp_file, 'w') as f:
            f.write(st.session_state.generated_code)
        
        st.success(f"Dashboard code saved to {temp_file}")
        st.info("Run `streamlit run temp_dashboard.py` in terminal to test")
    
    def show_overview(self):
        """Show overview for Review mode"""
        if st.session_state.data is None:
            st.warning("Please upload data first")
            return
        
        df = st.session_state.data
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total KPIs", len(df))
        with col2:
            if 'status' in df.columns:
                on_track = len(df[df['status'] == 'G'])
                st.metric("On Track", on_track)
        with col3:
            if 'status' in df.columns:
                at_risk = len(df[df['status'] == 'R'])
                st.metric("At Risk", at_risk)
        with col4:
            if 'health_score' in df.columns:
                avg_health = df['health_score'].mean()
                st.metric("Avg Health", f"{avg_health:.0f}%")
        
        # Visualizations
        fig = self.viz_engine.create_dashboard_view(df)
        st.plotly_chart(fig, use_container_width=True)
    
    def show_analytics(self):
        """Show analytics for Review mode"""
        if st.session_state.data is None:
            st.warning("Please upload data first")
            return
        
        analysis_results = self.analytics.perform_comprehensive_analysis(st.session_state.data)
        
        # Display results
        for key, value in analysis_results.items():
            st.subheader(key.replace('_', ' ').title())
            if isinstance(value, pd.DataFrame):
                st.dataframe(value)
            elif isinstance(value, dict):
                st.json(value)
            else:
                st.write(value)
    
    def show_details(self):
        """Show detailed KPI table"""
        if st.session_state.data is None:
            st.warning("Please upload data first")
            return
        
        st.dataframe(
            st.session_state.data,
            use_container_width=True,
            hide_index=True
        )
    
    def show_reports(self):
        """Show reports section"""
        if st.session_state.data is None:
            st.warning("Please upload data first")
            return
        
        st.markdown("### Generate Reports")
        
        report_type = st.selectbox(
            "Select Report Type",
            ["Executive Summary", "Detailed Analysis", "Performance Report"]
        )
        
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                # Generate Excel report
                excel_buffer = self.excel_gen.generate_report(
                    st.session_state.data,
                    report_type=report_type.lower().replace(' ', '_')
                )
                
                st.download_button(
                    label="📥 Download Report",
                    data=excel_buffer,
                    file_name=f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    def generate_sample_data(self):
        """Generate sample KPI data"""
        np.random.seed(42)
        n = 30
        
        data = {
            'kpi_name': [f'KPI {i}' for i in range(1, n+1)],
            'project': np.random.choice(['Project A', 'Project B', 'Project C'], n),
            'owner': np.random.choice(['John', 'Sarah', 'Mike', 'Emily'], n),
            'status': np.random.choice(['G', 'Y', 'R'], n, p=[0.5, 0.3, 0.2]),
            'target_value': np.random.randint(100, 1000, n),
            'actual_value': np.random.randint(50, 1100, n),
            'health_score': np.random.randint(40, 100, n),
            'progress': np.random.randint(1, 6, n),
            'last_updated': pd.date_range(end=datetime.now(), periods=n, freq='D')
        }
        
        return pd.DataFrame(data)
    
    def _get_ai_status(self) -> str:
        """Get AI model availability status"""
        if not self.ai:
            return "🔴 AI Models: Not Available (Install packages and add API keys)"
        
        models = self.ai.get_available_models()
        status_parts = []
        
        if models['openai']:
            status_parts.append("🤖 OpenAI: Ready")
        else:
            status_parts.append("⚪ OpenAI: Not configured")
        
        if models['claude']:
            status_parts.append("🧠 Claude: Ready")
        else:
            status_parts.append("⚪ Claude: Not configured")
        
        return " | ".join(status_parts)
    
    def show_ai_comparison(self):
        """Show AI model comparison interface"""
        st.markdown("### AI Model Comparison")
        
        if not self.ai:
            st.warning("AI models not available. Please configure API keys.")
            return
        
        if st.session_state.data is None:
            st.warning("Please upload data first")
            return
        
        task = st.selectbox(
            "Select comparison task",
            ["Analysis", "Insight Generation", "Code Generation"]
        )
        
        if st.button("Compare Models"):
            with st.spinner("Running comparison..."):
                if task == "Analysis":
                    data_summary = self.ai._prepare_data_summary(st.session_state.data)
                    results = self.ai.compare_models("analysis", data_summary)
                elif task == "Insight Generation":
                    results = {
                        'task': 'Insight Generation',
                        'models': []
                    }
                    
                    # Get insights from both models
                    insights = self.ai.generate_insights(st.session_state.data)
                    
                    # Group by source
                    openai_insights = [i for i in insights if i.get('source') == 'openai']
                    claude_insights = [i for i in insights if i.get('source') == 'claude']
                    
                    if openai_insights:
                        results['models'].append({
                            'name': 'OpenAI',
                            'insights': openai_insights
                        })
                    
                    if claude_insights:
                        results['models'].append({
                            'name': 'Claude',
                            'insights': claude_insights
                        })
                else:
                    results = self.ai.generate_dashboard_code(
                        st.session_state.dashboard_config,
                        "streamlit",
                        "both"
                    )
                
                # Display comparison results
                st.markdown("#### Comparison Results")
                
                if 'models' in results:
                    for model_result in results['models']:
                        with st.expander(f"{model_result['name']} Results"):
                            if 'insights' in model_result:
                                for insight in model_result['insights']:
                                    st.write(f"• {insight.get('title', '')}: {insight.get('message', '')}")
                            else:
                                st.json(model_result)
                else:
                    # Code comparison
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### OpenAI Generated Code")
                        if 'openai_code' in results:
                            st.code(results['openai_code'][:500] + "...", language='python')
                    
                    with col2:
                        st.markdown("##### Claude Generated Code")
                        if 'claude_code' in results:
                            st.code(results['claude_code'][:500] + "...", language='python')

# Main execution
if __name__ == "__main__":
    dashboard = EnhancedKPIDashboard()
    dashboard.run()