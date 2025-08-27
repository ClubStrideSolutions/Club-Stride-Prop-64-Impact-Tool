"""
KPI Dashboard System with AI Integration
=========================================
Streamlined dashboard for KPI tracking and analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from pathlib import Path

# Add modules to path
import sys
sys.path.append(str(Path(__file__).parent / 'modules'))

# Import core modules
from modules.excel_generator import ExcelGenerator
from modules.analytics_engine import AnalyticsEngine
from modules.visualization_engine import VisualizationEngine
from modules.data_validator import DataValidator
from modules.ai_orchestrator import AIOrchestrator

# Page configuration
st.set_page_config(
    page_title="KPI Dashboard System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C57FA;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f0f0;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)

class KPIDashboard:
    """Simplified KPI Dashboard Application"""
    
    def __init__(self):
        self.initialize_session_state()
        self.excel_gen = ExcelGenerator()
        self.analytics = AnalyticsEngine()
        self.visualizer = VisualizationEngine()
        self.validator = DataValidator()
        self.ai = AIOrchestrator()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'kpi_data' not in st.session_state:
            st.session_state.kpi_data = pd.DataFrame()
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
    
    def load_sample_data(self):
        """Load sample KPI data"""
        sample_data = {
            'kpi_name': [
                'User Acquisition Rate',
                'Customer Retention',
                'Revenue Growth',
                'Operational Efficiency',
                'Product Quality Score',
                'Customer Satisfaction',
                'Market Share',
                'Employee Productivity'
            ],
            'current_value': [85, 92, 78, 88, 95, 87, 72, 90],
            'target_value': [90, 95, 85, 90, 98, 90, 80, 92],
            'status': ['On Track', 'Achieved', 'At Risk', 'On Track', 
                      'Achieved', 'On Track', 'At Risk', 'Achieved'],
            'owner': ['Marketing', 'Sales', 'Finance', 'Operations',
                     'Quality', 'Support', 'Marketing', 'HR'],
            'last_updated': [datetime.now() - timedelta(days=i) for i in range(8)]
        }
        return pd.DataFrame(sample_data)
    
    def render_header(self):
        """Render application header"""
        st.markdown('<h1 class="main-header">📊 KPI Dashboard System</h1>', 
                   unsafe_allow_html=True)
        
        # Show key metrics if data is loaded
        if st.session_state.data_loaded and not st.session_state.kpi_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            df = st.session_state.kpi_data
            
            with col1:
                total_kpis = len(df)
                st.metric("Total KPIs", total_kpis, "+3 this month")
            
            with col2:
                if 'status' in df.columns:
                    achieved = len(df[df['status'] == 'Achieved'])
                    st.metric("Achieved", achieved, f"{achieved/total_kpis*100:.0f}%")
                else:
                    st.metric("Achieved", "N/A")
            
            with col3:
                if 'current_value' in df.columns and 'target_value' in df.columns:
                    avg_performance = (df['current_value'] / df['target_value'] * 100).mean()
                    st.metric("Avg Performance", f"{avg_performance:.1f}%", "↑ 2.3%")
                else:
                    st.metric("Avg Performance", "N/A")
            
            with col4:
                if 'health_score' in df.columns:
                    avg_health = df['health_score'].mean()
                    st.metric("Health Score", f"{avg_health:.0f}/100", "↑ 5")
                else:
                    st.metric("Health Score", "Calculate")
    
    def render_sidebar(self):
        """Render sidebar with data management options"""
        with st.sidebar:
            st.title("📁 Data Management")
            
            # Data source selection
            data_source = st.radio(
                "Select Data Source:",
                ["Upload Excel", "Load Sample Data", "Manual Entry"]
            )
            
            if data_source == "Upload Excel":
                uploaded_file = st.file_uploader(
                    "Choose Excel file",
                    type=['xlsx', 'xls'],
                    help="Upload your KPI Excel file"
                )
                
                if uploaded_file:
                    try:
                        df = pd.read_excel(uploaded_file)
                        
                        # Validate and process data
                        df = self.validator.validate_dataframe(df)
                        
                        # Add analytics
                        df = self.analytics.enrich_with_analytics(df)
                        
                        st.session_state.kpi_data = df
                        st.session_state.data_loaded = True
                        st.success(f"✅ Loaded {len(df)} KPIs")
                    except Exception as e:
                        st.error(f"Error loading file: {str(e)}")
            
            elif data_source == "Load Sample Data":
                if st.button("Load Sample KPIs", type="primary"):
                    df = self.load_sample_data()
                    
                    # Add analytics
                    df = self.analytics.enrich_with_analytics(df)
                    
                    st.session_state.kpi_data = df
                    st.session_state.data_loaded = True
                    st.success("✅ Sample data loaded!")
            
            else:  # Manual Entry
                with st.form("manual_entry"):
                    st.subheader("Add New KPI")
                    kpi_name = st.text_input("KPI Name")
                    current_value = st.number_input("Current Value", min_value=0.0)
                    target_value = st.number_input("Target Value", min_value=0.0)
                    status = st.selectbox("Status", 
                                         ["On Track", "At Risk", "Achieved", "Not Started"])
                    owner = st.text_input("Owner")
                    
                    if st.form_submit_button("Add KPI"):
                        new_kpi = pd.DataFrame([{
                            'kpi_name': kpi_name,
                            'current_value': current_value,
                            'target_value': target_value,
                            'status': status,
                            'owner': owner,
                            'last_updated': datetime.now()
                        }])
                        
                        if st.session_state.data_loaded:
                            st.session_state.kpi_data = pd.concat(
                                [st.session_state.kpi_data, new_kpi], 
                                ignore_index=True
                            )
                        else:
                            st.session_state.kpi_data = new_kpi
                            st.session_state.data_loaded = True
                        
                        st.success(f"✅ Added KPI: {kpi_name}")
            
            # Export options
            if st.session_state.data_loaded:
                st.divider()
                st.subheader("📥 Export Options")
                
                if st.button("Generate Excel Report", type="secondary"):
                    excel_file = self.excel_gen.generate_dashboard(
                        st.session_state.kpi_data,
                        "KPI_Dashboard.xlsx"
                    )
                    st.success("✅ Excel report generated!")
                    st.download_button(
                        label="Download Excel",
                        data=open(excel_file, 'rb').read(),
                        file_name="KPI_Dashboard.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    def render_dashboard(self):
        """Render main dashboard content"""
        if not st.session_state.data_loaded:
            st.info("👈 Please load data using the sidebar options")
            return
        
        df = st.session_state.kpi_data
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "📈 Analytics", 
            "🎯 Performance",
            "🤖 AI Insights",
            "📋 Data Table"
        ])
        
        with tab1:
            self.render_overview(df)
        
        with tab2:
            self.render_analytics(df)
        
        with tab3:
            self.render_performance(df)
        
        with tab4:
            self.render_ai_insights(df)
        
        with tab5:
            self.render_data_table(df)
    
    def render_overview(self, df):
        """Render overview tab"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            if 'status' in df.columns:
                fig = px.pie(df, names='status', title="KPI Status Distribution")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance by owner
            if 'owner' in df.columns and 'current_value' in df.columns:
                owner_perf = df.groupby('owner')['current_value'].mean().reset_index()
                fig = px.bar(owner_perf, x='owner', y='current_value', 
                           title="Average Performance by Owner")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Health score distribution
        if 'health_score' in df.columns:
            st.subheader("Health Score Distribution")
            fig = self.visualizer.create_health_distribution(df)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_analytics(self, df):
        """Render analytics tab"""
        st.subheader("📊 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk analysis
            st.markdown("### Risk Analysis")
            risk_data = self.analytics.calculate_risk_scores(df)
            for risk in risk_data[:5]:
                st.warning(f"⚠️ {risk['kpi']}: {risk['risk_level']} - {risk['reason']}")
        
        with col2:
            # Predictions
            st.markdown("### Predictions")
            predictions = self.analytics.generate_predictions(df)
            for pred in predictions[:5]:
                st.info(f"📈 {pred['kpi']}: {pred['prediction']}")
        
        # Correlation matrix
        if len(df.select_dtypes(include=['float64', 'int64']).columns) > 1:
            st.subheader("Correlation Analysis")
            fig = self.visualizer.create_correlation_heatmap(df)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_performance(self, df):
        """Render performance tab"""
        st.subheader("🎯 Performance Tracking")
        
        # Performance matrix
        if 'owner' in df.columns and 'status' in df.columns:
            fig = self.visualizer.create_performance_matrix(df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline view
        if 'last_updated' in df.columns:
            st.subheader("📅 Timeline View")
            fig = self.visualizer.create_timeline_chart(df)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_insights(self, df):
        """Render AI insights tab"""
        st.subheader("🤖 AI-Powered Insights")
        
        # Check if AI is available
        available_models = self.ai.get_available_models()
        
        if not available_models['openai'] and not available_models['claude']:
            st.warning("⚠️ No AI models configured. Please set up API keys in .env file:")
            st.code("""
# Create a .env file with:
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
            """)
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # AI Analysis button
            if st.button("🔍 Generate AI Analysis", type="primary"):
                with st.spinner("Analyzing KPI data..."):
                    try:
                        # Get AI insights
                        insights = self.ai.generate_insights(df, 
                            context="Analyze KPI performance and provide recommendations")
                        
                        # Display insights
                        for insight in insights:
                            priority_color = {
                                'high': '🔴',
                                'medium': '🟡', 
                                'low': '🟢'
                            }.get(insight.get('priority', '').lower(), '⚪')
                            
                            st.markdown(f"""
                            ### {priority_color} {insight.get('title', 'Insight')}
                            {insight.get('message', '')}
                            
                            **Recommendations:** {', '.join(insight.get('recommendations', []))}
                            
                            ---
                            """)
                    except Exception as e:
                        st.error(f"Error generating insights: {str(e)}")
        
        with col2:
            st.info(f"""
            **Available AI Models:**
            - OpenAI GPT-4: {'✅' if available_models['openai'] else '❌'}
            - Claude 3.5 Sonnet: {'✅' if available_models['claude'] else '❌'}
            """)
    
    def render_data_table(self, df):
        """Render data table tab"""
        st.subheader("📋 KPI Data Table")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'status' in df.columns:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=df['status'].unique(),
                    default=df['status'].unique()
                )
                df = df[df['status'].isin(status_filter)]
        
        with col2:
            if 'owner' in df.columns:
                owner_filter = st.multiselect(
                    "Filter by Owner",
                    options=df['owner'].unique(),
                    default=df['owner'].unique()
                )
                df = df[df['owner'].isin(owner_filter)]
        
        with col3:
            search = st.text_input("🔍 Search KPIs")
            if search:
                df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
        
        # Display editable dataframe
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="kpi_editor"
        )
        
        # Save changes
        if st.button("💾 Save Changes"):
            st.session_state.kpi_data = edited_df
            st.success("✅ Changes saved!")
    
    def run(self):
        """Main application entry point"""
        self.render_header()
        self.render_sidebar()
        self.render_dashboard()

# Run the application
if __name__ == "__main__":
    app = KPIDashboard()
    app.run()