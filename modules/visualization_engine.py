"""
Visualization Engine Module
===========================
Creates interactive charts and visualizations using Plotly
for comprehensive KPI data visualization.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class VisualizationEngine:
    """Advanced visualization engine for KPI data"""
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#2C57FA',
            'secondary': '#FA962C',
            'success': '#1B5E20',
            'warning': '#F57C00',
            'danger': '#C62828',
            'info': '#0288D1',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        self.status_colors = {
            'G': self.color_scheme['success'],
            'Y': self.color_scheme['warning'],
            'R': self.color_scheme['danger']
        }
        
        self.theme = {
            'layout': {
                'font': {'family': 'Inter, sans-serif'},
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
                'hoverlabel': {'bgcolor': 'white', 'font_size': 14}
            }
        }
    
    def create_health_distribution_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create health score distribution chart"""
        if 'health_score' not in data.columns:
            return self._create_empty_chart("No health score data available")
        
        # Create bins for health scores
        bins = [0, 30, 50, 70, 85, 100]
        labels = ['Critical', 'At Risk', 'Fair', 'Good', 'Excellent']
        data['health_category'] = pd.cut(data['health_score'], bins=bins, labels=labels)
        
        # Count by category
        category_counts = data['health_category'].value_counts().sort_index()
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=category_counts.index,
                y=category_counts.values,
                marker_color=[
                    self.color_scheme['danger'],
                    self.color_scheme['warning'],
                    self.color_scheme['info'],
                    self.color_scheme['success'],
                    self.color_scheme['primary']
                ][:len(category_counts)],
                text=category_counts.values,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<br>%{text} KPIs<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="KPI Health Score Distribution",
            xaxis_title="Health Category",
            yaxis_title="Number of KPIs",
            showlegend=False,
            **self.theme['layout']
        )
        
        return fig
    
    def create_status_breakdown_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create status breakdown pie/donut chart"""
        if 'status' not in data.columns:
            return self._create_empty_chart("No status data available")
        
        status_counts = data['status'].value_counts()
        status_labels = {
            'G': 'On Track',
            'Y': 'Needs Attention',
            'R': 'At Risk'
        }
        
        # Create donut chart
        fig = go.Figure(data=[
            go.Pie(
                labels=[status_labels.get(s, s) for s in status_counts.index],
                values=status_counts.values,
                hole=0.4,
                marker_colors=[self.status_colors.get(s, '#888') for s in status_counts.index],
                textinfo='label+percent',
                textposition='auto',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
            )
        ])
        
        # Add center text
        fig.add_annotation(
            text=f"Total<br>{len(data)}",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
        
        fig.update_layout(
            title="KPI Status Breakdown",
            showlegend=True,
            **self.theme['layout']
        )
        
        return fig
    
    def create_project_performance_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create project performance comparison chart"""
        if 'project' not in data.columns:
            return self._create_empty_chart("No project data available")
        
        # Calculate metrics by project
        project_metrics = data.groupby('project').agg({
            'health_score': 'mean' if 'health_score' in data.columns else lambda x: 50,
            'status': lambda x: (x == 'G').mean() * 100 if 'status' in data.columns else 50,
            'kpi_name': 'count'
        }).round(1)
        
        project_metrics.columns = ['avg_health', 'success_rate', 'kpi_count']
        project_metrics = project_metrics.sort_values('avg_health', ascending=True)
        
        # Create horizontal bar chart
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Average Health Score', 'Success Rate'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Health score bars
        fig.add_trace(
            go.Bar(
                y=project_metrics.index,
                x=project_metrics['avg_health'],
                orientation='h',
                marker_color=self._get_gradient_colors(project_metrics['avg_health']),
                text=project_metrics['avg_health'].apply(lambda x: f'{x:.0f}%'),
                textposition='auto',
                name='Health Score',
                hovertemplate='<b>%{y}</b><br>Health: %{x:.1f}%<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Success rate bars
        fig.add_trace(
            go.Bar(
                y=project_metrics.index,
                x=project_metrics['success_rate'],
                orientation='h',
                marker_color=self._get_gradient_colors(project_metrics['success_rate']),
                text=project_metrics['success_rate'].apply(lambda x: f'{x:.0f}%'),
                textposition='auto',
                name='Success Rate',
                hovertemplate='<b>%{y}</b><br>Success: %{x:.1f}%<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Health Score (%)", row=1, col=1, range=[0, 100])
        fig.update_xaxes(title_text="Success Rate (%)", row=1, col=2, range=[0, 100])
        
        fig.update_layout(
            title="Project Performance Comparison",
            height=max(400, len(project_metrics) * 40),
            showlegend=False,
            **self.theme['layout']
        )
        
        return fig
    
    def create_performance_matrix(self, data: pd.DataFrame) -> go.Figure:
        """Create performance matrix heatmap"""
        if 'project' not in data.columns or 'status' not in data.columns:
            return self._create_empty_chart("Insufficient data for matrix")
        
        # Create pivot table
        matrix = data.pivot_table(
            index='project',
            columns='status',
            values='kpi_name',
            aggfunc='count',
            fill_value=0
        )
        
        # Ensure all status columns exist
        for status in ['G', 'Y', 'R']:
            if status not in matrix.columns:
                matrix[status] = 0
        
        # Reorder columns
        matrix = matrix[['G', 'Y', 'R']]
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matrix.values,
            x=['On Track', 'Needs Attention', 'At Risk'],
            y=matrix.index,
            colorscale='RdYlGn_r',
            text=matrix.values,
            texttemplate='%{text}',
            textfont={"size": 12},
            hovertemplate='<b>%{y}</b><br>%{x}: %{z} KPIs<extra></extra>',
            colorbar=dict(title="KPI Count")
        ))
        
        fig.update_layout(
            title="KPI Performance Matrix by Project",
            xaxis_title="Status",
            yaxis_title="Project",
            height=max(400, len(matrix) * 30),
            **self.theme['layout']
        )
        
        return fig
    
    def create_correlation_heatmap(self, data: pd.DataFrame) -> go.Figure:
        """Create correlation heatmap for numeric columns"""
        # Select numeric columns
        numeric_cols = ['health_score', 'progress', 'completion_percentage', 
                       'risk_score', 'target_value', 'actual_value']
        
        available_cols = [col for col in numeric_cols if col in data.columns]
        
        if len(available_cols) < 2:
            return self._create_empty_chart("Insufficient numeric data for correlation")
        
        # Calculate correlation matrix
        corr_matrix = data[available_cols].corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>',
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="KPI Metrics Correlation Matrix",
            height=500,
            **self.theme['layout']
        )
        
        return fig
    
    def create_trend_analysis_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create trend analysis chart over time"""
        if 'last_updated' not in data.columns:
            return self._create_empty_chart("No temporal data available")
        
        # Convert to datetime
        data['last_updated'] = pd.to_datetime(data['last_updated'])
        
        # Group by week and status
        data['week'] = data['last_updated'].dt.to_period('W')
        
        # Count by week and status
        if 'status' in data.columns:
            trend_data = data.groupby(['week', 'status']).size().unstack(fill_value=0)
            
            fig = go.Figure()
            
            for status in ['G', 'Y', 'R']:
                if status in trend_data.columns:
                    fig.add_trace(go.Scatter(
                        x=trend_data.index.astype(str),
                        y=trend_data[status],
                        mode='lines+markers',
                        name={'G': 'On Track', 'Y': 'Needs Attention', 'R': 'At Risk'}[status],
                        line=dict(color=self.status_colors[status], width=3),
                        marker=dict(size=8),
                        hovertemplate='<b>Week %{x}</b><br>Count: %{y}<extra></extra>'
                    ))
        else:
            # Simple count over time
            trend_data = data.groupby('week').size()
            
            fig = go.Figure(data=go.Scatter(
                x=trend_data.index.astype(str),
                y=trend_data.values,
                mode='lines+markers',
                line=dict(color=self.color_scheme['primary'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>Week %{x}</b><br>KPIs: %{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title="KPI Trend Analysis",
            xaxis_title="Week",
            yaxis_title="Number of KPIs",
            hovermode='x unified',
            showlegend=True,
            **self.theme['layout']
        )
        
        return fig
    
    def create_risk_distribution_chart(self, risk_data: pd.DataFrame) -> go.Figure:
        """Create risk distribution visualization"""
        if 'risk_score' not in risk_data.columns:
            return self._create_empty_chart("No risk data available")
        
        # Create risk level categories
        risk_data['risk_category'] = pd.cut(
            risk_data['risk_score'],
            bins=[0, 30, 60, 100],
            labels=['Low', 'Medium', 'High']
        )
        
        # Count by category
        risk_counts = risk_data['risk_category'].value_counts()
        
        # Create gauge charts for each risk level
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=('Low Risk', 'Medium Risk', 'High Risk')
        )
        
        colors = [self.color_scheme['success'], self.color_scheme['warning'], self.color_scheme['danger']]
        
        for i, (category, color) in enumerate(zip(['Low', 'Medium', 'High'], colors), 1):
            count = risk_counts.get(category, 0)
            percentage = (count / len(risk_data) * 100) if len(risk_data) > 0 else 0
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=percentage,
                    title={'text': f"{count} KPIs"},
                    delta={'reference': 30},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgray"},
                            {'range': [30, 60], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 60
                        }
                    }
                ),
                row=1, col=i
            )
        
        fig.update_layout(
            title="Risk Distribution Analysis",
            height=300,
            **self.theme['layout']
        )
        
        return fig
    
    def create_risk_matrix(self, risk_data: pd.DataFrame) -> go.Figure:
        """Create risk impact/probability matrix"""
        if 'risk_score' not in risk_data.columns or 'priority_score' not in risk_data.columns:
            # Create synthetic data if not available
            if 'risk_score' in risk_data.columns:
                risk_data['priority_score'] = risk_data['risk_score'] * 0.8
            else:
                return self._create_empty_chart("Insufficient risk data")
        
        # Create scatter plot
        fig = go.Figure()
        
        # Add background zones
        fig.add_shape(
            type="rect", x0=0, y0=0, x1=33, y1=33,
            fillcolor=self.color_scheme['success'], opacity=0.2,
            line=dict(width=0)
        )
        fig.add_shape(
            type="rect", x0=33, y0=0, x1=66, y1=66,
            fillcolor=self.color_scheme['warning'], opacity=0.2,
            line=dict(width=0)
        )
        fig.add_shape(
            type="rect", x0=66, y0=66, x1=100, y1=100,
            fillcolor=self.color_scheme['danger'], opacity=0.2,
            line=dict(width=0)
        )
        
        # Add KPI points
        fig.add_trace(go.Scatter(
            x=risk_data['risk_score'],
            y=risk_data['priority_score'],
            mode='markers',
            marker=dict(
                size=10,
                color=risk_data['risk_score'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Risk Score"),
                line=dict(width=1, color='white')
            ),
            text=risk_data['kpi_name'] if 'kpi_name' in risk_data.columns else None,
            hovertemplate='<b>%{text}</b><br>Risk: %{x:.0f}<br>Priority: %{y:.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Risk vs Priority Matrix",
            xaxis_title="Risk Score",
            yaxis_title="Priority Score",
            xaxis=dict(range=[0, 100]),
            yaxis=dict(range=[0, 100]),
            **self.theme['layout']
        )
        
        # Add zone labels
        fig.add_annotation(x=16, y=16, text="Low Risk<br>Low Priority", showarrow=False)
        fig.add_annotation(x=50, y=50, text="Medium Risk<br>Medium Priority", showarrow=False)
        fig.add_annotation(x=83, y=83, text="High Risk<br>High Priority", showarrow=False)
        
        return fig
    
    def create_completion_timeline(self, prediction_data: Dict) -> go.Figure:
        """Create completion timeline visualization"""
        # Create Gantt-style chart
        fig = go.Figure()
        
        # Current progress bar
        fig.add_trace(go.Bar(
            x=[prediction_data.get('current_completion', 0)],
            y=['Current Progress'],
            orientation='h',
            marker_color=self.color_scheme['primary'],
            text=f"{prediction_data.get('current_completion', 0):.0f}%",
            textposition='auto',
            name='Completed',
            hovertemplate='Completed: %{x:.0f}%<extra></extra>'
        ))
        
        # Remaining work
        remaining = 100 - prediction_data.get('current_completion', 0)
        fig.add_trace(go.Bar(
            x=[remaining],
            y=['Current Progress'],
            orientation='h',
            marker_color=self.color_scheme['light'],
            text=f"{remaining:.0f}%",
            textposition='auto',
            name='Remaining',
            hovertemplate='Remaining: %{x:.0f}%<extra></extra>'
        ))
        
        # Add predicted completion date
        if 'estimated_date' in prediction_data:
            fig.add_annotation(
                x=50, y=-0.5,
                text=f"Estimated Completion: {prediction_data['estimated_date'].strftime('%Y-%m-%d')}",
                showarrow=False,
                font=dict(size=12, color=self.color_scheme['dark'])
            )
        
        # Add confidence indicator
        if 'confidence' in prediction_data:
            fig.add_annotation(
                x=50, y=-0.7,
                text=f"Confidence: {prediction_data['confidence']:.0f}%",
                showarrow=False,
                font=dict(size=10, color=self.color_scheme['info'])
            )
        
        fig.update_layout(
            title="Completion Timeline Projection",
            xaxis_title="Progress (%)",
            barmode='stack',
            height=200,
            xaxis=dict(range=[0, 100]),
            showlegend=True,
            **self.theme['layout']
        )
        
        return fig
    
    def create_success_timeline(self, success_data: pd.DataFrame) -> go.Figure:
        """Create success stories timeline"""
        if 'last_updated' not in success_data.columns:
            return self._create_empty_chart("No timeline data available")
        
        # Convert to datetime
        success_data['last_updated'] = pd.to_datetime(success_data['last_updated'])
        
        # Sort by date
        success_data = success_data.sort_values('last_updated')
        
        # Create timeline
        fig = go.Figure()
        
        # Add success events
        fig.add_trace(go.Scatter(
            x=success_data['last_updated'],
            y=success_data['health_score'] if 'health_score' in success_data.columns else [90] * len(success_data),
            mode='markers+lines',
            marker=dict(
                size=15,
                color=self.color_scheme['success'],
                symbol='star',
                line=dict(width=2, color='white')
            ),
            line=dict(color=self.color_scheme['success'], width=2, dash='dot'),
            text=success_data['kpi_name'] if 'kpi_name' in success_data.columns else None,
            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Health: %{y:.0f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="Success Stories Timeline",
            xaxis_title="Date",
            yaxis_title="Health Score",
            yaxis=dict(range=[0, 100]),
            **self.theme['layout']
        )
        
        return fig
    
    def create_owner_workload_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create owner workload distribution chart"""
        if 'owner' not in data.columns:
            return self._create_empty_chart("No owner data available")
        
        # Calculate metrics by owner
        owner_metrics = data.groupby('owner').agg({
            'kpi_name': 'count',
            'health_score': 'mean' if 'health_score' in data.columns else lambda x: 50,
            'status': lambda x: (x == 'R').sum() if 'status' in data.columns else 0
        })
        
        owner_metrics.columns = ['kpi_count', 'avg_health', 'at_risk_count']
        owner_metrics = owner_metrics.sort_values('kpi_count', ascending=False).head(15)
        
        # Create bubble chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=owner_metrics['kpi_count'],
            y=owner_metrics['avg_health'],
            mode='markers+text',
            marker=dict(
                size=owner_metrics['at_risk_count'] * 10 + 10,
                color=owner_metrics['avg_health'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Health Score"),
                line=dict(width=1, color='white')
            ),
            text=owner_metrics.index,
            textposition="top center",
            hovertemplate='<b>%{text}</b><br>KPIs: %{x}<br>Avg Health: %{y:.0f}%<br>At Risk: %{marker.size}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Owner Workload and Performance",
            xaxis_title="Number of KPIs",
            yaxis_title="Average Health Score",
            yaxis=dict(range=[0, 100]),
            **self.theme['layout']
        )
        
        return fig
    
    def create_progress_gauge(self, value: float, title: str = "Progress") -> go.Figure:
        """Create a single progress gauge"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self._get_color_for_value(value)},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "lightgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            **self.theme['layout']
        )
        
        return fig
    
    def create_mini_sparkline(self, data: List[float], title: str = "") -> go.Figure:
        """Create a mini sparkline chart"""
        fig = go.Figure(go.Scatter(
            y=data,
            mode='lines',
            line=dict(color=self.color_scheme['primary'], width=2),
            fill='tozeroy',
            fillcolor=f"rgba(44, 87, 250, 0.1)"
        ))
        
        fig.update_layout(
            title=title,
            height=100,
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=0, r=0, t=20, b=0),
            **self.theme['layout']
        )
        
        return fig
    
    # Helper methods
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create empty chart with message"""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=self.color_scheme['dark'])
        )
        
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **self.theme['layout']
        )
        
        return fig
    
    def _get_gradient_colors(self, values: pd.Series) -> List[str]:
        """Get gradient colors based on values"""
        colors = []
        for val in values:
            if val >= 80:
                colors.append(self.color_scheme['success'])
            elif val >= 60:
                colors.append(self.color_scheme['info'])
            elif val >= 40:
                colors.append(self.color_scheme['warning'])
            else:
                colors.append(self.color_scheme['danger'])
        return colors
    
    def _get_color_for_value(self, value: float) -> str:
        """Get color based on value threshold"""
        if value >= 80:
            return self.color_scheme['success']
        elif value >= 60:
            return self.color_scheme['info']
        elif value >= 40:
            return self.color_scheme['warning']
        else:
            return self.color_scheme['danger']
    
    def create_dashboard_view(self, data: pd.DataFrame) -> go.Figure:
        """Create comprehensive dashboard view with multiple charts"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Status Distribution', 'Health Score Trend', 
                          'Project Performance', 'Risk Analysis'),
            specs=[[{'type': 'pie'}, {'type': 'scatter'}],
                   [{'type': 'bar'}, {'type': 'scatter'}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Status Distribution (Pie Chart)
        if 'status' in data.columns:
            status_counts = data['status'].value_counts()
            fig.add_trace(
                go.Pie(
                    labels=status_counts.index.map({'G': 'On Track', 'Y': 'At Risk', 'R': 'Critical'}),
                    values=status_counts.values,
                    marker=dict(colors=[self.status_colors.get(s, '#666') for s in status_counts.index]),
                    hole=0.3
                ),
                row=1, col=1
            )
        
        # 2. Health Score Trend (Line Chart)
        if 'health_score' in data.columns:
            if 'last_updated' in data.columns:
                trend_data = data.groupby('last_updated')['health_score'].mean().reset_index()
                fig.add_trace(
                    go.Scatter(
                        x=trend_data['last_updated'],
                        y=trend_data['health_score'],
                        mode='lines+markers',
                        name='Avg Health Score',
                        line=dict(color=self.color_scheme['primary'], width=2)
                    ),
                    row=1, col=2
                )
            else:
                # If no date, show distribution
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(data))),
                        y=data['health_score'].sort_values(),
                        mode='lines+markers',
                        name='Health Score',
                        line=dict(color=self.color_scheme['primary'], width=2)
                    ),
                    row=1, col=2
                )
        
        # 3. Project Performance (Bar Chart)
        if 'project' in data.columns and 'health_score' in data.columns:
            project_perf = data.groupby('project')['health_score'].mean().reset_index()
            project_perf = project_perf.sort_values('health_score', ascending=True)
            
            fig.add_trace(
                go.Bar(
                    x=project_perf['health_score'],
                    y=project_perf['project'],
                    orientation='h',
                    marker=dict(
                        color=project_perf['health_score'],
                        colorscale='RdYlGn',
                        cmin=0,
                        cmax=100
                    )
                ),
                row=2, col=1
            )
        
        # 4. Risk Analysis (Scatter Plot)
        if 'health_score' in data.columns:
            if 'risk_score' in data.columns:
                x_data = data['health_score']
                y_data = data['risk_score']
            else:
                x_data = data['health_score']
                y_data = 100 - data['health_score']
            
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=x_data,
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Health", x=1.15)
                    ),
                    text=data.get('kpi_name', data.index),
                    hovertemplate='<b>%{text}</b><br>Health: %{x:.1f}<br>Risk: %{y:.1f}<extra></extra>'
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title="KPI Dashboard Overview",
            showlegend=False,
            height=700,
            **self.theme['layout']
        )
        
        # Update axes
        fig.update_xaxes(title_text="Health Score", row=2, col=2)
        fig.update_yaxes(title_text="Risk Score", row=2, col=2)
        
        return fig
    
    def create_comprehensive_analysis(self, data: pd.DataFrame) -> Dict[str, go.Figure]:
        """Create comprehensive set of analysis charts"""
        charts = {}
        
        # Create various charts
        if 'health_score' in data.columns:
            charts['health_distribution'] = self.create_health_distribution_chart(data)
        
        if 'status' in data.columns:
            charts['status_breakdown'] = self.create_status_breakdown_chart(data)
        
        if 'project' in data.columns:
            charts['project_performance'] = self.create_project_performance_chart(data)
        
        if 'health_score' in data.columns and 'actual_value' in data.columns:
            charts['performance_matrix'] = self.create_performance_matrix(data)
        
        # Add correlation heatmap if enough numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 2:
            charts['correlation'] = self.create_correlation_heatmap(data)
        
        if 'owner' in data.columns:
            charts['owner_workload'] = self.create_owner_workload_chart(data)
        
        return charts
    
    def create_interactive_dashboard(self, data: pd.DataFrame) -> go.Figure:
        """Create an interactive dashboard with dropdown selectors"""
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces for different metrics
        if 'health_score' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['health_score'],
                    name='Health Score',
                    visible=True,
                    line=dict(color=self.color_scheme['success'], width=2)
                ),
                secondary_y=False
            )
        
        if 'risk_score' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['risk_score'],
                    name='Risk Score',
                    visible=False,
                    line=dict(color=self.color_scheme['danger'], width=2)
                ),
                secondary_y=False
            )
        
        if 'completion_rate' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['completion_rate'],
                    name='Completion Rate',
                    visible=False,
                    line=dict(color=self.color_scheme['info'], width=2)
                ),
                secondary_y=False
            )
        
        # Create buttons for dropdown
        buttons = []
        metrics = ['Health Score', 'Risk Score', 'Completion Rate']
        
        for i, metric in enumerate(metrics):
            visibility = [False] * len(metrics)
            visibility[i] = True
            
            button = dict(
                label=metric,
                method='update',
                args=[{'visible': visibility},
                      {'title': f'KPI {metric} Analysis'}]
            )
            buttons.append(button)
        
        # Add dropdown menu
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction='down',
                    pad={'r': 10, 't': 10},
                    showactive=True,
                    x=0.1,
                    xanchor='left',
                    y=1.15,
                    yanchor='top'
                )
            ],
            title='Interactive KPI Analysis',
            height=500,
            **self.theme['layout']
        )
        
        # Update axes
        fig.update_xaxes(title_text='KPI Index')
        fig.update_yaxes(title_text='Value', secondary_y=False)
        
        return fig
    
    def create_executive_summary(self, data: pd.DataFrame) -> go.Figure:
        """Create executive summary visualization"""
        # Calculate key metrics
        metrics = {}
        
        if 'status' in data.columns:
            status_counts = data['status'].value_counts()
            metrics['On Track'] = status_counts.get('G', 0)
            metrics['At Risk'] = status_counts.get('Y', 0)
            metrics['Critical'] = status_counts.get('R', 0)
        
        if 'health_score' in data.columns:
            metrics['Avg Health'] = f"{data['health_score'].mean():.1f}%"
            metrics['Min Health'] = f"{data['health_score'].min():.1f}%"
            metrics['Max Health'] = f"{data['health_score'].max():.1f}%"
        
        # Create indicator chart
        fig = go.Figure()
        
        # Add metric cards
        for i, (label, value) in enumerate(metrics.items()):
            color = self.color_scheme['primary']
            if 'Critical' in label or 'Min' in label:
                color = self.color_scheme['danger']
            elif 'At Risk' in label:
                color = self.color_scheme['warning']
            elif 'On Track' in label or 'Max' in label:
                color = self.color_scheme['success']
            
            fig.add_trace(go.Indicator(
                mode="number",
                value=value if isinstance(value, (int, float)) else 0,
                title={'text': label},
                number={'suffix': '' if isinstance(value, (int, float)) else str(value)},
                domain={'x': [i/len(metrics), (i+1)/len(metrics)], 'y': [0, 1]}
            ))
        
        fig.update_layout(
            title="Executive Summary",
            height=200,
            **self.theme['layout']
        )
        
        return fig