"""
AI Orchestrator - Combines OpenAI and Claude for Enhanced Intelligence
======================================================================
Uses both AI models for better insights, code generation, and analysis
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# OpenAI imports
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI not installed. Run: pip install openai")

# Anthropic Claude imports
try:
    import anthropic
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("Anthropic not installed. Run: pip install anthropic")

@dataclass
class AIResponse:
    """Structure for AI responses"""
    model: str
    response: str
    confidence: float
    metadata: Dict[str, Any]

class AIOrchestrator:
    """Orchestrates between OpenAI and Claude for optimal results"""
    
    def __init__(self):
        """Initialize AI clients"""
        self.openai_client = None
        self.claude_client = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Initialize OpenAI
        if OPENAI_AVAILABLE:
            openai_key = os.getenv('OPENAI_API_KEY')
            print(f"OpenAI Key found: {bool(openai_key)}, starts with: {openai_key[:10] if openai_key else 'None'}")
            if openai_key and openai_key != "your-openai-api-key":
                try:
                    self.openai_client = OpenAI(api_key=openai_key)
                    print("OpenAI initialized successfully")
                except Exception as e:
                    print(f"Error initializing OpenAI: {e}")
            else:
                print("Warning: OpenAI API key not found. Set OPENAI_API_KEY environment variable")
        
        # Initialize Claude
        if CLAUDE_AVAILABLE:
            claude_key = os.getenv('ANTHROPIC_API_KEY')
            print(f"Claude Key found: {bool(claude_key)}, starts with: {claude_key[:15] if claude_key else 'None'}")
            if claude_key and claude_key != "your-anthropic-api-key":
                try:
                    self.claude_client = Anthropic(api_key=claude_key)
                    print("Claude initialized successfully")
                except Exception as e:
                    print(f"Error initializing Claude: {e}")
            else:
                print("Warning: Claude API key not found. Set ANTHROPIC_API_KEY environment variable")
    
    def analyze_kpi_data(self, df: pd.DataFrame, mode: str = "both") -> Dict[str, Any]:
        """
        Analyze KPI data using selected AI model(s)
        
        Args:
            df: KPI dataframe
            mode: "openai", "claude", or "both"
        
        Returns:
            Analysis results from AI models
        """
        results = {}
        
        # Prepare data summary for AI
        data_summary = self._prepare_data_summary(df)
        
        if mode in ["openai", "both"] and self.openai_client:
            results['openai'] = self._analyze_with_openai(data_summary)
        
        if mode in ["claude", "both"] and self.claude_client:
            results['claude'] = self._analyze_with_claude(data_summary)
        
        if mode == "both" and len(results) == 2:
            results['combined'] = self._combine_analyses(results['openai'], results['claude'])
        
        return results
    
    def generate_dashboard_code(self, requirements: Dict[str, Any], framework: str = "streamlit", mode: str = "both") -> Dict[str, str]:
        """
        Generate dashboard code using AI models
        
        Args:
            requirements: Dashboard requirements and configuration
            framework: Target framework (streamlit, dash, etc.)
            mode: "openai", "claude", or "both"
        
        Returns:
            Generated code from each model
        """
        results = {}
        
        prompt = self._create_code_generation_prompt(requirements, framework)
        
        if mode in ["openai", "both"] and self.openai_client:
            results['openai_code'] = self._generate_with_openai(prompt)
        
        if mode in ["claude", "both"] and self.claude_client:
            results['claude_code'] = self._generate_with_claude(prompt)
        
        if mode == "both" and len(results) == 2:
            results['best_practices'] = self._merge_best_practices(
                results['openai_code'], 
                results['claude_code']
            )
        
        return results
    
    def generate_insights(self, df: pd.DataFrame, context: str = "") -> List[Dict[str, Any]]:
        """
        Generate insights using both AI models
        
        Args:
            df: KPI dataframe
            context: Additional context for insight generation
        
        Returns:
            List of insights from both models
        """
        insights = []
        
        # Prepare analysis request
        analysis_prompt = f"""
        Analyze this KPI data and provide actionable insights:
        
        Data Summary:
        - Total KPIs: {len(df)}
        - Columns: {', '.join(df.columns.tolist())}
        - Status distribution: {df['status'].value_counts().to_dict() if 'status' in df.columns else 'N/A'}
        
        Context: {context}
        
        Provide 5 key insights with priority levels (High/Medium/Low) and specific recommendations.
        """
        
        # Get insights from both models in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            
            if self.openai_client:
                futures.append(executor.submit(self._get_openai_insights, analysis_prompt))
            
            if self.claude_client:
                futures.append(executor.submit(self._get_claude_insights, analysis_prompt))
            
            for future in futures:
                try:
                    result = future.result(timeout=30)
                    insights.extend(result)
                except Exception as e:
                    print(f"Error getting insights: {e}")
        
        # Deduplicate and rank insights
        insights = self._rank_insights(insights)
        
        return insights
    
    def _prepare_data_summary(self, df: pd.DataFrame) -> str:
        """Prepare a summary of the dataframe for AI analysis"""
        summary = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'sample_data': df.head(5).to_dict()
        }
        
        if 'status' in df.columns:
            summary['status_distribution'] = df['status'].value_counts().to_dict()
        
        if 'health_score' in df.columns:
            summary['health_stats'] = {
                'mean': df['health_score'].mean(),
                'median': df['health_score'].median(),
                'std': df['health_score'].std()
            }
        
        return json.dumps(summary, default=str)
    
    def _analyze_with_openai(self, data_summary: str) -> Dict[str, Any]:
        """Analyze data using OpenAI"""
        if not self.openai_client:
            return {}
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a KPI analysis expert. Provide detailed insights and recommendations."},
                    {"role": "user", "content": f"Analyze this KPI data and provide insights:\n{data_summary}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'model': 'gpt-4-turbo',
                'confidence': 0.9
            }
        except Exception as e:
            print(f"OpenAI analysis error: {e}")
            return {}
    
    def _analyze_with_claude(self, data_summary: str) -> Dict[str, Any]:
        """Analyze data using Claude"""
        if not self.claude_client:
            return {}
        
        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[
                    {"role": "user", "content": f"Analyze this KPI data and provide insights:\n{data_summary}"}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return {
                'analysis': response.content[0].text,
                'model': 'claude-3-opus',
                'confidence': 0.9
            }
        except Exception as e:
            print(f"Claude analysis error: {e}")
            return {}
    
    def _create_code_generation_prompt(self, requirements: Dict[str, Any], framework: str) -> str:
        """Create prompt for code generation"""
        return f"""
        Generate a complete {framework} dashboard with the following requirements:
        
        Dashboard Name: {requirements.get('name', 'KPI Dashboard')}
        Type: {requirements.get('type', 'Standard KPI')}
        Update Frequency: {requirements.get('update_frequency', 'Daily')}
        
        Features to include:
        - KPI Fields: {', '.join(requirements.get('kpi_fields', []))}
        - Chart Types: {', '.join(requirements.get('chart_types', []))}
        - Theme: {requirements.get('theme', 'Light')}
        - Animations: {requirements.get('animations', True)}
        
        Requirements:
        1. Complete, runnable code
        2. Error handling
        3. Data validation
        4. Responsive design
        5. Export functionality
        6. Comments and documentation
        
        Generate production-ready code following best practices.
        """
    
    def _generate_with_openai(self, prompt: str) -> str:
        """Generate code using OpenAI"""
        if not self.openai_client:
            return "# OpenAI not available"
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert dashboard developer. Generate clean, efficient, production-ready code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI generation error: {e}")
            return f"# Error generating code with OpenAI: {e}"
    
    def _generate_with_claude(self, prompt: str) -> str:
        """Generate code using Claude"""
        if not self.claude_client:
            return "# Claude not available"
        
        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            return response.content[0].text
        except Exception as e:
            print(f"Claude generation error: {e}")
            return f"# Error generating code with Claude: {e}"
    
    def _get_openai_insights(self, prompt: str) -> List[Dict[str, Any]]:
        """Get insights from OpenAI"""
        if not self.openai_client:
            return []
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a KPI analysis expert. Provide insights in JSON format."},
                    {"role": "user", "content": prompt + "\n\nReturn as JSON array with fields: title, message, priority, recommendations"}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            insights_data = json.loads(response.choices[0].message.content)
            insights = insights_data.get('insights', [])
            
            # Add source
            for insight in insights:
                insight['source'] = 'openai'
            
            return insights
        except Exception as e:
            print(f"OpenAI insights error: {e}")
            return []
    
    def _get_claude_insights(self, prompt: str) -> List[Dict[str, Any]]:
        """Get insights from Claude"""
        if not self.claude_client:
            return []
        
        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[
                    {"role": "user", "content": prompt + "\n\nReturn as JSON array with fields: title, message, priority, recommendations"}
                ],
                max_tokens=1000
            )
            
            # Parse JSON from response
            content = response.content[0].text
            # Extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                
                # Add source
                for insight in insights:
                    insight['source'] = 'claude'
                
                return insights
        except Exception as e:
            print(f"Claude insights error: {e}")
            return []
        
        return []
    
    def _combine_analyses(self, openai_result: Dict, claude_result: Dict) -> Dict[str, Any]:
        """Combine analyses from both models"""
        return {
            'consensus': self._find_consensus(openai_result, claude_result),
            'openai_unique': openai_result,
            'claude_unique': claude_result,
            'confidence': (openai_result.get('confidence', 0) + claude_result.get('confidence', 0)) / 2
        }
    
    def _merge_best_practices(self, openai_code: str, claude_code: str) -> str:
        """Merge best practices from both code generations"""
        # This is a simplified merge - in production, you'd use more sophisticated merging
        merged = f"""
