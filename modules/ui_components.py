"""
UI Components Module
===================
Provides safe, reusable UI components for the KPI Dashboard.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import html
from typing import Dict, List, Any, Optional


class UIComponents:
    """Helper class for creating consistent UI components"""
    
    @staticmethod
    def render_metric_card(title: str, value: Any, delta: Optional[Any] = None, 
                          delta_color: str = "normal", icon: str = "") -> None:
        """Render a styled metric card"""
        with st.container():
            if icon:
                st.markdown(f"### {icon} {title}")
            else:
                st.markdown(f"### {title}")
            
            st.metric(label="", value=value, delta=delta, delta_color=delta_color)
    
    @staticmethod
    def render_info_card(title: str, content: str, card_type: str = "info") -> None:
        """Render an information card with appropriate styling"""
        type_map = {
            "info": st.info,
            "success": st.success,
            "warning": st.warning,
            "error": st.error
        }
        
        render_func = type_map.get(card_type, st.info)
        
        with st.container():
            if title:
                render_func(f"**{title}**\n\n{content}")
            else:
                render_func(content)
    
    @staticmethod
    def render_kpi_summary_card(kpi_data: pd.Series) -> None:
        """Render a KPI summary card with safe HTML escaping"""
        with st.container():
            # Header with status indicator
            status_icons = {"G": "🟢", "Y": "🟡", "R": "🔴"}
            status = kpi_data.get("status", "Y")
            icon = status_icons.get(status, "🟡")
            
            st.markdown(f"### {icon} {html.escape(str(kpi_data.get('kpi_name', 'Unnamed KPI')))}")
            
            # Create columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Project**")
                st.write(html.escape(str(kpi_data.get("project", "N/A"))))
                
                st.markdown("**Owner**")
                st.write(html.escape(str(kpi_data.get("owner", "N/A"))))
            
            with col2:
                health = kpi_data.get("health_score", 0)
                st.metric("Health Score", f"{health:.0f}%")
                
                progress = kpi_data.get("progress", 0)
                st.metric("Progress", f"{progress}/5")
            
            with col3:
                if "target_value" in kpi_data and "actual_value" in kpi_data:
                    target = kpi_data.get("target_value", 0)
                    actual = kpi_data.get("actual_value", 0)
                    completion = (actual / target * 100) if target > 0 else 0
                    st.metric("Completion", f"{completion:.0f}%")
                    st.caption(f"Target: {target:,.0f}")
                    st.caption(f"Actual: {actual:,.0f}")
            
            # Description section
            if kpi_data.get("description"):
                st.markdown("---")
                st.markdown("**Description**")
                st.write(html.escape(str(kpi_data.get("description"))))
            
            # Actions needed
            if kpi_data.get("actions_needed"):
                st.warning(f"⚠️ **Actions Needed:** {html.escape(str(kpi_data.get('actions_needed')))}")
            
            # Success stories
            if kpi_data.get("successes"):
                st.success(f"✅ **Success:** {html.escape(str(kpi_data.get('successes')))}")
    
    @staticmethod
    def render_progress_bar(value: float, max_value: float = 100, label: str = "") -> None:
        """Render a progress bar with label"""
        progress = min(value / max_value, 1.0) if max_value > 0 else 0
        
        if label:
            st.markdown(f"**{label}**")
        
        st.progress(progress)
        st.caption(f"{value:.0f} / {max_value:.0f} ({progress * 100:.0f}%)")
    
    @staticmethod
    def render_status_badge(status: str, label: Optional[str] = None) -> None:
        """Render a status badge"""
        status_config = {
            "G": {"icon": "🟢", "text": "On Track", "type": "success"},
            "Y": {"icon": "🟡", "text": "Needs Attention", "type": "warning"},
            "R": {"icon": "🔴", "text": "At Risk", "type": "error"}
        }
        
        config = status_config.get(status, status_config["Y"])
        display_text = label or config["text"]
        
        if config["type"] == "success":
            st.success(f"{config['icon']} {display_text}")
        elif config["type"] == "warning":
            st.warning(f"{config['icon']} {display_text}")
        elif config["type"] == "error":
            st.error(f"{config['icon']} {display_text}")
    
    @staticmethod
    def render_data_table(data: pd.DataFrame, 
                          show_search: bool = True,
                          show_download: bool = True,
                          height: int = 400) -> None:
        """Render an interactive data table"""
        if show_search:
            search_term = st.text_input("🔍 Search", placeholder="Type to search...")
            if search_term:
                # Filter data based on search term
                mask = False
                for col in data.columns:
                    if data[col].dtype == 'object':
                        mask |= data[col].astype(str).str.contains(search_term, case=False, na=False)
                data = data[mask]
        
        # Display the dataframe
        st.dataframe(
            data,
            use_container_width=True,
            height=height,
            hide_index=True
        )
        
        if show_download and not data.empty:
            csv = data.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    @staticmethod
    def render_insight(insight: Dict[str, Any]) -> None:
        """Render an insight with appropriate styling"""
        type_icons = {
            "success": "✅",
            "warning": "⚠️",
            "error": "🚨",
            "info": "ℹ️"
        }
        
        insight_type = insight.get("type", "info")
        icon = type_icons.get(insight_type, "ℹ️")
        title = html.escape(str(insight.get("title", "Insight")))
        message = html.escape(str(insight.get("message", "")))
        
        # Use appropriate Streamlit function based on type
        if insight_type == "success":
            st.success(f"{icon} **{title}**\n\n{message}")
        elif insight_type == "warning":
            st.warning(f"{icon} **{title}**\n\n{message}")
        elif insight_type == "error":
            st.error(f"{icon} **{title}**\n\n{message}")
        else:
            st.info(f"{icon} **{title}**\n\n{message}")
    
    @staticmethod
    def render_stats_grid(stats: Dict[str, Any], cols: int = 4) -> None:
        """Render a grid of statistics"""
        columns = st.columns(cols)
        
        for idx, (key, value) in enumerate(stats.items()):
            col_idx = idx % cols
            with columns[col_idx]:
                # Determine if value has a delta
                if isinstance(value, dict):
                    st.metric(
                        label=key,
                        value=value.get("value", 0),
                        delta=value.get("delta"),
                        delta_color=value.get("delta_color", "normal")
                    )
                else:
                    st.metric(label=key, value=value)
    
    @staticmethod
    def render_timeline_event(event_date: datetime, 
                             title: str, 
                             description: str,
                             event_type: str = "info") -> None:
        """Render a timeline event"""
        type_colors = {
            "success": "🟢",
            "warning": "🟡",
            "error": "🔴",
            "info": "🔵"
        }
        
        color = type_colors.get(event_type, "🔵")
        
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"**{event_date.strftime('%Y-%m-%d')}**")
                st.markdown(f"{color}")
            
            with col2:
                st.markdown(f"**{html.escape(title)}**")
                st.write(html.escape(description))
    
    @staticmethod
    def render_comparison_metrics(current: float, 
                                 previous: float,
                                 label: str,
                                 format_str: str = ".0f",
                                 suffix: str = "") -> None:
        """Render comparison metrics with change indicator"""
        change = current - previous
        change_pct = (change / previous * 100) if previous != 0 else 0
        
        # Determine color based on whether increase is good or bad
        is_positive_good = True  # Can be parameterized
        delta_color = "normal" if (change >= 0) == is_positive_good else "inverse"
        
        value_str = f"{current:{format_str}}{suffix}"
        delta_str = f"{change:+{format_str}}{suffix} ({change_pct:+.1f}%)"
        
        st.metric(
            label=label,
            value=value_str,
            delta=delta_str,
            delta_color=delta_color
        )
    
    @staticmethod
    def render_filter_sidebar(data: pd.DataFrame) -> Dict[str, Any]:
        """Render filter controls in sidebar and return selected filters"""
        filters = {}
        
        st.sidebar.markdown("### 🔍 Filters")
        
        # Date range filter
        if "last_updated" in data.columns:
            st.sidebar.markdown("#### Date Range")
            date_col = pd.to_datetime(data["last_updated"])
            
            min_date = date_col.min().date()
            max_date = date_col.max().date()
            
            start_date = st.sidebar.date_input(
                "Start Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )
            
            end_date = st.sidebar.date_input(
                "End Date",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )
            
            filters["date_range"] = (start_date, end_date)
        
        # Status filter
        if "status" in data.columns:
            st.sidebar.markdown("#### Status")
            statuses = data["status"].unique().tolist()
            selected_statuses = st.sidebar.multiselect(
                "Select Status",
                options=statuses,
                default=statuses,
                format_func=lambda x: {"G": "🟢 On Track", "Y": "🟡 Needs Attention", "R": "🔴 At Risk"}.get(x, x)
            )
            filters["status"] = selected_statuses
        
        # Project filter
        if "project" in data.columns:
            st.sidebar.markdown("#### Projects")
            projects = data["project"].unique().tolist()
            selected_projects = st.sidebar.multiselect(
                "Select Projects",
                options=projects,
                default=projects
            )
            filters["project"] = selected_projects
        
        # Owner filter
        if "owner" in data.columns:
            st.sidebar.markdown("#### Owners")
            owners = data["owner"].unique().tolist()
            selected_owners = st.sidebar.multiselect(
                "Select Owners",
                options=owners,
                default=owners
            )
            filters["owner"] = selected_owners
        
        return filters
    
    @staticmethod
    def apply_filters(data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to dataframe"""
        filtered_data = data.copy()
        
        # Apply date range filter
        if "date_range" in filters and "last_updated" in filtered_data.columns:
            start_date, end_date = filters["date_range"]
            date_col = pd.to_datetime(filtered_data["last_updated"]).dt.date
            filtered_data = filtered_data[
                (date_col >= start_date) & (date_col <= end_date)
            ]
        
        # Apply status filter
        if "status" in filters and "status" in filtered_data.columns:
            filtered_data = filtered_data[
                filtered_data["status"].isin(filters["status"])
            ]
        
        # Apply project filter
        if "project" in filters and "project" in filtered_data.columns:
            filtered_data = filtered_data[
                filtered_data["project"].isin(filters["project"])
            ]
        
        # Apply owner filter
        if "owner" in filters and "owner" in filtered_data.columns:
            filtered_data = filtered_data[
                filtered_data["owner"].isin(filters["owner"])
            ]
        
        return filtered_data