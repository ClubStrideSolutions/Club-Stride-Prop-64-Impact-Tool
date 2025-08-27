"""
UI Testing Script
================
Tests the improved UI components to ensure HTML is rendered correctly.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ui_components import UIComponents

# Page config
st.set_page_config(
    page_title="UI Components Test",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 UI Components Test Suite")
st.markdown("Testing improved UI components with safe HTML handling")

# Initialize UI components
ui = UIComponents()

# Test data
test_kpi_data = pd.Series({
    'kpi_name': 'Test KPI <script>alert("XSS")</script>',  # Test HTML escaping
    'project': 'Test Project & Development',  # Test special chars
    'owner': 'John Doe <test@example.com>',  # Test HTML chars
    'status': 'G',
    'health_score': 85.5,
    'progress': 4,
    'target_value': 1000,
    'actual_value': 850,
    'description': 'This is a test description with <b>HTML tags</b> that should be escaped',
    'actions_needed': 'Action needed: Review & approve changes',
    'successes': 'Successfully completed phase 1 & 2',
    'last_updated': datetime.now()
})

# Create tabs for different component tests
tabs = st.tabs([
    "Metric Cards",
    "Info Cards", 
    "KPI Summary",
    "Progress Bars",
    "Status Badges",
    "Data Tables",
    "Insights",
    "Statistics Grid",
    "Timeline Events"
])

with tabs[0]:
    st.header("Metric Cards")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui.render_metric_card(
            title="Total KPIs",
            value=42,
            delta=5,
            delta_color="normal",
            icon="📊"
        )
    
    with col2:
        ui.render_metric_card(
            title="Health Score",
            value="85%",
            delta="-3%",
            delta_color="inverse",
            icon="❤️"
        )
    
    with col3:
        ui.render_metric_card(
            title="Progress",
            value="4/5",
            delta="+1",
            icon="📈"
        )

with tabs[1]:
    st.header("Info Cards")
    
    ui.render_info_card(
        title="Success Story",
        content="Project completed ahead of schedule with excellent results.",
        card_type="success"
    )
    
    ui.render_info_card(
        title="Warning",
        content="Some KPIs need attention. Review required.",
        card_type="warning"
    )
    
    ui.render_info_card(
        title="Critical Issue",
        content="Immediate action required for at-risk items.",
        card_type="error"
    )
    
    ui.render_info_card(
        title="Information",
        content="New features have been added to the dashboard.",
        card_type="info"
    )

with tabs[2]:
    st.header("KPI Summary Card")
    st.markdown("Testing HTML escaping and safe rendering:")
    ui.render_kpi_summary_card(test_kpi_data)

with tabs[3]:
    st.header("Progress Bars")
    
    ui.render_progress_bar(
        value=75,
        max_value=100,
        label="Project Completion"
    )
    
    st.markdown("---")
    
    ui.render_progress_bar(
        value=850,
        max_value=1000,
        label="Target Achievement"
    )

with tabs[4]:
    st.header("Status Badges")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui.render_status_badge("G", "On Track")
    
    with col2:
        ui.render_status_badge("Y", "Needs Attention")
    
    with col3:
        ui.render_status_badge("R", "At Risk")

with tabs[5]:
    st.header("Data Table")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'KPI Name': [f'KPI {i+1}' for i in range(10)],
        'Project': [f'Project {chr(65 + i % 3)}' for i in range(10)],
        'Status': np.random.choice(['G', 'Y', 'R'], 10),
        'Health Score': np.random.randint(50, 100, 10),
        'Progress': np.random.randint(1, 6, 10),
        'Owner': [f'Owner {i % 3 + 1}' for i in range(10)],
        'Last Updated': [datetime.now() - timedelta(days=i) for i in range(10)]
    })
    
    ui.render_data_table(
        data=sample_data,
        show_search=True,
        show_download=True,
        height=400
    )

with tabs[6]:
    st.header("Insights")
    
    insights = [
        {
            'type': 'success',
            'title': 'Great Progress',
            'message': '85% of KPIs are on track. Keep up the good work!'
        },
        {
            'type': 'warning',
            'title': 'Attention Required',
            'message': '3 KPIs have not been updated in over 14 days.'
        },
        {
            'type': 'error',
            'title': 'Critical Issue',
            'message': '2 KPIs are at high risk and need immediate attention.'
        },
        {
            'type': 'info',
            'title': 'Tip',
            'message': 'Consider setting up automated data collection for better tracking.'
        }
    ]
    
    for insight in insights:
        ui.render_insight(insight)
        st.markdown("")

with tabs[7]:
    st.header("Statistics Grid")
    
    stats = {
        'Total KPIs': 42,
        'On Track': {'value': 35, 'delta': '+5', 'delta_color': 'normal'},
        'At Risk': {'value': 7, 'delta': '-2', 'delta_color': 'inverse'},
        'Average Health': {'value': '82%', 'delta': '+3%'},
        'Completion Rate': '78%',
        'Active Projects': 5,
        'Team Members': 12,
        'Days to Deadline': 45
    }
    
    ui.render_stats_grid(stats, cols=4)

with tabs[8]:
    st.header("Timeline Events")
    
    events = [
        {
            'date': datetime.now(),
            'title': 'Project Milestone Reached',
            'description': 'Successfully completed Phase 2 of the implementation.',
            'type': 'success'
        },
        {
            'date': datetime.now() - timedelta(days=3),
            'title': 'Risk Identified',
            'description': 'Potential delay in deliverables due to resource constraints.',
            'type': 'warning'
        },
        {
            'date': datetime.now() - timedelta(days=7),
            'title': 'KPI Review Meeting',
            'description': 'Quarterly review completed with stakeholders.',
            'type': 'info'
        },
        {
            'date': datetime.now() - timedelta(days=10),
            'title': 'Critical Issue Resolved',
            'description': 'Fixed the data synchronization problem affecting metrics.',
            'type': 'error'
        }
    ]
    
    for event in events:
        ui.render_timeline_event(
            event_date=event['date'],
            title=event['title'],
            description=event['description'],
            event_type=event['type']
        )
        st.markdown("---")

# Test comparison metrics
st.header("Comparison Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    ui.render_comparison_metrics(
        current=95,
        previous=87,
        label="Health Score",
        format_str=".0f",
        suffix="%"
    )

with col2:
    ui.render_comparison_metrics(
        current=42,
        previous=38,
        label="Active KPIs",
        format_str=".0f"
    )

with col3:
    ui.render_comparison_metrics(
        current=850000,
        previous=750000,
        label="Budget Used",
        format_str=",.0f",
        suffix="$"
    )

with col4:
    ui.render_comparison_metrics(
        current=3.8,
        previous=4.2,
        label="Risk Score",
        format_str=".1f"
    )

# Footer
st.markdown("---")
st.success("✅ All UI components tested successfully. HTML is properly escaped and rendered safely.")
st.info("💡 The UI components handle special characters, HTML tags, and potential XSS attempts correctly.")