# Dashboard generated using best practices from OpenAI and Claude

# ============== OpenAI Version ==============
{openai_code}

# ============== Claude Version ==============
{claude_code}

# ============== Merged Best Practices ==============
# Use the best parts from each version above
"""
        return merged
    
    def _rank_insights(self, insights: List[Dict]) -> List[Dict]:
        """Rank and deduplicate insights"""
        # Simple deduplication based on title similarity
        unique_insights = []
        seen_titles = set()
        
        for insight in insights:
            title = insight.get('title', '').lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_insights.append(insight)
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        unique_insights.sort(
            key=lambda x: priority_order.get(x.get('priority', '').lower(), 3)
        )
        
        return unique_insights[:10]  # Return top 10
    
    def _find_consensus(self, result1: Dict, result2: Dict) -> str:
        """Find consensus between two analyses"""
        try:
            analysis1 = result1.get('analysis', '')
            analysis2 = result2.get('analysis', '')
            
            # Extract key points from both analyses
            key_points = []
            
            # Look for common themes
            common_words = ['performance', 'risk', 'improvement', 'trend', 'critical', 'success']
            for word in common_words:
                if word.lower() in analysis1.lower() and word.lower() in analysis2.lower():
                    key_points.append(f"Both models identify {word} as a key factor")
            
            if key_points:
                return "AI Consensus: " + "; ".join(key_points[:3])
            else:
                return "Both AIs have analyzed the data from complementary perspectives, providing comprehensive insights."
        except:
            return "Both models have completed their analysis. Review individual insights above."
    
    def compare_models(self, task: str, data: Any) -> Dict[str, Any]:
        """
        Compare outputs from both models for a given task
        
        Args:
            task: Type of task (analysis, generation, etc.)
            data: Input data for the task
        
        Returns:
            Comparison results
        """
        results = {
            'task': task,
            'models': []
        }
        
        # Run task on both models
        if task == "analysis":
            openai_result = self._analyze_with_openai(data) if self.openai_client else None
            claude_result = self._analyze_with_claude(data) if self.claude_client else None
            
            if openai_result:
                results['models'].append({
                    'name': 'OpenAI GPT-4',
                    'result': openai_result,
                    'response_time': 0  # Add timing in production
                })
            
            if claude_result:
                results['models'].append({
                    'name': 'Claude 3 Opus',
                    'result': claude_result,
                    'response_time': 0  # Add timing in production
                })
        
        return results
    
    def get_available_models(self) -> Dict[str, bool]:
        """Check which models are available"""
        return {
            'openai': self.openai_client is not None,
            'claude': self.claude_client is not None,
            'both_available': self.openai_client is not None and self.claude_client is not None
        }

# Singleton instance
ai_orchestrator = AIOrchestrator()

def get_orchestrator() -> AIOrchestrator:
    """Get the AI orchestrator instance"""
    return ai_orchestrator