"""
AI-Enhanced Code Review Dashboard
==================================
Streamlit-based UI for comprehensive code review system
"""

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime
import sys
import os

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

from code_review_panel import (
    CodeAnalyst,
    StandardsSpecialist, 
    SecurityReviewer,
    SeniorReviewLead
)

# Page configuration
st.set_page_config(
    page_title="Code Review Panel",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for review panel
st.markdown("""
<style>
    .review-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .finding-critical {
        background-color: #fee;
        border-left: 4px solid #f44336;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .finding-high {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .finding-medium {
        background-color: #fff9c4;
        border-left: 4px solid #ffeb3b;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .finding-low {
        background-color: #f1f8e9;
        border-left: 4px solid #8bc34a;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .roadmap-phase {
        background: #f5f5f5;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

class CodeReviewDashboard:
    """Main dashboard for code review system"""
    
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        """Initialize session state variables"""
        if 'review_report' not in st.session_state:
            st.session_state.review_report = None
        if 'current_view' not in st.session_state:
            st.session_state.current_view = 'overview'
        if 'project_path' not in st.session_state:
            st.session_state.project_path = os.getcwd()
            
    def render_header(self):
        """Render dashboard header"""
        st.markdown("""
        <div class="review-header">
            <h1 style="color: white; margin: 0;">🔍 Code Review Panel</h1>
            <p style="color: white; margin-top: 10px;">
                Comprehensive multi-perspective code analysis system
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_sidebar(self):
        """Render sidebar controls"""
        with st.sidebar:
            st.title("Review Controls")
            
            # Project path selection
            project_path = st.text_input(
                "Project Path",
                value=st.session_state.project_path,
                help="Path to the project to review"
            )
            
            if project_path != st.session_state.project_path:
                st.session_state.project_path = project_path
                st.session_state.review_report = None
                
            # Run review button
            if st.button("🚀 Run Comprehensive Review", type="primary", use_container_width=True):
                with st.spinner("Running comprehensive code review... This may take a few minutes."):
                    self.run_review()
                    
            st.divider()
            
            # View selection
            st.subheader("View Options")
            views = {
                'overview': '📊 Overview',
                'code_analysis': '📝 Code Analysis',
                'standards': '📏 Standards Compliance',
                'security': '🔒 Security Assessment',
                'roadmap': '🗺️ Remediation Roadmap',
                'detailed': '📋 Detailed Findings'
            }
            
            for view_key, view_name in views.items():
                if st.button(view_name, use_container_width=True):
                    st.session_state.current_view = view_key
                    
            st.divider()
            
            # Review statistics
            if st.session_state.review_report:
                st.subheader("Review Statistics")
                report = st.session_state.review_report
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Files", report['executive_summary']['total_files_reviewed'])
                    st.metric("Critical", report['executive_summary']['critical_issues'])
                with col2:
                    st.metric("Issues", report['executive_summary']['total_findings'])
                    st.metric("High", report['executive_summary']['high_issues'])
                    
            # Export options
            st.divider()
            st.subheader("Export Options")
            
            if st.session_state.review_report:
                if st.button("💾 Export JSON Report", use_container_width=True):
                    self.export_json_report()
                    
                if st.button("📄 Export Markdown Report", use_container_width=True):
                    self.export_markdown_report()
                    
    def run_review(self):
        """Execute comprehensive code review"""
        try:
            lead = SeniorReviewLead(st.session_state.project_path)
            report = lead.generate_comprehensive_report()
            st.session_state.review_report = report
            st.success("✅ Code review completed successfully!")
        except Exception as e:
            st.error(f"Error running review: {str(e)}")
            
    def render_overview(self):
        """Render overview dashboard"""
        if not st.session_state.review_report:
            st.info("👆 Click 'Run Comprehensive Review' to start the analysis")
            return
            
        report = st.session_state.review_report
        summary = report['executive_summary']
        
        # Executive Summary
        st.header("Executive Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Files", summary['total_files_reviewed'])
        with col2:
            st.metric("Total Issues", summary['total_findings'])
        with col3:
            st.metric("Critical Issues", summary['critical_issues'])
        with col4:
            st.metric("Est. Remediation", summary['estimated_remediation_time'])
            
        # Security Score Gauge
        st.subheader("Security Score")
        security_score = report['metrics']['security_score']
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = security_score,
            title = {'text': "Security Health"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Issues by Severity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Issues by Severity")
            severity_data = self.get_severity_distribution(report)
            fig = px.pie(
                values=severity_data['count'],
                names=severity_data['severity'],
                color_discrete_map={
                    'Critical': '#f44336',
                    'High': '#ff9800',
                    'Medium': '#ffeb3b',
                    'Low': '#8bc34a',
                    'Info': '#2196f3'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Issues by Category")
            category_data = self.get_category_distribution(report)
            fig = px.bar(
                x=category_data['category'],
                y=category_data['count'],
                color=category_data['category']
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # Top Recommendations
        st.subheader("Key Recommendations")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            st.write(f"{i}. {rec}")
            
    def render_code_analysis(self):
        """Render code analysis view"""
        if not st.session_state.review_report:
            st.info("No review report available")
            return
            
        analysis = st.session_state.review_report['code_analysis']
        
        st.header("Code Analysis Report")
        
        # File Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", analysis['total_files'])
        with col2:
            st.metric("Architectural Patterns", len(analysis['architectural_patterns']))
        with col3:
            st.metric("Technical Debt Items", len(analysis['technical_debt']))
            
        # Architectural Patterns
        st.subheader("Detected Architectural Patterns")
        if analysis['architectural_patterns']:
            for pattern in analysis['architectural_patterns']:
                with st.expander(f"{pattern['pattern']} (Confidence: {pattern['confidence']})"):
                    st.write("Locations:")
                    for loc in pattern['locations']:
                        st.write(f"- {loc}")
        else:
            st.write("No specific patterns detected")
            
        # Technical Debt
        st.subheader("Technical Debt")
        if analysis['technical_debt']:
            debt_df = pd.DataFrame(analysis['technical_debt'])
            st.dataframe(debt_df, use_container_width=True)
        else:
            st.write("No significant technical debt identified")
            
    def render_standards(self):
        """Render standards compliance view"""
        if not st.session_state.review_report:
            st.info("No review report available")
            return
            
        standards = st.session_state.review_report['standards_compliance']
        
        st.header("Standards Compliance Report")
        
        # Compliance Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Standards Violations", len(standards['standards_violations']))
        with col2:
            st.metric("Design Issues", len(standards['design_issues']))
        with col3:
            coverage = standards['test_coverage'].get('coverage_ratio', 0) * 100
            st.metric("Test Coverage", f"{coverage:.1f}%")
            
        # Standards Violations
        st.subheader("Standards Violations")
        if standards['standards_violations']:
            for violation in standards['standards_violations'][:10]:
                severity_class = f"finding-{violation['severity'].lower()}"
                st.markdown(f"""
                <div class="{severity_class}">
                    <strong>{violation['severity']}</strong>: {violation['issue']}<br>
                    <small>File: {violation['file']} (Line: {violation.get('line', 'N/A')})</small><br>
                    <em>Fix: {violation['fix']}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No standards violations found")
            
        # Test Coverage Details
        st.subheader("Test Coverage Analysis")
        coverage_data = standards['test_coverage']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Test Files", coverage_data['test_files'])
            st.metric("Source Files", coverage_data['source_files'])
        with col2:
            untested = len(coverage_data.get('untested_modules', []))
            st.metric("Untested Modules", untested)
            if untested > 0:
                with st.expander("Show Untested Modules"):
                    for module in coverage_data['untested_modules'][:10]:
                        st.write(f"- {module}")
                        
    def render_security(self):
        """Render security assessment view"""
        if not st.session_state.review_report:
            st.info("No review report available")
            return
            
        security = st.session_state.review_report['security_assessment']
        
        st.header("Security Assessment Report")
        
        # Security Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Critical", security['critical'], delta_color="inverse")
        with col2:
            st.metric("High", security['high'], delta_color="inverse")
        with col3:
            st.metric("Medium", security['medium'], delta_color="inverse")
        with col4:
            st.metric("Low", security['low'])
            
        # Security Findings
        st.subheader("Security Vulnerabilities")
        
        # Group by severity
        critical_findings = [f for f in security['findings'] if f['severity'] == 'Critical']
        high_findings = [f for f in security['findings'] if f['severity'] == 'High']
        
        if critical_findings:
            st.error("⚠️ Critical Security Issues")
            for finding in critical_findings:
                st.markdown(f"""
                <div class="finding-critical">
                    <strong>{finding['category']}</strong>: {finding['issue']}<br>
                    <small>File: {finding['file']} (Line: {finding.get('line', 'N/A')})</small><br>
                    <em>Recommendation: {finding['recommendation']}</em>
                </div>
                """, unsafe_allow_html=True)
                
        if high_findings:
            st.warning("⚠️ High Priority Security Issues")
            for finding in high_findings[:5]:
                st.markdown(f"""
                <div class="finding-high">
                    <strong>{finding['category']}</strong>: {finding['issue']}<br>
                    <small>File: {finding['file']} (Line: {finding.get('line', 'N/A')})</small><br>
                    <em>Recommendation: {finding['recommendation']}</em>
                </div>
                """, unsafe_allow_html=True)
                
    def render_roadmap(self):
        """Render remediation roadmap"""
        if not st.session_state.review_report:
            st.info("No review report available")
            return
            
        roadmap = st.session_state.review_report['remediation_roadmap']
        
        st.header("Remediation Roadmap")
        st.write("Structured plan for addressing identified issues")
        
        for phase in roadmap:
            st.markdown(f"""
            <div class="roadmap-phase">
                <h3>Phase {phase['phase']}: {phase['name']}</h3>
                <p><strong>Duration:</strong> {phase['duration']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"View {len(phase['tasks'])} Tasks"):
                for task in phase['tasks']:
                    if 'file' in task:
                        st.write(f"**File:** {task['file']}")
                        st.write(f"**Issue:** {task['issue']}")
                        st.write(f"**Action:** {task['action']}")
                    else:
                        st.write(f"**Action:** {task['action']}")
                        if 'scope' in task:
                            st.write(f"**Scope:** {task['scope']}")
                    st.divider()
                    
    def render_detailed(self):
        """Render detailed findings view"""
        if not st.session_state.review_report:
            st.info("No review report available")
            return
            
        st.header("Detailed Findings")
        
        # Prioritized Issues
        priorities = st.session_state.review_report['prioritized_issues']
        
        st.subheader("Top Priority Issues")
        
        for i, issue in enumerate(priorities, 1):
            severity_class = f"finding-{issue['severity'].lower()}"
            st.markdown(f"""
            <div class="{severity_class}">
                <strong>#{i} - {issue['severity']} Priority</strong><br>
                <strong>Category:</strong> {issue['category']}<br>
                <strong>File:</strong> {issue['file']}<br>
                <strong>Issue:</strong> {issue['issue']}<br>
                <strong>Recommendation:</strong> {issue['recommendation']}<br>
                <strong>Estimated Effort:</strong> {issue['estimated_effort']}
            </div>
            """, unsafe_allow_html=True)
            
    def get_severity_distribution(self, report):
        """Get severity distribution data"""
        findings = []
        if 'security_assessment' in report:
            findings = report['security_assessment']['findings']
            
        severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Info': 0}
        for finding in findings:
            severity = finding.get('severity', 'Info')
            if severity in severity_counts:
                severity_counts[severity] += 1
                
        return pd.DataFrame({
            'severity': list(severity_counts.keys()),
            'count': list(severity_counts.values())
        })
        
    def get_category_distribution(self, report):
        """Get category distribution data"""
        findings = []
        if 'security_assessment' in report:
            findings = report['security_assessment']['findings']
            
        category_counts = {}
        for finding in findings:
            category = finding.get('category', 'Other')
            category_counts[category] = category_counts.get(category, 0) + 1
            
        return pd.DataFrame({
            'category': list(category_counts.keys()),
            'count': list(category_counts.values())
        })
        
    def export_json_report(self):
        """Export report as JSON"""
        if st.session_state.review_report:
            json_str = json.dumps(st.session_state.review_report, indent=2, default=str)
            st.download_button(
                label="Download JSON Report",
                data=json_str,
                file_name=f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
    def export_markdown_report(self):
        """Export report as Markdown"""
        if not st.session_state.review_report:
            return
            
        report = st.session_state.review_report
        md_content = f"""# Code Review Report

## Executive Summary
- **Date**: {report['executive_summary']['review_date']}
- **Files Reviewed**: {report['executive_summary']['total_files_reviewed']}
- **Total Issues**: {report['executive_summary']['total_findings']}
- **Critical Issues**: {report['executive_summary']['critical_issues']}
- **High Issues**: {report['executive_summary']['high_issues']}
- **Estimated Remediation Time**: {report['executive_summary']['estimated_remediation_time']}

## Key Recommendations
"""
        
        for i, rec in enumerate(report['recommendations'], 1):
            md_content += f"{i}. {rec}\n"
            
        md_content += "\n## Security Score\n"
        md_content += f"**Score**: {report['metrics']['security_score']}/100\n"
        
        st.download_button(
            label="Download Markdown Report",
            data=md_content,
            file_name=f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
    def run(self):
        """Main dashboard execution"""
        self.render_header()
        self.render_sidebar()
        
        # Main content area
        if st.session_state.current_view == 'overview':
            self.render_overview()
        elif st.session_state.current_view == 'code_analysis':
            self.render_code_analysis()
        elif st.session_state.current_view == 'standards':
            self.render_standards()
        elif st.session_state.current_view == 'security':
            self.render_security()
        elif st.session_state.current_view == 'roadmap':
            self.render_roadmap()
        elif st.session_state.current_view == 'detailed':
            self.render_detailed()

# Main execution
if __name__ == "__main__":
    dashboard = CodeReviewDashboard()
    dashboard.run()