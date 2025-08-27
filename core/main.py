"""
Enhanced KPI Dashboard System - Main Application
================================================
A comprehensive KPI tracking and analytics system that processes documents,
generates Excel dashboards, and provides AI-powered insights.

Features:
- Document parsing (SOW, Requirements, Word docs)
- Excel generation with advanced formatting
- AI-powered insights and predictions
- Real-time data validation
- Interactive visualizations
- Multi-view dashboards
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

# Import custom modules
from document_processor import DocumentProcessor
from excel_generator import ExcelGenerator
from analytics_engine import AnalyticsEngine
from visualization_engine import VisualizationEngine
from data_validator import DataValidator
from config import Config
from ui_components import UIComponents

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown(Config.CUSTOM_CSS, unsafe_allow_html=True)

class KPIDashboardApp:
    """Main application class for KPI Dashboard System"""
    
    def __init__(self):
        self.initialize_session_state()
        self.doc_processor = DocumentProcessor()
        self.excel_generator = ExcelGenerator()
        self.analytics = AnalyticsEngine()
        self.visualizer = VisualizationEngine()
        self.validator = DataValidator()
        self.ui = UIComponents()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'kpi_data' not in st.session_state:
            st.session_state.kpi_data = pd.DataFrame()
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'data_modified' not in st.session_state:
            st.session_state.data_modified = False
        if 'last_saved' not in st.session_state:
            st.session_state.last_saved = None
        if 'change_log' not in st.session_state:
            st.session_state.change_log = []
        if 'insights_cache' not in st.session_state:
            st.session_state.insights_cache = {}
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = Config.DEFAULT_PREFERENCES
    
    def run(self):
        """Main application entry point"""
        self.render_header()
        self.render_sidebar()
        
        if st.session_state.data_loaded:
            self.render_main_dashboard()
        else:
            self.render_welcome_screen()
    
    def render_header(self):
        """Render application header"""
        # Use Streamlit containers instead of raw HTML
        with st.container():
            st.markdown(
                """
                <style>
                .header-container {
                    background: linear-gradient(135deg, #2C57FA 0%, #FA962C 100%);
                    padding: 2rem;
                    border-radius: 12px;
                    margin-bottom: 2rem;
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Create a colored container using columns
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.title(Config.APP_TITLE)
                st.subheader(Config.APP_SUBTITLE)
                
                # Display badges using native Streamlit components
                if st.session_state.data_loaded:
                    badge_cols = st.columns(3)
                    total_kpis = len(st.session_state.kpi_data)
                    
                    with badge_cols[0]:
                        st.info(f"📊 {total_kpis} KPIs")
                    
                    if st.session_state.data_modified:
                        with badge_cols[1]:
                            st.warning("⚠️ Unsaved Changes")
                    
                    if st.session_state.last_saved:
                        time_diff = datetime.now() - st.session_state.last_saved
                        if time_diff.total_seconds() < 300:
                            with badge_cols[2]:
                                st.success("✅ Recently Saved")
    
    def get_status_badges(self):
        """Generate status badges for header - DEPRECATED"""
        # This method is now integrated into render_header
        return ""
    
    def render_sidebar(self):
        """Render sidebar controls"""
        with st.sidebar:
            st.markdown("## 🎛️ Control Panel")
            
            # Data Input Section
            self.render_data_input_section()
            
            # Filters Section (if data is loaded)
            if st.session_state.data_loaded:
                self.render_filters_section()
                self.render_export_section()
                self.render_settings_section()
    
    def render_data_input_section(self):
        """Render data input controls"""
        st.markdown("### 📥 Data Input")
        
        input_method = st.selectbox(
            "Select input method:",
            ["Upload Excel File", "Process Document", "Paste Data", "Load Sample Data"],
            key="input_method"
        )
        
        if input_method == "Upload Excel File":
            self.handle_excel_upload()
        elif input_method == "Process Document":
            self.handle_document_processing()
        elif input_method == "Paste Data":
            self.handle_paste_data()
        elif input_method == "Load Sample Data":
            self.handle_sample_data()
    
    def handle_excel_upload(self):
        """Handle Excel file upload"""
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type=['xlsx', 'xlsm', 'xls'],
            help="Upload your KPI Dashboard Excel file"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Process File", type="primary", use_container_width=True):
                    with st.spinner("Processing Excel file..."):
                        try:
                            # Process the Excel file
                            data = self.doc_processor.process_excel(uploaded_file)
                            
                            # Validate data
                            validated_data = self.validator.validate_dataframe(data)
                            
                            # Calculate analytics
                            validated_data = self.analytics.enrich_with_analytics(validated_data)
                            
                            # Store in session
                            st.session_state.kpi_data = validated_data
                            st.session_state.data_loaded = True
                            st.session_state.last_saved = datetime.now()
                            
                            # Log the action
                            self.log_action(f"Loaded {len(validated_data)} KPIs from Excel")
                            
                            st.success(f"✅ Successfully loaded {len(validated_data)} KPIs!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error processing file: {str(e)}")
            
            with col2:
                if st.button("👁️ Preview Structure", use_container_width=True):
                    try:
                        structure = self.doc_processor.preview_excel_structure(uploaded_file)
                        st.json(structure)
                    except Exception as e:
                        st.error(f"Error previewing file: {str(e)}")
    
    def handle_document_processing(self):
        """Handle document processing (SOW, Requirements, etc.)"""
        st.markdown("#### 📄 Document Processing")
        
        doc_type = st.selectbox(
            "Document type:",
            ["Statement of Work (SOW)", "Requirements Document", "Project Charter", "Custom Text"]
        )
        
        # File upload or text input
        input_method = st.radio("Input method:", ["Upload File", "Paste Text"])
        
        if input_method == "Upload File":
            uploaded_doc = st.file_uploader(
                f"Upload {doc_type}",
                type=['pdf', 'docx', 'txt', 'md'],
                help="Upload your document for KPI extraction"
            )
            
            if uploaded_doc:
                if st.button("🔍 Extract KPIs", type="primary", use_container_width=True):
                    with st.spinner("Analyzing document..."):
                        try:
                            # Process document based on type
                            if doc_type == "Statement of Work (SOW)":
                                data = self.doc_processor.process_sow(uploaded_doc)
                            elif doc_type == "Requirements Document":
                                data = self.doc_processor.process_requirements(uploaded_doc)
                            elif doc_type == "Project Charter":
                                data = self.doc_processor.process_charter(uploaded_doc)
                            else:
                                data = self.doc_processor.process_custom_document(uploaded_doc)
                            
                            # Enrich and validate
                            data = self.validator.validate_dataframe(data)
                            data = self.analytics.enrich_with_analytics(data)
                            
                            # Store in session
                            st.session_state.kpi_data = data
                            st.session_state.data_loaded = True
                            st.session_state.last_saved = datetime.now()
                            
                            self.log_action(f"Extracted {len(data)} KPIs from {doc_type}")
                            
                            st.success(f"✅ Extracted {len(data)} KPIs from document!")
                            
                            # Show extraction summary
                            with st.expander("📋 Extraction Summary", expanded=True):
                                self.show_extraction_summary(data)
                            
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error processing document: {str(e)}")
        
        else:  # Paste Text
            text_input = st.text_area(
                f"Paste {doc_type} content:",
                height=300,
                placeholder="Paste your document content here..."
            )
            
            if text_input and st.button("🔍 Extract KPIs", type="primary", use_container_width=True):
                with st.spinner("Analyzing text..."):
                    try:
                        # Process text based on type
                        if doc_type == "Statement of Work (SOW)":
                            data = self.doc_processor.process_sow_text(text_input)
                        elif doc_type == "Requirements Document":
                            data = self.doc_processor.process_requirements_text(text_input)
                        else:
                            data = self.doc_processor.process_text(text_input)
                        
                        # Enrich and validate
                        data = self.validator.validate_dataframe(data)
                        data = self.analytics.enrich_with_analytics(data)
                        
                        # Store in session
                        st.session_state.kpi_data = data
                        st.session_state.data_loaded = True
                        st.session_state.last_saved = datetime.now()
                        
                        self.log_action(f"Extracted {len(data)} KPIs from pasted text")
                        
                        st.success(f"✅ Extracted {len(data)} KPIs!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error processing text: {str(e)}")
    
    def handle_paste_data(self):
        """Handle paste data input"""
        st.markdown("#### 📋 Paste Data")
        
        data_format = st.selectbox(
            "Data format:",
            ["CSV", "Tab-separated", "JSON"]
        )
        
        pasted_data = st.text_area(
            "Paste your data:",
            height=300,
            placeholder="Paste your KPI data here..."
        )
        
        if pasted_data and st.button("📊 Process Data", type="primary", use_container_width=True):
            with st.spinner("Processing data..."):
                try:
                    # Parse based on format
                    if data_format == "CSV":
                        import io
                        data = pd.read_csv(io.StringIO(pasted_data))
                    elif data_format == "Tab-separated":
                        import io
                        data = pd.read_csv(io.StringIO(pasted_data), sep='\t')
                    elif data_format == "JSON":
                        import json
                        data = pd.DataFrame(json.loads(pasted_data))
                    
                    # Validate and enrich
                    data = self.validator.validate_dataframe(data)
                    data = self.analytics.enrich_with_analytics(data)
                    
                    # Store in session
                    st.session_state.kpi_data = data
                    st.session_state.data_loaded = True
                    st.session_state.last_saved = datetime.now()
                    
                    self.log_action(f"Loaded {len(data)} KPIs from pasted data")
                    
                    st.success(f"✅ Loaded {len(data)} KPIs!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing data: {str(e)}")
    
    def handle_sample_data(self):
        """Load sample data for demonstration"""
        st.markdown("#### 🎲 Sample Data")
        
        sample_type = st.selectbox(
            "Select sample dataset:",
            ["Youth Health Program", "Digital Transformation", "Sustainability Initiative", "Custom KPIs"]
        )
        
        if st.button("📊 Load Sample Data", type="primary", use_container_width=True):
            with st.spinner("Loading sample data..."):
                try:
                    # Generate sample data based on type
                    data = self.doc_processor.generate_sample_data(sample_type)
                    
                    # Validate and enrich
                    data = self.validator.validate_dataframe(data)
                    data = self.analytics.enrich_with_analytics(data)
                    
                    # Store in session
                    st.session_state.kpi_data = data
                    st.session_state.data_loaded = True
                    st.session_state.last_saved = datetime.now()
                    
                    self.log_action(f"Loaded {len(data)} sample KPIs")
                    
                    st.success(f"✅ Loaded {len(data)} sample KPIs!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")
    
    def render_filters_section(self):
        """Render filters section"""
        st.markdown("---")
        st.markdown("### 🔍 Filters")
        
        data = st.session_state.kpi_data
        
        # Project filter
        projects = st.multiselect(
            "Projects",
            options=data['project'].unique() if 'project' in data.columns else [],
            default=data['project'].unique() if 'project' in data.columns else [],
            key="filter_projects"
        )
        
        # Status filter
        status_options = data['status'].unique() if 'status' in data.columns else ['G', 'Y', 'R']
        status_filter = st.multiselect(
            "Status",
            options=status_options,
            default=status_options,
            format_func=lambda x: Config.STATUS_LABELS.get(x, x),
            key="filter_status"
        )
        
        # Owner filter
        if 'owner' in data.columns:
            owners = st.multiselect(
                "Owners",
                options=data['owner'].unique(),
                default=data['owner'].unique(),
                key="filter_owners"
            )
        else:
            owners = []
        
        # Date range filter
        if 'last_updated' in data.columns:
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                start_date = st.date_input(
                    "From",
                    value=data['last_updated'].min() if not data.empty else datetime.now() - timedelta(days=30),
                    key="filter_start_date"
                )
            with date_col2:
                end_date = st.date_input(
                    "To",
                    value=data['last_updated'].max() if not data.empty else datetime.now(),
                    key="filter_end_date"
                )
        
        # Apply filters button
        if st.button("🔄 Apply Filters", use_container_width=True):
            st.rerun()
    
    def render_export_section(self):
        """Render export section"""
        st.markdown("---")
        st.markdown("### 💾 Export & Save")
        
        # Show save status
        if st.session_state.data_modified:
            st.warning("⚠️ You have unsaved changes")
        
        if st.session_state.last_saved:
            time_diff = datetime.now() - st.session_state.last_saved
            if time_diff.total_seconds() < 60:
                st.success(f"✅ Saved {int(time_diff.total_seconds())} seconds ago")
            elif time_diff.total_seconds() < 3600:
                st.info(f"💾 Last saved {int(time_diff.total_seconds()/60)} minutes ago")
            else:
                st.warning(f"⏰ Last saved {int(time_diff.total_seconds()/3600)} hours ago")
        
        # Export options
        export_format = st.selectbox(
            "Export format:",
            ["Excel (Advanced)", "Excel (Simple)", "CSV", "JSON", "PDF Report"],
            key="export_format"
        )
        
        if st.button("📥 Generate Export", type="primary", use_container_width=True):
            with st.spinner(f"Generating {export_format}..."):
                try:
                    if export_format == "Excel (Advanced)":
                        file_data = self.excel_generator.generate_advanced_excel(st.session_state.kpi_data)
                        file_name = f"kpi_dashboard_advanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    
                    elif export_format == "Excel (Simple)":
                        file_data = self.excel_generator.generate_simple_excel(st.session_state.kpi_data)
                        file_name = f"kpi_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    
                    elif export_format == "CSV":
                        file_data = st.session_state.kpi_data.to_csv(index=False)
                        file_name = f"kpi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                        mime_type = "text/csv"
                    
                    elif export_format == "JSON":
                        file_data = st.session_state.kpi_data.to_json(orient='records', indent=2)
                        file_name = f"kpi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        mime_type = "application/json"
                    
                    elif export_format == "PDF Report":
                        # This would require additional PDF generation logic
                        st.info("PDF generation coming soon!")
                        return
                    
                    # Create download button
                    st.download_button(
                        label=f"⬇️ Download {export_format}",
                        data=file_data,
                        file_name=file_name,
                        mime=mime_type,
                        use_container_width=True
                    )
                    
                    # Mark as saved
                    st.session_state.data_modified = False
                    st.session_state.last_saved = datetime.now()
                    
                    self.log_action(f"Exported data as {export_format}")
                    
                    st.success(f"✅ {export_format} ready for download!")
                    
                except Exception as e:
                    st.error(f"Export error: {str(e)}")
        
        # Quick save button
        if st.button("💾 Quick Save", use_container_width=True):
            st.session_state.last_saved = datetime.now()
            st.session_state.data_modified = False
            self.log_action("Quick save performed")
            st.success("✅ Changes saved to session!")
    
    def render_settings_section(self):
        """Render settings section"""
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # Theme selection
        theme = st.selectbox(
            "Theme:",
            ["Light", "Dark", "Auto"],
            index=["Light", "Dark", "Auto"].index(st.session_state.user_preferences.get('theme', 'Light')),
            key="settings_theme"
        )
        
        # Auto-save toggle
        auto_save = st.checkbox(
            "Enable auto-save",
            value=st.session_state.user_preferences.get('auto_save', False),
            key="settings_auto_save"
        )
        
        # Notification settings
        notifications = st.checkbox(
            "Enable notifications",
            value=st.session_state.user_preferences.get('notifications', True),
            key="settings_notifications"
        )
        
        # Advanced analytics toggle
        advanced_analytics = st.checkbox(
            "Show advanced analytics",
            value=st.session_state.user_preferences.get('advanced_analytics', True),
            key="settings_advanced"
        )
        
        if st.button("💾 Save Settings", use_container_width=True):
            st.session_state.user_preferences = {
                'theme': theme,
                'auto_save': auto_save,
                'notifications': notifications,
                'advanced_analytics': advanced_analytics
            }
            self.log_action("Settings updated")
            st.success("✅ Settings saved!")
    
    def render_main_dashboard(self):
        """Render main dashboard content"""
        # Get filtered data
        filtered_data = self.get_filtered_data()
        
        if filtered_data.empty:
            st.warning("No data matches the selected filters. Please adjust your filters.")
            return
        
        # Create tabs for different views
        tabs = st.tabs([
            "📊 Executive Dashboard",
            "📈 Analytics & Insights",
            "📋 KPI Details",
            "✏️ Data Editor",
            "🎯 Performance Matrix",
            "🚧 Risk Analysis",
            "🏆 Success Stories",
            "📑 Reports"
        ])
        
        with tabs[0]:
            self.render_executive_dashboard(filtered_data)
        
        with tabs[1]:
            self.render_analytics_dashboard(filtered_data)
        
        with tabs[2]:
            self.render_kpi_details(filtered_data)
        
        with tabs[3]:
            self.render_data_editor(filtered_data)
        
        with tabs[4]:
            self.render_performance_matrix(filtered_data)
        
        with tabs[5]:
            self.render_risk_analysis(filtered_data)
        
        with tabs[6]:
            self.render_success_stories(filtered_data)
        
        with tabs[7]:
            self.render_reports(filtered_data)
    
    def render_executive_dashboard(self, data):
        """Render executive dashboard"""
        st.markdown("## 📊 Executive Dashboard")
        
        # Key metrics row
        metrics = self.analytics.calculate_key_metrics(data)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total KPIs",
                metrics['total_kpis'],
                delta=metrics.get('kpi_change', 0)
            )
        
        with col2:
            st.metric(
                "On Track",
                metrics['on_track'],
                delta=f"{metrics['on_track_percentage']:.0f}%",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                "At Risk",
                metrics['at_risk'],
                delta=f"{metrics['at_risk_percentage']:.0f}%",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                "Avg Health",
                f"{metrics['avg_health']:.0f}%",
                delta=metrics.get('health_change', '0%')
            )
        
        with col5:
            st.metric(
                "Avg Progress",
                f"{metrics['avg_progress']:.1f}/5",
                delta=metrics.get('progress_change', '0')
            )
        
        # AI Insights
        st.markdown("---")
        insights = self.analytics.generate_insights(data)
        
        if insights:
            st.markdown("### 🧠 AI-Powered Insights")
            
            # Display top insights
            for insight in insights[:3]:
                self.render_insight_card(insight)
        
        # Visualizations
        st.markdown("---")
        st.markdown("### 📈 Key Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Health distribution chart
            health_chart = self.visualizer.create_health_distribution_chart(data)
            st.plotly_chart(health_chart, use_container_width=True)
        
        with col2:
            # Status breakdown chart
            status_chart = self.visualizer.create_status_breakdown_chart(data)
            st.plotly_chart(status_chart, use_container_width=True)
        
        # Project performance
        st.markdown("---")
        st.markdown("### 🎯 Project Performance")
        
        project_chart = self.visualizer.create_project_performance_chart(data)
        st.plotly_chart(project_chart, use_container_width=True)
        
        # Recent activity
        st.markdown("---")
        st.markdown("### 🔄 Recent Activity")
        
        recent_data = data.nlargest(5, 'last_updated') if 'last_updated' in data.columns else data.head(5)
        self.render_activity_feed(recent_data)
    
    def render_analytics_dashboard(self, data):
        """Render analytics dashboard"""
        st.markdown("## 📈 Analytics & Insights")
        
        # Predictive analytics
        st.markdown("### 🔮 Predictive Analytics")
        
        predictions = self.analytics.generate_predictions(data)
        
        if predictions:
            for project, pred in predictions.items():
                with st.expander(f"📊 {project}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Current Completion", f"{pred['current_completion']:.0f}%")
                    
                    with col2:
                        st.metric("Est. Days to Complete", f"{pred['estimated_days']:.0f}")
                    
                    with col3:
                        st.metric("Confidence Level", f"{pred['confidence']:.0f}%")
                    
                    # Show completion timeline
                    timeline_chart = self.visualizer.create_completion_timeline(pred)
                    st.plotly_chart(timeline_chart, use_container_width=True)
        
        # Correlation analysis
        st.markdown("---")
        st.markdown("### 🔗 Correlation Analysis")
        
        correlation_chart = self.visualizer.create_correlation_heatmap(data)
        st.plotly_chart(correlation_chart, use_container_width=True)
        
        # Trend analysis
        st.markdown("---")
        st.markdown("### 📊 Trend Analysis")
        
        trend_chart = self.visualizer.create_trend_analysis_chart(data)
        st.plotly_chart(trend_chart, use_container_width=True)
        
        # Statistical summary
        st.markdown("---")
        st.markdown("### 📋 Statistical Summary")
        
        summary_stats = self.analytics.generate_statistical_summary(data)
        st.dataframe(summary_stats, use_container_width=True)
    
    def render_kpi_details(self, data):
        """Render detailed KPI view"""
        st.markdown("## 📋 KPI Details")
        
        # Search and filter
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_term = st.text_input(
                "🔍 Search KPIs",
                placeholder="Search by name, project, owner...",
                key="kpi_search"
            )
        
        with col2:
            sort_by = st.selectbox(
                "Sort by:",
                ["Health Score", "Progress", "Last Updated", "Project", "Status"],
                key="kpi_sort"
            )
        
        with col3:
            sort_order = st.selectbox(
                "Order:",
                ["Descending", "Ascending"],
                key="kpi_order"
            )
        
        # Apply search and sort
        display_data = self.apply_search_and_sort(data, search_term, sort_by, sort_order)
        
        # Display KPIs in expandable cards
        for idx, row in display_data.iterrows():
            self.render_kpi_card(row, idx)
    
    def render_data_editor(self, data):
        """Render data editor interface"""
        st.markdown("## ✏️ Data Editor")
        
        st.info("""
        📝 **Instructions:**
        - Edit data directly in the table below
        - Click 'Apply Changes' to save your modifications
        - Use 'Add Row' to create new KPIs
        - Changes are validated automatically
        """)
        
        # Create editable dataframe
        edited_data = st.data_editor(
            data,
            use_container_width=True,
            num_rows="dynamic",
            column_config=Config.COLUMN_CONFIG,
            key="data_editor"
        )
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Apply Changes", type="primary", use_container_width=True):
                try:
                    # Validate changes
                    validated_data = self.validator.validate_dataframe(edited_data)
                    
                    # Recalculate analytics
                    validated_data = self.analytics.enrich_with_analytics(validated_data)
                    
                    # Update session state
                    st.session_state.kpi_data = validated_data
                    st.session_state.data_modified = True
                    
                    self.log_action(f"Applied changes to {len(validated_data)} KPIs")
                    
                    st.success("✅ Changes applied successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error applying changes: {str(e)}")
        
        with col2:
            if st.button("➕ Add Row", use_container_width=True):
                # Add new empty row
                new_row = self.create_empty_kpi_row()
                st.session_state.kpi_data = pd.concat([st.session_state.kpi_data, new_row], ignore_index=True)
                st.session_state.data_modified = True
                self.log_action("Added new KPI row")
                st.rerun()
        
        with col3:
            if st.button("🔄 Refresh Analytics", use_container_width=True):
                # Recalculate all analytics
                st.session_state.kpi_data = self.analytics.enrich_with_analytics(st.session_state.kpi_data)
                st.session_state.data_modified = True
                self.log_action("Refreshed analytics")
                st.success("✅ Analytics refreshed!")
                st.rerun()
        
        with col4:
            if st.button("↩️ Revert Changes", use_container_width=True):
                if st.session_state.data_modified:
                    st.session_state.data_modified = False
                    self.log_action("Reverted changes")
                    st.info("Changes reverted")
                    st.rerun()
    
    def render_performance_matrix(self, data):
        """Render performance matrix view"""
        st.markdown("## 🎯 Performance Matrix")
        
        # Create performance matrix visualization
        matrix_chart = self.visualizer.create_performance_matrix(data)
        st.plotly_chart(matrix_chart, use_container_width=True)
        
        # Performance rankings
        st.markdown("### 🏆 Performance Rankings")
        
        rankings = self.analytics.calculate_performance_rankings(data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Top Performers")
            for item in rankings['top_performers'][:5]:
                st.success(f"🥇 {item['name']}: {item['score']:.0f}%")
        
        with col2:
            st.markdown("#### Need Improvement")
            for item in rankings['need_improvement'][:5]:
                st.warning(f"⚠️ {item['name']}: {item['score']:.0f}%")
        
        with col3:
            st.markdown("#### Critical")
            for item in rankings['critical'][:5]:
                st.error(f"🚨 {item['name']}: {item['score']:.0f}%")
    
    def render_risk_analysis(self, data):
        """Render risk analysis view"""
        st.markdown("## 🚧 Risk Analysis")
        
        # Calculate risk scores
        risk_data = self.analytics.calculate_risk_scores(data)
        
        # Risk distribution chart
        risk_chart = self.visualizer.create_risk_distribution_chart(risk_data)
        st.plotly_chart(risk_chart, use_container_width=True)
        
        # Risk matrix
        st.markdown("### 🎯 Risk Matrix")
        
        risk_matrix = self.visualizer.create_risk_matrix(risk_data)
        st.plotly_chart(risk_matrix, use_container_width=True)
        
        # Risk mitigation recommendations
        st.markdown("### 💡 Risk Mitigation Recommendations")
        
        recommendations = self.analytics.generate_risk_recommendations(risk_data)
        
        for rec in recommendations:
            with st.expander(f"🔧 {rec['title']}", expanded=False):
                st.write(rec['description'])
                st.write(f"**Priority:** {rec['priority']}")
                st.write(f"**Impact:** {rec['impact']}")
                
                if 'actions' in rec:
                    st.write("**Recommended Actions:**")
                    for action in rec['actions']:
                        st.write(f"• {action}")
    
    def render_success_stories(self, data):
        """Render success stories view"""
        st.markdown("## 🏆 Success Stories")
        
        # Filter for successful KPIs
        success_data = data[
            (data['status'] == 'G') & 
            (data['health_score'] > 80) if 'health_score' in data.columns else (data['status'] == 'G')
        ]
        
        if not success_data.empty:
            # Success metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Successes", len(success_data))
            
            with col2:
                st.metric("Success Rate", f"{len(success_data)/len(data)*100:.0f}%")
            
            with col3:
                avg_health = success_data['health_score'].mean() if 'health_score' in success_data.columns else 0
                st.metric("Avg Success Health", f"{avg_health:.0f}%")
            
            # Success timeline
            st.markdown("---")
            st.markdown("### 📈 Success Timeline")
            
            timeline_chart = self.visualizer.create_success_timeline(success_data)
            st.plotly_chart(timeline_chart, use_container_width=True)
            
            # Success stories cards
            st.markdown("---")
            st.markdown("### 🌟 Featured Success Stories")
            
            for idx, row in success_data.head(5).iterrows():
                self.render_success_card(row)
        else:
            st.info("No success stories available yet. Keep working on your KPIs!")
    
    def render_reports(self, data):
        """Render reports section"""
        st.markdown("## 📑 Reports")
        
        # Report type selection
        report_type = st.selectbox(
            "Select report type:",
            ["Executive Summary", "Detailed Analysis", "Performance Report", 
             "Risk Assessment", "Custom Report"],
            key="report_type"
        )
        
        # Report parameters
        col1, col2 = st.columns(2)
        
        with col1:
            include_charts = st.checkbox("Include visualizations", value=True)
            include_insights = st.checkbox("Include AI insights", value=True)
            include_recommendations = st.checkbox("Include recommendations", value=True)
        
        with col2:
            report_format = st.selectbox(
                "Output format:",
                ["PDF", "Word", "PowerPoint", "HTML"],
                key="report_format"
            )
            
            report_period = st.selectbox(
                "Report period:",
                ["Current", "Last 7 days", "Last 30 days", "Last quarter", "Custom"],
                key="report_period"
            )
        
        # Generate report button
        if st.button("📄 Generate Report", type="primary", use_container_width=True):
            with st.spinner(f"Generating {report_type}..."):
                try:
                    # Generate report based on type
                    if report_type == "Executive Summary":
                        report_content = self.generate_executive_summary(
                            data, include_charts, include_insights, include_recommendations
                        )
                    elif report_type == "Detailed Analysis":
                        report_content = self.generate_detailed_analysis(
                            data, include_charts, include_insights, include_recommendations
                        )
                    elif report_type == "Performance Report":
                        report_content = self.generate_performance_report(
                            data, include_charts, include_insights, include_recommendations
                        )
                    elif report_type == "Risk Assessment":
                        report_content = self.generate_risk_assessment(
                            data, include_charts, include_insights, include_recommendations
                        )
                    else:
                        report_content = self.generate_custom_report(
                            data, include_charts, include_insights, include_recommendations
                        )
                    
                    # Display report preview
                    st.markdown("---")
                    st.markdown("### 📄 Report Preview")
                    
                    with st.expander("View Report", expanded=True):
                        st.markdown(report_content, unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label=f"⬇️ Download {report_type}",
                        data=report_content,
                        file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    
                    self.log_action(f"Generated {report_type} report")
                    
                    st.success(f"✅ {report_type} generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
    
    def render_welcome_screen(self):
        """Render welcome screen"""
        # Use native Streamlit components instead of raw HTML
        st.title("🚀 Welcome to the Enhanced KPI Dashboard System")
        st.subheader("Transform your KPI tracking with AI-powered insights and advanced analytics")
        
        st.markdown("---")
        
        # Feature cards using columns
        st.markdown("### 🌟 Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container():
                st.markdown("#### 📄 Document Processing")
                st.write("Extract KPIs from SOW, requirements, and other documents automatically")
            
            with st.container():
                st.markdown("#### 📈 Advanced Analytics")
                st.write("Comprehensive analysis with health scores and risk assessments")
        
        with col2:
            with st.container():
                st.markdown("#### 📊 Excel Generation")
                st.write("Create professional Excel dashboards that exceed requirements")
            
            with st.container():
                st.markdown("#### 🎨 Interactive Visualizations")
                st.write("Beautiful, interactive charts and dashboards")
        
        with col3:
            with st.container():
                st.markdown("#### 🧠 AI Insights")
                st.write("Get intelligent recommendations and predictive analytics")
            
            with st.container():
                st.markdown("#### 📑 Professional Reports")
                st.write("Generate executive summaries and detailed reports automatically")
        
        st.markdown("---")
        
        # Call to action
        st.markdown("### 🚀 Get Started")
        st.info("""
        👈 **Use the sidebar to:**
        - Upload your Excel KPI data
        - Process documents to extract KPIs
        - Paste data directly
        - Load sample data to explore features
        """)
    
    # Helper methods
    def get_filtered_data(self):
        """Get filtered data based on sidebar filters"""
        data = st.session_state.kpi_data.copy()
        
        if data.empty:
            return data
        
        # Apply project filter
        if 'filter_projects' in st.session_state and 'project' in data.columns:
            data = data[data['project'].isin(st.session_state.filter_projects)]
        
        # Apply status filter
        if 'filter_status' in st.session_state and 'status' in data.columns:
            data = data[data['status'].isin(st.session_state.filter_status)]
        
        # Apply owner filter
        if 'filter_owners' in st.session_state and 'owner' in data.columns:
            data = data[data['owner'].isin(st.session_state.filter_owners)]
        
        # Apply date filter
        if 'filter_start_date' in st.session_state and 'filter_end_date' in st.session_state and 'last_updated' in data.columns:
            data = data[
                (pd.to_datetime(data['last_updated']).dt.date >= st.session_state.filter_start_date) &
                (pd.to_datetime(data['last_updated']).dt.date <= st.session_state.filter_end_date)
            ]
        
        return data
    
    def apply_search_and_sort(self, data, search_term, sort_by, sort_order):
        """Apply search and sort to data"""
        # Apply search
        if search_term:
            mask = False
            searchable_columns = ['kpi_name', 'project', 'owner', 'description']
            
            for col in searchable_columns:
                if col in data.columns:
                    mask |= data[col].astype(str).str.contains(search_term, case=False, na=False)
            
            data = data[mask]
        
        # Apply sort
        sort_column_map = {
            'Health Score': 'health_score',
            'Progress': 'progress',
            'Last Updated': 'last_updated',
            'Project': 'project',
            'Status': 'status'
        }
        
        sort_col = sort_column_map.get(sort_by, 'health_score')
        
        if sort_col in data.columns:
            data = data.sort_values(
                sort_col,
                ascending=(sort_order == "Ascending")
            )
        
        return data
    
    def render_insight_card(self, insight):
        """Render an insight card using safe UI components"""
        self.ui.render_insight(insight)
    
    def render_kpi_card(self, row, idx):
        """Render a KPI card using safe UI components"""
        with st.expander(f"{row.get('kpi_name', 'KPI')} - {row.get('project', 'Unknown')}", expanded=False):
            self.ui.render_kpi_summary_card(row)
    
    def render_success_card(self, row):
        """Render a success story card"""
        with st.container():
            st.success(f"🏆 **{row.get('kpi_name', 'Success Story')}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Project:** {row.get('project', 'Unknown')}")
                st.write(f"**Owner:** {row.get('owner', 'Unknown')}")
            
            with col2:
                st.metric("Health Score", f"{row.get('health_score', 0):.0f}%")
                st.metric("Progress", f"{row.get('progress', 0)}/5")
            
            if row.get('successes'):
                st.write(f"📝 {row.get('successes')}")
            else:
                st.write("📝 Great achievement!")
    
    def render_activity_feed(self, recent_data):
        """Render recent activity feed"""
        for _, row in recent_data.iterrows():
            status_icon = Config.STATUS_ICONS.get(row.get('status', 'Y'), '🟡')
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{status_icon} **{row.get('kpi_name', 'KPI')}** - {row.get('project', 'Unknown')}")
                    st.caption(f"Updated {pd.to_datetime(row.get('last_updated', datetime.now())).strftime('%Y-%m-%d %H:%M')} by {row.get('owner', 'Unknown')}")
                with col2:
                    if row.get('health_score'):
                        st.metric("Health", f"{row.get('health_score', 0):.0f}%", label_visibility="collapsed")
    
    def show_extraction_summary(self, data):
        """Show summary of extracted KPIs"""
        st.metric("Total KPIs Extracted", len(data))
        
        if 'project' in data.columns:
            st.metric("Projects Identified", data['project'].nunique())
        
        if 'status' in data.columns:
            status_counts = data['status'].value_counts()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Ready", status_counts.get('G', 0))
            with col2:
                st.metric("In Progress", status_counts.get('Y', 0))
            with col3:
                st.metric("Not Started", status_counts.get('R', 0))
    
    def create_empty_kpi_row(self):
        """Create an empty KPI row for new entries"""
        return pd.DataFrame([{
            'kpi_name': 'New KPI',
            'project': 'TBD',
            'description': 'Enter description',
            'target_value': 100.0,
            'actual_value': 0.0,
            'progress': 1,
            'status': 'R',
            'owner': 'TBD',
            'last_updated': datetime.now(),
            'health_score': 0.0,
            'risk_level': 'High'
        }])
    
    def log_action(self, action):
        """Log an action to the change log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp}: {action}"
        st.session_state.change_log.append(log_entry)
        
        # Keep only last 100 entries
        if len(st.session_state.change_log) > 100:
            st.session_state.change_log = st.session_state.change_log[-100:]
    
    def generate_executive_summary(self, data, include_charts, include_insights, include_recommendations):
        """Generate executive summary report"""
        html_content = "<h1>Executive Summary</h1>"
        
        # Add metrics
        metrics = self.analytics.calculate_key_metrics(data)
        html_content += f"""
        <h2>Key Metrics</h2>
        <ul>
            <li>Total KPIs: {metrics['total_kpis']}</li>
            <li>On Track: {metrics['on_track']} ({metrics['on_track_percentage']:.0f}%)</li>
            <li>At Risk: {metrics['at_risk']} ({metrics['at_risk_percentage']:.0f}%)</li>
            <li>Average Health Score: {metrics['avg_health']:.0f}%</li>
            <li>Average Progress: {metrics['avg_progress']:.1f}/5</li>
        </ul>
        """
        
        if include_insights:
            insights = self.analytics.generate_insights(data)
            html_content += "<h2>Key Insights</h2><ul>"
            for insight in insights[:5]:
                html_content += f"<li><strong>{insight['title']}:</strong> {insight['message']}</li>"
            html_content += "</ul>"
        
        if include_recommendations:
            recommendations = self.analytics.generate_recommendations(data)
            html_content += "<h2>Recommendations</h2><ul>"
            for rec in recommendations[:5]:
                html_content += f"<li>{rec}</li>"
            html_content += "</ul>"
        
        return html_content
    
    def generate_detailed_analysis(self, data, include_charts, include_insights, include_recommendations):
        """Generate detailed analysis report"""
        # Similar implementation for detailed analysis
        return "<h1>Detailed Analysis</h1><p>Comprehensive analysis content here...</p>"
    
    def generate_performance_report(self, data, include_charts, include_insights, include_recommendations):
        """Generate performance report"""
        # Similar implementation for performance report
        return "<h1>Performance Report</h1><p>Performance metrics and analysis...</p>"
    
    def generate_risk_assessment(self, data, include_charts, include_insights, include_recommendations):
        """Generate risk assessment report"""
        # Similar implementation for risk assessment
        return "<h1>Risk Assessment</h1><p>Risk analysis and mitigation strategies...</p>"
    
    def generate_custom_report(self, data, include_charts, include_insights, include_recommendations):
        """Generate custom report"""
        # Similar implementation for custom report
        return "<h1>Custom Report</h1><p>Customized report content...</p>"

# Main execution
if __name__ == "__main__":
    app = KPIDashboardApp()
    app.run()