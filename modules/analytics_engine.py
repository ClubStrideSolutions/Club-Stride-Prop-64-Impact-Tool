"""
Analytics Engine Module
=======================
Provides AI-powered insights, predictions, and advanced analytics
for KPI data analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AnalyticsEngine:
    """Advanced analytics and AI-powered insights for KPI data"""
    
    def __init__(self):
        self.insight_thresholds = {
            'critical_health': 50,
            'warning_health': 70,
            'good_health': 80,
            'stale_days': 14,
            'critical_stale_days': 30,
            'at_risk_threshold': 0.3,
            'success_threshold': 0.7,
            'low_progress': 2,
            'high_progress': 4
        }
        
        self.risk_weights = {
            'status': 0.35,
            'progress': 0.25,
            'health': 0.25,
            'recency': 0.15
        }
    
    def enrich_with_analytics(self, data: pd.DataFrame) -> pd.DataFrame:
        """Enrich dataframe with calculated analytics fields"""
        if data.empty:
            return data
        
        enriched = data.copy()
        
        # Calculate health scores
        enriched['health_score'] = enriched.apply(self._calculate_health_score, axis=1)
        
        # Calculate risk scores
        enriched['risk_score'] = enriched.apply(self._calculate_risk_score, axis=1)
        enriched['risk_level'] = enriched['risk_score'].apply(self._get_risk_level)
        
        # Calculate completion percentage
        if 'target_value' in enriched.columns and 'actual_value' in enriched.columns:
            enriched['completion_percentage'] = enriched.apply(
                lambda x: min((x['actual_value'] / x['target_value'] * 100) if x['target_value'] > 0 else 0, 100),
                axis=1
            )
        
        # Calculate days since update
        if 'last_updated' in enriched.columns:
            enriched['days_since_update'] = (datetime.now() - pd.to_datetime(enriched['last_updated'])).dt.days
            enriched['update_status'] = enriched['days_since_update'].apply(self._get_update_status)
        
        # Add trend analysis
        enriched['trend'] = self._calculate_trends(enriched)
        
        # Add priority score
        enriched['priority_score'] = enriched.apply(self._calculate_priority_score, axis=1)
        
        # Add predicted completion date
        enriched['predicted_completion'] = enriched.apply(self._predict_completion_date, axis=1)
        
        return enriched
    
    def generate_insights(self, data: pd.DataFrame) -> List[Dict]:
        """Generate AI-powered insights from KPI data"""
        insights = []
        
        if data.empty:
            return insights
        
        # Portfolio health insight
        avg_health = data['health_score'].mean() if 'health_score' in data.columns else 50
        if avg_health < self.insight_thresholds['critical_health']:
            insights.append({
                'type': 'error',
                'title': 'Critical Portfolio Health',
                'message': f'Average health score is {avg_health:.0f}% - immediate intervention required',
                'priority': 'high',
                'affected_kpis': len(data[data['health_score'] < self.insight_thresholds['critical_health']])
            })
        elif avg_health < self.insight_thresholds['warning_health']:
            insights.append({
                'type': 'warning',
                'title': 'Portfolio Health Warning',
                'message': f'Average health score is {avg_health:.0f}% - attention needed',
                'priority': 'medium',
                'affected_kpis': len(data[data['health_score'] < self.insight_thresholds['warning_health']])
            })
        elif avg_health > self.insight_thresholds['good_health']:
            insights.append({
                'type': 'success',
                'title': 'Excellent Portfolio Health',
                'message': f'Portfolio maintaining {avg_health:.0f}% health score',
                'priority': 'low',
                'affected_kpis': len(data[data['health_score'] > self.insight_thresholds['good_health']])
            })
        
        # Risk analysis insight
        if 'status' in data.columns:
            at_risk_ratio = (data['status'] == 'R').mean()
            if at_risk_ratio > self.insight_thresholds['at_risk_threshold']:
                insights.append({
                    'type': 'error',
                    'title': 'High Risk Alert',
                    'message': f'{at_risk_ratio*100:.0f}% of KPIs are at risk',
                    'priority': 'high',
                    'affected_kpis': (data['status'] == 'R').sum()
                })
        
        # Progress insights
        if 'progress' in data.columns:
            low_progress = (data['progress'] <= self.insight_thresholds['low_progress']).sum()
            if low_progress > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Progress Concerns',
                    'message': f'{low_progress} KPIs showing limited progress',
                    'priority': 'medium',
                    'affected_kpis': low_progress
                })
            
            high_performers = (data['progress'] >= self.insight_thresholds['high_progress']).sum()
            if high_performers > len(data) * 0.5:
                insights.append({
                    'type': 'success',
                    'title': 'Strong Progress',
                    'message': f'{high_performers} KPIs showing excellent progress',
                    'priority': 'low',
                    'affected_kpis': high_performers
                })
        
        # Update frequency insights
        if 'days_since_update' in data.columns:
            stale_kpis = data[data['days_since_update'] > self.insight_thresholds['stale_days']]
            critical_stale = data[data['days_since_update'] > self.insight_thresholds['critical_stale_days']]
            
            if len(critical_stale) > 0:
                insights.append({
                    'type': 'error',
                    'title': 'Critical Update Gap',
                    'message': f'{len(critical_stale)} KPIs not updated in 30+ days',
                    'priority': 'high',
                    'affected_kpis': len(critical_stale)
                })
            elif len(stale_kpis) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Update Required',
                    'message': f'{len(stale_kpis)} KPIs need updates (14+ days old)',
                    'priority': 'medium',
                    'affected_kpis': len(stale_kpis)
                })
        
        # Project-specific insights
        if 'project' in data.columns:
            project_health = data.groupby('project')['health_score'].mean()
            struggling_projects = project_health[project_health < self.insight_thresholds['critical_health']]
            
            if len(struggling_projects) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Projects Needing Support',
                    'message': f'{len(struggling_projects)} projects below critical health threshold',
                    'priority': 'high',
                    'projects': struggling_projects.index.tolist()
                })
        
        # Completion rate insights
        if 'completion_percentage' in data.columns:
            avg_completion = data['completion_percentage'].mean()
            
            if avg_completion < 40:
                insights.append({
                    'type': 'error',
                    'title': 'Low Completion Rate',
                    'message': f'Average completion is only {avg_completion:.0f}%',
                    'priority': 'high'
                })
            elif avg_completion > 80:
                insights.append({
                    'type': 'success',
                    'title': 'High Completion Rate',
                    'message': f'Average completion at {avg_completion:.0f}%',
                    'priority': 'low'
                })
        
        # Trend insights
        if 'trend' in data.columns:
            improving = (data['trend'] == 'improving').sum()
            declining = (data['trend'] == 'declining').sum()
            
            if declining > improving:
                insights.append({
                    'type': 'warning',
                    'title': 'Negative Trend',
                    'message': f'{declining} KPIs showing declining trend',
                    'priority': 'medium'
                })
            elif improving > declining * 2:
                insights.append({
                    'type': 'success',
                    'title': 'Positive Momentum',
                    'message': f'{improving} KPIs showing improvement',
                    'priority': 'low'
                })
        
        return insights
    
    def generate_predictions(self, data: pd.DataFrame) -> Dict:
        """Generate predictions for KPI completion"""
        predictions = {}
        
        if data.empty:
            return predictions
        
        # Group by project for predictions
        if 'project' in data.columns:
            for project in data['project'].unique():
                project_data = data[data['project'] == project]
                
                # Calculate current metrics
                current_completion = 0
                if 'completion_percentage' in project_data.columns:
                    current_completion = project_data['completion_percentage'].mean()
                elif 'actual_value' in project_data.columns and 'target_value' in project_data.columns:
                    total_actual = project_data['actual_value'].sum()
                    total_target = project_data['target_value'].sum()
                    current_completion = (total_actual / total_target * 100) if total_target > 0 else 0
                
                # Estimate completion timeline
                avg_progress = project_data['progress'].mean() if 'progress' in project_data.columns else 3
                
                # Simple velocity calculation
                if current_completion > 0 and avg_progress > 2:
                    # Assume 30 days of work so far
                    daily_velocity = current_completion / 30
                    
                    if daily_velocity > 0:
                        remaining_work = 100 - current_completion
                        estimated_days = remaining_work / daily_velocity
                        
                        # Adjust based on progress level
                        progress_factor = avg_progress / 3.0  # Normalize to 1.0 for average
                        adjusted_days = estimated_days / progress_factor
                        
                        # Calculate confidence based on data quality
                        confidence = self._calculate_prediction_confidence(project_data)
                        
                        predictions[project] = {
                            'current_completion': current_completion,
                            'estimated_days': max(0, adjusted_days),
                            'estimated_date': datetime.now() + timedelta(days=adjusted_days),
                            'confidence': confidence,
                            'velocity': daily_velocity,
                            'kpi_count': len(project_data)
                        }
        
        return predictions
    
    def calculate_key_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate key performance metrics"""
        metrics = {
            'total_kpis': len(data),
            'on_track': 0,
            'at_risk': 0,
            'needs_attention': 0,
            'on_track_percentage': 0,
            'at_risk_percentage': 0,
            'avg_health': 0,
            'avg_progress': 0,
            'avg_completion': 0
        }
        
        if data.empty:
            return metrics
        
        # Status metrics
        if 'status' in data.columns:
            metrics['on_track'] = (data['status'] == 'G').sum()
            metrics['at_risk'] = (data['status'] == 'R').sum()
            metrics['needs_attention'] = (data['status'] == 'Y').sum()
            
            total = len(data)
            metrics['on_track_percentage'] = (metrics['on_track'] / total * 100) if total > 0 else 0
            metrics['at_risk_percentage'] = (metrics['at_risk'] / total * 100) if total > 0 else 0
        
        # Average metrics
        if 'health_score' in data.columns:
            metrics['avg_health'] = data['health_score'].mean()
        
        if 'progress' in data.columns:
            metrics['avg_progress'] = data['progress'].mean()
        
        if 'completion_percentage' in data.columns:
            metrics['avg_completion'] = data['completion_percentage'].mean()
        
        # Trend metrics
        if 'trend' in data.columns:
            metrics['improving'] = (data['trend'] == 'improving').sum()
            metrics['declining'] = (data['trend'] == 'declining').sum()
            metrics['stable'] = (data['trend'] == 'stable').sum()
        
        # Resource metrics
        if 'owner' in data.columns:
            metrics['unique_owners'] = data['owner'].nunique()
            owner_load = data['owner'].value_counts()
            metrics['max_owner_load'] = owner_load.max()
            metrics['avg_owner_load'] = owner_load.mean()
        
        if 'project' in data.columns:
            metrics['unique_projects'] = data['project'].nunique()
        
        return metrics
    
    def calculate_performance_rankings(self, data: pd.DataFrame) -> Dict:
        """Calculate performance rankings for KPIs, projects, and owners"""
        rankings = {
            'top_performers': [],
            'need_improvement': [],
            'critical': []
        }
        
        if data.empty:
            return rankings
        
        # KPI rankings
        if 'health_score' in data.columns:
            kpi_scores = data[['kpi_name', 'health_score', 'project']].copy()
            kpi_scores = kpi_scores.sort_values('health_score', ascending=False)
            
            # Top performers (>80%)
            top = kpi_scores[kpi_scores['health_score'] > 80]
            for _, row in top.head(10).iterrows():
                rankings['top_performers'].append({
                    'name': row['kpi_name'][:50] + '...' if len(str(row['kpi_name'])) > 50 else row['kpi_name'],
                    'score': row['health_score'],
                    'project': row['project']
                })
            
            # Need improvement (50-80%)
            middle = kpi_scores[(kpi_scores['health_score'] >= 50) & (kpi_scores['health_score'] <= 80)]
            for _, row in middle.head(10).iterrows():
                rankings['need_improvement'].append({
                    'name': row['kpi_name'][:50] + '...' if len(str(row['kpi_name'])) > 50 else row['kpi_name'],
                    'score': row['health_score'],
                    'project': row['project']
                })
            
            # Critical (<50%)
            critical = kpi_scores[kpi_scores['health_score'] < 50]
            for _, row in critical.head(10).iterrows():
                rankings['critical'].append({
                    'name': row['kpi_name'][:50] + '...' if len(str(row['kpi_name'])) > 50 else row['kpi_name'],
                    'score': row['health_score'],
                    'project': row['project']
                })
        
        # Project rankings
        if 'project' in data.columns and 'health_score' in data.columns:
            project_scores = data.groupby('project').agg({
                'health_score': 'mean',
                'status': lambda x: (x == 'G').mean() * 100
            }).round(1)
            
            project_scores.columns = ['avg_health', 'success_rate']
            project_scores['overall_score'] = (project_scores['avg_health'] + project_scores['success_rate']) / 2
            
            rankings['project_rankings'] = project_scores.sort_values('overall_score', ascending=False).to_dict('index')
        
        # Owner rankings
        if 'owner' in data.columns and 'health_score' in data.columns:
            owner_scores = data.groupby('owner').agg({
                'health_score': 'mean',
                'status': lambda x: (x == 'G').mean() * 100,
                'kpi_name': 'count'
            }).round(1)
            
            owner_scores.columns = ['avg_health', 'success_rate', 'kpi_count']
            owner_scores['performance_score'] = (owner_scores['avg_health'] + owner_scores['success_rate']) / 2
            
            rankings['owner_rankings'] = owner_scores.sort_values('performance_score', ascending=False).to_dict('index')
        
        return rankings
    
    def calculate_risk_scores(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate comprehensive risk scores"""
        risk_data = data.copy()
        
        if risk_data.empty:
            return risk_data
        
        # Already calculated in enrich_with_analytics
        if 'risk_score' not in risk_data.columns:
            risk_data['risk_score'] = risk_data.apply(self._calculate_risk_score, axis=1)
            risk_data['risk_level'] = risk_data['risk_score'].apply(self._get_risk_level)
        
        # Add risk factors breakdown
        risk_data['risk_factors'] = risk_data.apply(self._identify_risk_factors, axis=1)
        
        # Add risk trend
        risk_data['risk_trend'] = risk_data.apply(self._calculate_risk_trend, axis=1)
        
        return risk_data
    
    def generate_recommendations(self, data: pd.DataFrame) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if data.empty:
            return recommendations
        
        # High-risk KPIs
        if 'risk_level' in data.columns:
            high_risk = data[data['risk_level'] == 'High']
            if len(high_risk) > 0:
                recommendations.append(
                    f"🚨 Immediate Action: {len(high_risk)} high-risk KPIs require intervention. "
                    f"Focus on: {', '.join(high_risk['kpi_name'].head(3).tolist())}"
                )
        
        # Stale updates
        if 'days_since_update' in data.columns:
            stale = data[data['days_since_update'] > 14]
            if len(stale) > 0:
                recommendations.append(
                    f"📅 Update Required: {len(stale)} KPIs haven't been updated in 2+ weeks. "
                    f"Priority updates for: {', '.join(stale['owner'].unique()[:3])}"
                )
        
        # Low progress
        if 'progress' in data.columns:
            low_progress = data[data['progress'] <= 2]
            if len(low_progress) > 0:
                recommendations.append(
                    f"🔧 Progress Support: {len(low_progress)} KPIs showing limited progress. "
                    f"Consider additional resources or revised targets."
                )
        
        # Resource balancing
        if 'owner' in data.columns:
            owner_load = data.groupby('owner').agg({
                'kpi_name': 'count',
                'health_score': 'mean' if 'health_score' in data.columns else lambda x: 50
            })
            
            overloaded = owner_load[owner_load['kpi_name'] > 10]
            if len(overloaded) > 0:
                recommendations.append(
                    f"⚖️ Resource Balancing: {len(overloaded)} owners managing 10+ KPIs. "
                    f"Consider redistributing workload."
                )
            
            struggling = owner_load[owner_load['health_score'] < 60]
            if len(struggling) > 0:
                recommendations.append(
                    f"🤝 Support Needed: {len(struggling)} owners with average health score <60%. "
                    f"Provide additional support or training."
                )
        
        # Project recommendations
        if 'project' in data.columns and 'health_score' in data.columns:
            project_health = data.groupby('project')['health_score'].mean()
            
            low_performing = project_health[project_health < 60]
            if len(low_performing) > 0:
                recommendations.append(
                    f"📊 Project Review: {len(low_performing)} projects below 60% health. "
                    f"Consider project-level interventions."
                )
            
            high_performing = project_health[project_health > 85]
            if len(high_performing) > 0:
                recommendations.append(
                    f"🌟 Best Practices: Study {', '.join(high_performing.index[:2])} "
                    f"for successful strategies to replicate."
                )
        
        # Trend-based recommendations
        if 'trend' in data.columns:
            declining = data[data['trend'] == 'declining']
            if len(declining) > len(data) * 0.3:
                recommendations.append(
                    f"📉 Trend Alert: {len(declining)} KPIs showing declining trend. "
                    f"Review targets and strategies."
                )
            
            improving = data[data['trend'] == 'improving']
            if len(improving) > len(data) * 0.5:
                recommendations.append(
                    f"📈 Positive Momentum: {len(improving)} KPIs improving. "
                    f"Maintain current strategies and document successes."
                )
        
        # Completion recommendations
        if 'completion_percentage' in data.columns:
            near_complete = data[(data['completion_percentage'] >= 80) & (data['completion_percentage'] < 100)]
            if len(near_complete) > 0:
                recommendations.append(
                    f"🎯 Final Push: {len(near_complete)} KPIs are 80%+ complete. "
                    f"Focus resources to achieve full completion."
                )
        
        if not recommendations:
            recommendations.append("✅ All KPIs within acceptable parameters. Continue current monitoring.")
        
        return recommendations
    
    def generate_risk_recommendations(self, risk_data: pd.DataFrame) -> List[Dict]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        if risk_data.empty:
            return recommendations
        
        # Group by risk level
        if 'risk_level' in risk_data.columns:
            for risk_level in ['High', 'Medium', 'Low']:
                level_data = risk_data[risk_data['risk_level'] == risk_level]
                
                if len(level_data) > 0:
                    if risk_level == 'High':
                        rec = {
                            'title': f'Critical Risk Mitigation ({len(level_data)} KPIs)',
                            'description': 'Immediate intervention required for high-risk KPIs',
                            'priority': 'Critical',
                            'impact': 'High',
                            'actions': [
                                'Schedule emergency review meetings',
                                'Allocate additional resources',
                                'Consider target adjustments',
                                'Implement daily monitoring'
                            ],
                            'affected_kpis': level_data['kpi_name'].head(5).tolist()
                        }
                    elif risk_level == 'Medium':
                        rec = {
                            'title': f'Moderate Risk Management ({len(level_data)} KPIs)',
                            'description': 'Proactive measures needed to prevent escalation',
                            'priority': 'Medium',
                            'impact': 'Moderate',
                            'actions': [
                                'Increase monitoring frequency',
                                'Review progress barriers',
                                'Provide targeted support',
                                'Update action plans'
                            ],
                            'affected_kpis': level_data['kpi_name'].head(3).tolist()
                        }
                    else:  # Low
                        rec = {
                            'title': f'Maintenance Activities ({len(level_data)} KPIs)',
                            'description': 'Continue standard monitoring and support',
                            'priority': 'Low',
                            'impact': 'Low',
                            'actions': [
                                'Maintain current approach',
                                'Document best practices',
                                'Share successes',
                                'Regular updates'
                            ],
                            'affected_kpis': []
                        }
                    
                    recommendations.append(rec)
        
        # Specific risk factor recommendations
        if 'risk_factors' in risk_data.columns:
            common_factors = {}
            for factors in risk_data['risk_factors']:
                if isinstance(factors, list):
                    for factor in factors:
                        common_factors[factor] = common_factors.get(factor, 0) + 1
            
            # Address most common risk factors
            for factor, count in sorted(common_factors.items(), key=lambda x: x[1], reverse=True)[:3]:
                if factor == 'status_red':
                    recommendations.append({
                        'title': f'Status Improvement Plan ({count} KPIs)',
                        'description': 'Multiple KPIs showing red status',
                        'priority': 'High',
                        'impact': 'High',
                        'actions': [
                            'Conduct root cause analysis',
                            'Develop recovery plans',
                            'Set interim milestones',
                            'Increase stakeholder communication'
                        ]
                    })
                elif factor == 'low_progress':
                    recommendations.append({
                        'title': f'Progress Acceleration ({count} KPIs)',
                        'description': 'KPIs showing limited progress',
                        'priority': 'Medium',
                        'impact': 'Medium',
                        'actions': [
                            'Review activity plans',
                            'Identify blockers',
                            'Provide additional training',
                            'Consider process improvements'
                        ]
                    })
                elif factor == 'stale_update':
                    recommendations.append({
                        'title': f'Update Schedule Enforcement ({count} KPIs)',
                        'description': 'KPIs with outdated information',
                        'priority': 'Medium',
                        'impact': 'Low',
                        'actions': [
                            'Implement update reminders',
                            'Automate data collection',
                            'Review reporting processes',
                            'Assign backup owners'
                        ]
                    })
        
        return recommendations
    
    def generate_statistical_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate comprehensive statistical summary"""
        if data.empty:
            return pd.DataFrame()
        
        summary_data = []
        
        # Numeric columns summary
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col in ['health_score', 'progress', 'completion_percentage', 'risk_score', 
                      'target_value', 'actual_value', 'days_since_update']:
                stats = {
                    'Metric': col.replace('_', ' ').title(),
                    'Mean': data[col].mean(),
                    'Median': data[col].median(),
                    'Std Dev': data[col].std(),
                    'Min': data[col].min(),
                    'Max': data[col].max(),
                    'Q1': data[col].quantile(0.25),
                    'Q3': data[col].quantile(0.75),
                    'IQR': data[col].quantile(0.75) - data[col].quantile(0.25)
                }
                summary_data.append(stats)
        
        # Categorical columns summary
        if 'status' in data.columns:
            status_dist = data['status'].value_counts()
            for status, count in status_dist.items():
                summary_data.append({
                    'Metric': f'Status {status}',
                    'Count': count,
                    'Percentage': count / len(data) * 100
                })
        
        if 'risk_level' in data.columns:
            risk_dist = data['risk_level'].value_counts()
            for level, count in risk_dist.items():
                summary_data.append({
                    'Metric': f'Risk {level}',
                    'Count': count,
                    'Percentage': count / len(data) * 100
                })
        
        return pd.DataFrame(summary_data)
    
    # Private helper methods
    def _calculate_health_score(self, row: pd.Series) -> float:
        """Calculate comprehensive health score for a KPI"""
        score = 0
        max_score = 100
        
        # Completion component (40%)
        if 'target_value' in row and 'actual_value' in row:
            target = row.get('target_value', 100)
            actual = row.get('actual_value', 0)
            if target > 0:
                completion_ratio = min(actual / target, 1.0)
                score += completion_ratio * 40
        
        # Progress component (30%)
        if 'progress' in row:
            progress = row.get('progress', 3)
            progress_score = (progress - 1) / 4.0  # Normalize 1-5 to 0-1
            score += progress_score * 30
        
        # Status component (20%)
        if 'status' in row:
            status = row.get('status', 'Y')
            status_scores = {'G': 20, 'Y': 10, 'R': 0}
            score += status_scores.get(status, 10)
        
        # Recency component (10%)
        if 'last_updated' in row:
            try:
                last_updated = pd.to_datetime(row['last_updated'])
                days_old = (datetime.now() - last_updated).days
                
                if days_old <= 7:
                    score += 10
                elif days_old <= 14:
                    score += 7
                elif days_old <= 30:
                    score += 3
                else:
                    score += 0
            except:
                score += 5  # Default if date parsing fails
        
        return min(score, max_score)
    
    def _calculate_risk_score(self, row: pd.Series) -> float:
        """Calculate risk score for a KPI"""
        risk_score = 0
        
        # Status risk (0-35 points)
        if 'status' in row:
            status = row.get('status', 'Y')
            if status == 'R':
                risk_score += 35
            elif status == 'Y':
                risk_score += 15
        
        # Progress risk (0-25 points)
        if 'progress' in row:
            progress = row.get('progress', 3)
            if progress <= 1:
                risk_score += 25
            elif progress == 2:
                risk_score += 15
            elif progress == 3:
                risk_score += 8
        
        # Health score risk (0-25 points)
        if 'health_score' in row:
            health = row.get('health_score', 50)
            if health < 30:
                risk_score += 25
            elif health < 50:
                risk_score += 15
            elif health < 70:
                risk_score += 8
        
        # Update recency risk (0-15 points)
        if 'last_updated' in row:
            try:
                last_updated = pd.to_datetime(row['last_updated'])
                days_old = (datetime.now() - last_updated).days
                
                if days_old > 30:
                    risk_score += 15
                elif days_old > 14:
                    risk_score += 10
                elif days_old > 7:
                    risk_score += 5
            except:
                risk_score += 10
        
        return min(risk_score, 100)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score >= 70:
            return 'High'
        elif risk_score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def _get_update_status(self, days: int) -> str:
        """Get update status based on days since last update"""
        if days <= 7:
            return 'Current'
        elif days <= 14:
            return 'Recent'
        elif days <= 30:
            return 'Stale'
        else:
            return 'Critical'
    
    def _calculate_trends(self, data: pd.DataFrame) -> pd.Series:
        """Calculate trend for each KPI"""
        trends = []
        
        for _, row in data.iterrows():
            trend = 'stable'
            
            # Simple trend based on progress and health
            if 'progress' in row and 'health_score' in row:
                progress = row.get('progress', 3)
                health = row.get('health_score', 50)
                
                if progress >= 4 and health >= 70:
                    trend = 'improving'
                elif progress <= 2 or health < 50:
                    trend = 'declining'
            
            trends.append(trend)
        
        return pd.Series(trends, index=data.index)
    
    def _calculate_priority_score(self, row: pd.Series) -> float:
        """Calculate priority score for resource allocation"""
        priority = 0
        
        # High risk = high priority
        if 'risk_score' in row:
            priority += row['risk_score'] * 0.4
        
        # Low health = high priority
        if 'health_score' in row:
            priority += (100 - row['health_score']) * 0.3
        
        # Low progress = high priority
        if 'progress' in row:
            priority += (6 - row['progress']) * 6  # Scale to 0-30
        
        return min(priority, 100)
    
    def _predict_completion_date(self, row: pd.Series) -> Optional[datetime]:
        """Predict completion date for a KPI"""
        if 'completion_percentage' not in row:
            return None
        
        completion = row.get('completion_percentage', 0)
        
        if completion >= 100:
            return datetime.now()
        
        if completion == 0:
            return None
        
        # Simple linear projection
        if 'last_updated' in row:
            try:
                last_updated = pd.to_datetime(row['last_updated'])
                days_elapsed = (datetime.now() - last_updated).days
                
                if days_elapsed > 0:
                    daily_rate = completion / days_elapsed
                    
                    if daily_rate > 0:
                        remaining = 100 - completion
                        days_to_complete = remaining / daily_rate
                        
                        return datetime.now() + timedelta(days=days_to_complete)
            except:
                pass
        
        return None
    
    def _calculate_prediction_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence level for predictions"""
        confidence = 50  # Base confidence
        
        # More data = higher confidence
        if len(data) >= 10:
            confidence += 20
        elif len(data) >= 5:
            confidence += 10
        
        # Recent updates = higher confidence
        if 'days_since_update' in data.columns:
            avg_days = data['days_since_update'].mean()
            if avg_days <= 7:
                confidence += 20
            elif avg_days <= 14:
                confidence += 10
        
        # Consistent progress = higher confidence
        if 'progress' in data.columns:
            progress_std = data['progress'].std()
            if progress_std < 1:
                confidence += 10
        
        return min(confidence, 100)
    
    def _identify_risk_factors(self, row: pd.Series) -> List[str]:
        """Identify specific risk factors for a KPI"""
        factors = []
        
        if row.get('status') == 'R':
            factors.append('status_red')
        
        if row.get('progress', 5) <= 2:
            factors.append('low_progress')
        
        if row.get('health_score', 100) < 50:
            factors.append('low_health')
        
        if row.get('days_since_update', 0) > 14:
            factors.append('stale_update')
        
        if row.get('completion_percentage', 100) < 30:
            factors.append('low_completion')
        
        return factors
    
    def _calculate_risk_trend(self, row: pd.Series) -> str:
        """Calculate risk trend direction"""
        # Simplified trend calculation
        if row.get('trend') == 'improving':
            return 'decreasing'
        elif row.get('trend') == 'declining':
            return 'increasing'
        else:
            return 'stable'