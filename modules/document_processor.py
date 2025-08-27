"""
Document Processor Module
=========================
Processes various document types to extract KPI information.
Supports SOW, Requirements, Word docs, PDFs, and more.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import json
from typing import Dict, List, Optional, Tuple, Any
import io
from pathlib import Path

class DocumentProcessor:
    """Advanced document processing for KPI extraction"""
    
    def __init__(self):
        self.kpi_patterns = {
            'kpi_indicators': [
                r'(?i)kpi[:\s]+([^.\n]+)',
                r'(?i)metric[:\s]+([^.\n]+)',
                r'(?i)measure[:\s]+([^.\n]+)',
                r'(?i)indicator[:\s]+([^.\n]+)',
                r'(?i)performance indicator[:\s]+([^.\n]+)',
                r'(?i)success metric[:\s]+([^.\n]+)'
            ],
            'goal_patterns': [
                r'(?i)goal[:\s]+([^.\n]+)',
                r'(?i)objective[:\s]+([^.\n]+)',
                r'(?i)outcome[:\s]+([^.\n]+)',
                r'(?i)target[:\s]+([^.\n]+)',
                r'(?i)deliverable[:\s]+([^.\n]+)'
            ],
            'project_patterns': [
                r'(?i)project[:\s]+([^.\n]+)',
                r'(?i)program[:\s]+([^.\n]+)',
                r'(?i)initiative[:\s]+([^.\n]+)',
                r'(?i)workstream[:\s]+([^.\n]+)'
            ],
            'measurement_patterns': [
                r'(\d+)\s*(?:/|of)\s*(\d+)',
                r'(\d+)%',
                r'(\d+\.?\d*)\s*(hours?|days?|weeks?|months?)',
                r'(?i)increase.*?(\d+)%',
                r'(?i)reduce.*?(\d+)%',
                r'(?i)achieve.*?(\d+)'
            ]
        }
        
        self.progress_mapping = {
            '1. Limited engagement; critical actions not initiated': 1,
            '2. Targets unmet; requires urgent support and redirection': 2,
            '3. Partial progress; improvement plan underway': 3,
            '4. Steady development; more consistency required': 4,
            '5. Strong momentum; measurable impact aligned with goals': 5
        }
    
    def process_excel(self, file) -> pd.DataFrame:
        """Process Excel file and extract KPI data"""
        try:
            # Read Excel file
            if hasattr(file, 'read'):
                excel_file = pd.ExcelFile(file)
            else:
                excel_file = pd.ExcelFile(str(file))
            
            all_data = []
            
            # Process each sheet
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name)
                
                if df.empty:
                    continue
                
                # Determine sheet type and process accordingly
                if self._is_impact_kpi_sheet(sheet_name, df):
                    processed = self._process_impact_kpis(df)
                elif self._is_project_mgmt_sheet(sheet_name, df):
                    processed = self._process_project_mgmt_kpis(df)
                elif self._is_performance_sheet(sheet_name, df):
                    processed = self._process_performance_kpis(df)
                else:
                    # Try generic processing
                    processed = self._process_generic_sheet(df)
                
                if not processed.empty:
                    processed['source_sheet'] = sheet_name
                    all_data.append(processed)
            
            # Combine all processed data
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                return self._standardize_dataframe(combined_df)
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error processing Excel: {str(e)}")
            return pd.DataFrame()
    
    def process_sow(self, file) -> pd.DataFrame:
        """Process Statement of Work document"""
        content = self._read_document(file)
        return self.process_sow_text(content)
    
    def process_sow_text(self, text: str) -> pd.DataFrame:
        """Extract KPIs from SOW text"""
        kpis = []
        
        # Split into sections
        sections = self._split_into_sections(text)
        
        current_project = "TBD"
        current_goal = "TBD"
        
        for section_title, section_content in sections.items():
            # Extract project name from section
            project_match = self._extract_with_patterns(
                section_content, 
                self.kpi_patterns['project_patterns']
            )
            if project_match:
                current_project = project_match
            
            # Extract goals
            goal_matches = self._extract_all_with_patterns(
                section_content,
                self.kpi_patterns['goal_patterns']
            )
            
            for goal in goal_matches:
                if goal:
                    current_goal = goal
                
                # Extract KPIs for this goal
                kpi_matches = self._extract_all_with_patterns(
                    section_content,
                    self.kpi_patterns['kpi_indicators']
                )
                
                for kpi in kpi_matches:
                    if kpi:
                        # Extract measurement if available
                        measurement = self._extract_measurement(section_content)
                        
                        kpi_record = {
                            'kpi_name': kpi[:200],  # Limit length
                            'project': current_project,
                            'goal': current_goal,
                            'description': f"Extracted from SOW: {section_title}",
                            'measurement': measurement.get('text', 'TBD'),
                            'target_value': measurement.get('target', 100.0),
                            'actual_value': measurement.get('actual', 0.0),
                            'owner': 'TBD',
                            'status': 'R',  # Red/Not started by default
                            'progress': 1,
                            'last_updated': datetime.now(),
                            'source': 'SOW',
                            'section': section_title
                        }
                        kpis.append(kpi_record)
        
        # If no KPIs found, create template based on sections
        if not kpis:
            kpis = self._create_template_kpis_from_text(text, 'SOW')
        
        df = pd.DataFrame(kpis)
        return self._standardize_dataframe(df)
    
    def process_requirements(self, file) -> pd.DataFrame:
        """Process requirements document"""
        content = self._read_document(file)
        return self.process_requirements_text(content)
    
    def process_requirements_text(self, text: str) -> pd.DataFrame:
        """Extract KPIs from requirements text"""
        kpis = []
        
        # Parse requirements
        requirements = self._parse_requirements(text)
        
        for req in requirements:
            # Check if requirement contains measurable criteria
            if self._is_measurable_requirement(req):
                kpi = self._convert_requirement_to_kpi(req)
                kpis.append(kpi)
        
        df = pd.DataFrame(kpis)
        return self._standardize_dataframe(df)
    
    def process_charter(self, file) -> pd.DataFrame:
        """Process project charter document"""
        content = self._read_document(file)
        return self._process_charter_text(content)
    
    def _process_charter_text(self, text: str) -> pd.DataFrame:
        """Extract KPIs from project charter"""
        kpis = []
        
        # Extract project information
        project_info = self._extract_project_info(text)
        
        # Extract success criteria as KPIs
        success_criteria = self._extract_success_criteria(text)
        
        for criterion in success_criteria:
            kpi = {
                'kpi_name': criterion['name'],
                'project': project_info.get('name', 'TBD'),
                'goal': project_info.get('objective', 'TBD'),
                'description': criterion.get('description', ''),
                'target_value': criterion.get('target', 100.0),
                'actual_value': 0.0,
                'owner': project_info.get('manager', 'TBD'),
                'status': 'R',
                'progress': 1,
                'last_updated': datetime.now(),
                'source': 'Project Charter'
            }
            kpis.append(kpi)
        
        df = pd.DataFrame(kpis)
        return self._standardize_dataframe(df)
    
    def process_custom_document(self, file) -> pd.DataFrame:
        """Process custom document type"""
        content = self._read_document(file)
        return self.process_text(content)
    
    def process_text(self, text: str) -> pd.DataFrame:
        """Generic text processing for KPI extraction"""
        kpis = []
        
        # Try to identify document structure
        lines = text.split('\n')
        
        current_context = {
            'project': 'TBD',
            'goal': 'TBD',
            'section': 'General'
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for project indicators
            project = self._extract_with_patterns(line, self.kpi_patterns['project_patterns'])
            if project:
                current_context['project'] = project
            
            # Check for goals
            goal = self._extract_with_patterns(line, self.kpi_patterns['goal_patterns'])
            if goal:
                current_context['goal'] = goal
            
            # Check for KPIs
            kpi = self._extract_with_patterns(line, self.kpi_patterns['kpi_indicators'])
            if kpi:
                measurement = self._extract_measurement(line)
                
                kpi_record = {
                    'kpi_name': kpi,
                    'project': current_context['project'],
                    'goal': current_context['goal'],
                    'description': f"From section: {current_context['section']}",
                    'target_value': measurement.get('target', 100.0),
                    'actual_value': measurement.get('actual', 0.0),
                    'measurement': measurement.get('text', 'TBD'),
                    'owner': 'TBD',
                    'status': 'R',
                    'progress': 1,
                    'last_updated': datetime.now(),
                    'source': 'Custom Document'
                }
                kpis.append(kpi_record)
        
        # Create template if no KPIs found
        if not kpis:
            kpis = self._create_template_kpis_from_text(text, 'Custom')
        
        df = pd.DataFrame(kpis)
        return self._standardize_dataframe(df)
    
    def preview_excel_structure(self, file) -> Dict:
        """Preview Excel file structure without full processing"""
        try:
            if hasattr(file, 'read'):
                excel_file = pd.ExcelFile(file)
            else:
                excel_file = pd.ExcelFile(str(file))
            
            structure = {
                'sheets': {},
                'total_sheets': len(excel_file.sheet_names)
            }
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name, nrows=5)  # Preview first 5 rows
                
                structure['sheets'][sheet_name] = {
                    'columns': df.columns.tolist(),
                    'rows': len(pd.read_excel(excel_file, sheet_name)),
                    'sample_data': df.head(2).to_dict('records')
                }
            
            return structure
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_sample_data(self, sample_type: str) -> pd.DataFrame:
        """Generate sample KPI data based on type"""
        
        if sample_type == "Youth Health Program":
            kpis = [
                {
                    'kpi_name': 'Number of youth enrolled in health education program',
                    'project': 'Youth Health Initiative',
                    'goal': 'Increase youth health awareness and engagement',
                    'description': 'Track enrollment and participation in health education sessions',
                    'target_value': 500.0,
                    'actual_value': 387.0,
                    'progress': 4,
                    'status': 'G',
                    'owner': 'Program Director',
                    'last_updated': datetime.now() - timedelta(days=3),
                    'health_score': 85.0,
                    'risk_level': 'Low'
                },
                {
                    'kpi_name': 'STI prevention knowledge improvement rate',
                    'project': 'Youth Health Initiative',
                    'goal': 'Reduce STI rates among youth',
                    'description': 'Measure knowledge gain through pre/post assessments',
                    'target_value': 80.0,
                    'actual_value': 72.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'Health Educator',
                    'last_updated': datetime.now() - timedelta(days=7),
                    'health_score': 70.0,
                    'risk_level': 'Medium'
                },
                {
                    'kpi_name': 'Peer educator certification completion',
                    'project': 'Peer Education Program',
                    'goal': 'Build peer education capacity',
                    'description': 'Number of youth completing peer educator certification',
                    'target_value': 50.0,
                    'actual_value': 22.0,
                    'progress': 2,
                    'status': 'R',
                    'owner': 'Training Coordinator',
                    'last_updated': datetime.now() - timedelta(days=14),
                    'health_score': 45.0,
                    'risk_level': 'High'
                },
                {
                    'kpi_name': 'Community health fair attendance',
                    'project': 'Community Outreach',
                    'goal': 'Increase community engagement',
                    'description': 'Number of community members reached through health fairs',
                    'target_value': 1000.0,
                    'actual_value': 1250.0,
                    'progress': 5,
                    'status': 'G',
                    'owner': 'Outreach Manager',
                    'last_updated': datetime.now() - timedelta(days=1),
                    'health_score': 95.0,
                    'risk_level': 'Low'
                },
                {
                    'kpi_name': 'Digital health content engagement rate',
                    'project': 'Digital Health Campaign',
                    'goal': 'Leverage digital platforms for health education',
                    'description': 'Engagement metrics for social media health content',
                    'target_value': 25000.0,
                    'actual_value': 18500.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'Digital Marketing Lead',
                    'last_updated': datetime.now() - timedelta(days=5),
                    'health_score': 65.0,
                    'risk_level': 'Medium'
                }
            ]
        
        elif sample_type == "Digital Transformation":
            kpis = [
                {
                    'kpi_name': 'Legacy system migration completion',
                    'project': 'Digital Transformation Initiative',
                    'goal': 'Modernize IT infrastructure',
                    'description': 'Percentage of legacy systems successfully migrated to cloud',
                    'target_value': 100.0,
                    'actual_value': 65.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'IT Director',
                    'last_updated': datetime.now() - timedelta(days=2),
                    'health_score': 70.0,
                    'risk_level': 'Medium'
                },
                {
                    'kpi_name': 'Employee digital skills training completion',
                    'project': 'Digital Skills Program',
                    'goal': 'Upskill workforce for digital tools',
                    'description': 'Percentage of employees completing digital skills training',
                    'target_value': 90.0,
                    'actual_value': 78.0,
                    'progress': 4,
                    'status': 'G',
                    'owner': 'HR Training Manager',
                    'last_updated': datetime.now() - timedelta(days=4),
                    'health_score': 82.0,
                    'risk_level': 'Low'
                },
                {
                    'kpi_name': 'Customer portal adoption rate',
                    'project': 'Customer Experience Enhancement',
                    'goal': 'Improve customer self-service capabilities',
                    'description': 'Percentage of customers using new digital portal',
                    'target_value': 60.0,
                    'actual_value': 45.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'Customer Experience Lead',
                    'last_updated': datetime.now() - timedelta(days=6),
                    'health_score': 68.0,
                    'risk_level': 'Medium'
                }
            ]
        
        elif sample_type == "Sustainability Initiative":
            kpis = [
                {
                    'kpi_name': 'Carbon footprint reduction',
                    'project': 'Green Operations',
                    'goal': 'Achieve carbon neutrality by 2025',
                    'description': 'Percentage reduction in carbon emissions from baseline',
                    'target_value': 30.0,
                    'actual_value': 22.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'Sustainability Officer',
                    'last_updated': datetime.now() - timedelta(days=10),
                    'health_score': 73.0,
                    'risk_level': 'Medium'
                },
                {
                    'kpi_name': 'Renewable energy adoption',
                    'project': 'Energy Transition',
                    'goal': 'Transition to 100% renewable energy',
                    'description': 'Percentage of energy from renewable sources',
                    'target_value': 50.0,
                    'actual_value': 38.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'Facilities Manager',
                    'last_updated': datetime.now() - timedelta(days=8),
                    'health_score': 70.0,
                    'risk_level': 'Medium'
                },
                {
                    'kpi_name': 'Waste diversion rate',
                    'project': 'Zero Waste Program',
                    'goal': 'Achieve 90% waste diversion from landfills',
                    'description': 'Percentage of waste diverted through recycling and composting',
                    'target_value': 90.0,
                    'actual_value': 82.0,
                    'progress': 4,
                    'status': 'G',
                    'owner': 'Environmental Manager',
                    'last_updated': datetime.now() - timedelta(days=1),
                    'health_score': 88.0,
                    'risk_level': 'Low'
                }
            ]
        
        else:  # Custom KPIs
            kpis = [
                {
                    'kpi_name': 'Custom KPI 1 - Performance Metric',
                    'project': 'Custom Project Alpha',
                    'goal': 'Achieve operational excellence',
                    'description': 'Track key performance indicator for operations',
                    'target_value': 100.0,
                    'actual_value': 75.0,
                    'progress': 3,
                    'status': 'Y',
                    'owner': 'Operations Manager',
                    'last_updated': datetime.now() - timedelta(days=5),
                    'health_score': 75.0,
                    'risk_level': 'Medium'
                },
                {
                    'kpi_name': 'Custom KPI 2 - Quality Score',
                    'project': 'Quality Improvement',
                    'goal': 'Enhance product quality',
                    'description': 'Quality score based on defect rates and customer feedback',
                    'target_value': 95.0,
                    'actual_value': 92.0,
                    'progress': 4,
                    'status': 'G',
                    'owner': 'Quality Manager',
                    'last_updated': datetime.now() - timedelta(days=2),
                    'health_score': 90.0,
                    'risk_level': 'Low'
                }
            ]
        
        df = pd.DataFrame(kpis)
        return self._standardize_dataframe(df)
    
    # Helper methods
    def _read_document(self, file) -> str:
        """Read document content from various file types"""
        try:
            if hasattr(file, 'read'):
                # Handle uploaded file objects
                content = file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')
                return content
            else:
                # Handle file paths
                path = Path(file)
                
                if path.suffix == '.pdf':
                    return self._read_pdf(path)
                elif path.suffix == '.docx':
                    return self._read_docx(path)
                else:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
                        
        except Exception as e:
            print(f"Error reading document: {str(e)}")
            return ""
    
    def _read_pdf(self, path: Path) -> str:
        """Read PDF content (requires PyPDF2 or similar)"""
        # Simplified - would need actual PDF library
        return "PDF content extraction not implemented"
    
    def _read_docx(self, path: Path) -> str:
        """Read Word document content (requires python-docx)"""
        # Simplified - would need actual docx library
        return "DOCX content extraction not implemented"
    
    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split text into logical sections"""
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        # Common section headers
        section_patterns = [
            r'^\d+\.?\s+(.+)$',  # Numbered sections
            r'^[A-Z][A-Z\s]+$',  # All caps headers
            r'^#+\s+(.+)$',  # Markdown headers
            r'^(.+):$'  # Colon-ended headers
        ]
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check if this is a section header
            is_header = False
            for pattern in section_patterns:
                match = re.match(pattern, line)
                if match and len(line) < 100:  # Reasonable header length
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line
                    current_content = []
                    is_header = True
                    break
            
            if not is_header:
                current_content.append(line)
        
        # Add last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _extract_with_patterns(self, text: str, patterns: List[str]) -> Optional[str]:
        """Extract first match using patterns"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_all_with_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """Extract all matches using patterns"""
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend([m.strip() for m in found if isinstance(m, str)])
        return matches
    
    def _extract_measurement(self, text: str) -> Dict:
        """Extract measurement values from text"""
        result = {
            'text': 'TBD',
            'target': 100.0,
            'actual': 0.0
        }
        
        # Try to find measurement patterns
        for pattern in self.kpi_patterns['measurement_patterns']:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                
                if len(groups) == 2:  # Format: X/Y or X of Y
                    try:
                        result['actual'] = float(groups[0])
                        result['target'] = float(groups[1])
                        result['text'] = f"{groups[0]}/{groups[1]}"
                    except:
                        pass
                elif len(groups) == 1:  # Format: X% or single number
                    try:
                        value = float(groups[0])
                        if '%' in text:
                            result['actual'] = value
                            result['target'] = 100.0
                            result['text'] = f"{value}%"
                        else:
                            result['target'] = value
                            result['text'] = f"Target: {value}"
                    except:
                        pass
                break
        
        return result
    
    def _is_impact_kpi_sheet(self, sheet_name: str, df: pd.DataFrame) -> bool:
        """Check if sheet contains impact KPIs"""
        name_check = any(term in sheet_name.lower() for term in ['impact', 'kpi', 'logic'])
        
        if name_check:
            return True
        
        # Check column names
        impact_columns = ['impact kpi', 'enter kpi measurement', 'what it measures']
        df_columns_lower = [col.lower() for col in df.columns]
        
        return sum(1 for col in impact_columns if col in df_columns_lower) >= 2
    
    def _is_project_mgmt_sheet(self, sheet_name: str, df: pd.DataFrame) -> bool:
        """Check if sheet contains project management KPIs"""
        name_check = 'project management' in sheet_name.lower()
        
        if name_check:
            return True
        
        # Check column names
        mgmt_columns = ['target outcomes', 'actions taken', 'kpi measurement']
        df_columns_lower = [col.lower() for col in df.columns]
        
        return sum(1 for col in mgmt_columns if any(col in c for c in df_columns_lower)) >= 2
    
    def _is_performance_sheet(self, sheet_name: str, df: pd.DataFrame) -> bool:
        """Check if sheet contains performance data"""
        return 'performance' in sheet_name.lower()
    
    def _process_impact_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process impact KPIs sheet"""
        processed = pd.DataFrame()
        
        # Column mapping
        column_map = {
            'kpi_name': ['Impact KPI', 'KPI', 'Key Performance Indicator'],
            'project': ['Project', 'Program', 'Initiative'],
            'goal': ['Goal', 'Objective', 'Goals'],
            'measurement': ['Enter KPI Measurement', 'KPI Measurement', 'Measurement'],
            'description': ['What It Measures', 'Description', 'What This Measures'],
            'activities': ['Log Activities Done/Needed to Complete KPI', 'Activities', 'Actions'],
            'barriers': ['Key Barrier/Needs', 'Barriers', 'Challenges'],
            'owner': ['Owner', 'Responsible Person', 'Assignee'],
            'successes': ['Key Success', 'Successes', 'Achievements'],
            'progress': ['Progress', 'Progress Level'],
            'status': ['Status', 'Current Status'],
            'last_updated': ['Last Updated', 'Last Update', 'Date Updated']
        }
        
        # Map columns
        for target, sources in column_map.items():
            for source in sources:
                if source in df.columns:
                    processed[target] = df[source]
                    break
        
        # Parse measurements
        if 'measurement' in processed.columns:
            measurements = processed['measurement'].apply(self._parse_measurement_value)
            processed['target_value'] = measurements.apply(lambda x: x[1])
            processed['actual_value'] = measurements.apply(lambda x: x[0])
        
        # Process progress
        if 'progress' in processed.columns:
            processed['progress'] = processed['progress'].apply(self._normalize_progress)
        
        return processed
    
    def _process_project_mgmt_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process project management KPIs"""
        processed = pd.DataFrame()
        
        # Similar column mapping for project management
        column_map = {
            'kpi_name': ['Target Outcomes/ KPI', 'Target Outcomes', 'KPI'],
            'project': ['Project', 'Program'],
            'goal': ['Goals', 'Goal'],
            'measurement': ['KPI Measurement', 'Measurement'],
            'activities': ['Actions Taken', 'Activities'],
            'barriers': ['Key Barrier/Needs', 'Barriers'],
            'owner': ['Owner', 'Responsible'],
            'successes': ['Key Successes', 'Successes'],
            'progress': ['Progress'],
            'status': ['Status'],
            'last_updated': ['Last Updated']
        }
        
        # Map columns
        for target, sources in column_map.items():
            for source in sources:
                if source in df.columns:
                    processed[target] = df[source]
                    break
        
        processed['kpi_type'] = 'Project Management'
        
        return processed
    
    def _process_performance_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process performance KPIs"""
        # Similar to other processing methods
        return self._process_generic_sheet(df)
    
    def _process_generic_sheet(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generic sheet processing"""
        processed = pd.DataFrame()
        
        # Try to identify KPI-related columns
        for col in df.columns:
            col_lower = col.lower()
            
            if any(term in col_lower for term in ['kpi', 'metric', 'indicator', 'measure']):
                processed['kpi_name'] = df[col]
            elif any(term in col_lower for term in ['project', 'program']):
                processed['project'] = df[col]
            elif any(term in col_lower for term in ['goal', 'objective']):
                processed['goal'] = df[col]
            elif any(term in col_lower for term in ['owner', 'responsible']):
                processed['owner'] = df[col]
            elif any(term in col_lower for term in ['status']):
                processed['status'] = df[col]
            elif any(term in col_lower for term in ['progress']):
                processed['progress'] = df[col]
            elif any(term in col_lower for term in ['updated', 'date']):
                processed['last_updated'] = df[col]
        
        return processed
    
    def _parse_measurement_value(self, measurement) -> Tuple[float, float]:
        """Parse measurement value into actual and target"""
        if pd.isna(measurement):
            return (0.0, 100.0)
        
        measurement_str = str(measurement).strip()
        
        # Try different formats
        if '/' in measurement_str:
            try:
                parts = measurement_str.split('/')
                actual = float(parts[0].strip())
                target = float(parts[1].strip())
                return (actual, target)
            except:
                pass
        
        if '%' in measurement_str:
            try:
                value = float(measurement_str.replace('%', '').strip())
                return (value, 100.0)
            except:
                pass
        
        # Try as single number
        try:
            value = float(measurement_str)
            return (value, 100.0)
        except:
            pass
        
        return (0.0, 100.0)
    
    def _normalize_progress(self, progress_value) -> int:
        """Normalize progress to 1-5 scale"""
        if pd.isna(progress_value):
            return 3
        
        # If it's already a number
        if isinstance(progress_value, (int, float)):
            return max(1, min(5, int(progress_value)))
        
        # If it's text, try to extract or map
        progress_str = str(progress_value).strip()
        
        # Check against known mapping
        if progress_str in self.progress_mapping:
            return self.progress_mapping[progress_str]
        
        # Try to extract number
        match = re.search(r'(\d+)', progress_str)
        if match:
            return max(1, min(5, int(match.group(1))))
        
        return 3  # Default to middle
    
    def _parse_requirements(self, text: str) -> List[Dict]:
        """Parse requirements from text"""
        requirements = []
        
        # Split by common requirement patterns
        req_patterns = [
            r'(?i)(?:req|requirement)[\s#]*(\d+[\.\d]*)[:\s]+([^.\n]+)',
            r'(?i)(?:the system shall|shall|must|should)[:\s]+([^.\n]+)',
            r'(?i)(?:as a|i want|so that)[:\s]+([^.\n]+)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    req_text = match[-1] if match else ""
                else:
                    req_text = match
                
                if req_text:
                    requirements.append({
                        'text': req_text,
                        'type': 'functional' if 'shall' in text.lower() else 'user_story'
                    })
        
        return requirements
    
    def _is_measurable_requirement(self, req: Dict) -> bool:
        """Check if requirement contains measurable criteria"""
        measurable_keywords = [
            'percent', '%', 'number', 'count', 'rate', 'ratio',
            'increase', 'decrease', 'reduce', 'improve', 'achieve',
            'within', 'less than', 'greater than', 'at least'
        ]
        
        req_text = req.get('text', '').lower()
        return any(keyword in req_text for keyword in measurable_keywords)
    
    def _convert_requirement_to_kpi(self, req: Dict) -> Dict:
        """Convert requirement to KPI format"""
        req_text = req.get('text', '')
        
        # Extract measurement if present
        measurement = self._extract_measurement(req_text)
        
        return {
            'kpi_name': f"Requirement: {req_text[:100]}",
            'project': 'Requirements Implementation',
            'goal': 'Meet system requirements',
            'description': req_text,
            'target_value': measurement.get('target', 100.0),
            'actual_value': measurement.get('actual', 0.0),
            'measurement': measurement.get('text', 'TBD'),
            'owner': 'TBD',
            'status': 'R',
            'progress': 1,
            'last_updated': datetime.now(),
            'source': 'Requirements Document',
            'requirement_type': req.get('type', 'functional')
        }
    
    def _extract_project_info(self, text: str) -> Dict:
        """Extract project information from charter"""
        info = {}
        
        # Project name
        name_match = re.search(r'(?i)project\s+name[:\s]+([^.\n]+)', text)
        if name_match:
            info['name'] = name_match.group(1).strip()
        
        # Project manager
        mgr_match = re.search(r'(?i)project\s+manager[:\s]+([^.\n]+)', text)
        if mgr_match:
            info['manager'] = mgr_match.group(1).strip()
        
        # Objective
        obj_match = re.search(r'(?i)(?:objective|goal)[:\s]+([^.\n]+)', text)
        if obj_match:
            info['objective'] = obj_match.group(1).strip()
        
        return info
    
    def _extract_success_criteria(self, text: str) -> List[Dict]:
        """Extract success criteria from charter"""
        criteria = []
        
        # Find success criteria section
        success_section = re.search(
            r'(?i)success\s+criteria[:\s]+(.+?)(?:\n\n|\Z)',
            text,
            re.DOTALL
        )
        
        if success_section:
            criteria_text = success_section.group(1)
            
            # Split into individual criteria
            lines = criteria_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract measurement if present
                    measurement = self._extract_measurement(line)
                    
                    criteria.append({
                        'name': line[:100],
                        'description': line,
                        'target': measurement.get('target', 100.0)
                    })
        
        return criteria
    
    def _create_template_kpis_from_text(self, text: str, source_type: str) -> List[Dict]:
        """Create template KPIs when none found in text"""
        templates = []
        
        # Extract any structure we can find
        sections = self._split_into_sections(text)
        
        # Create at least one template KPI per section
        for section_title in sections.keys():
            template = {
                'kpi_name': f"KPI for {section_title[:50]}",
                'project': f"{source_type} Project",
                'goal': f"Achieve objectives in {section_title}",
                'description': f"Template KPI extracted from {source_type} section: {section_title}",
                'target_value': 100.0,
                'actual_value': 0.0,
                'measurement': 'TBD - Define measurement criteria',
                'owner': 'TBD',
                'status': 'R',
                'progress': 1,
                'last_updated': datetime.now(),
                'source': source_type,
                'section': section_title,
                'needs_definition': True
            }
            templates.append(template)
        
        # Ensure at least one template
        if not templates:
            templates.append({
                'kpi_name': f"Template KPI from {source_type}",
                'project': f"{source_type} Project",
                'goal': 'Define project goals',
                'description': f"Template KPI - needs customization based on {source_type} content",
                'target_value': 100.0,
                'actual_value': 0.0,
                'measurement': 'TBD',
                'owner': 'TBD',
                'status': 'R',
                'progress': 1,
                'last_updated': datetime.now(),
                'source': source_type,
                'needs_definition': True
            })
        
        return templates
    
    def _standardize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize dataframe columns and data types"""
        if df.empty:
            return df
        
        # Standard column names
        standard_columns = {
            'kpi_name': 'KPI Name',
            'project': 'Project',
            'goal': 'Goal',
            'description': 'Description',
            'target_value': 0.0,
            'actual_value': 0.0,
            'measurement': 'TBD',
            'owner': 'TBD',
            'status': 'R',
            'progress': 1,
            'last_updated': datetime.now(),
            'health_score': 0.0,
            'risk_level': 'High',
            'activities': '',
            'barriers': '',
            'successes': '',
            'source': 'Document',
            'kpi_type': 'General'
        }
        
        # Ensure all standard columns exist
        for col, default in standard_columns.items():
            if col not in df.columns:
                df[col] = default
        
        # Ensure correct data types
        numeric_columns = ['target_value', 'actual_value', 'progress', 'health_score']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Ensure progress is 1-5
        if 'progress' in df.columns:
            df['progress'] = df['progress'].clip(1, 5).astype(int)
        
        # Ensure status is valid
        if 'status' in df.columns:
            valid_statuses = ['G', 'Y', 'R']
            df['status'] = df['status'].apply(
                lambda x: x if x in valid_statuses else 'R'
            )
        
        # Ensure dates are datetime
        if 'last_updated' in df.columns:
            df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
            df['last_updated'].fillna(datetime.now(), inplace=True)
        
        # Fill NaN values in text columns
        text_columns = ['kpi_name', 'project', 'goal', 'description', 'owner', 
                       'measurement', 'activities', 'barriers', 'successes']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('TBD')
        
        return df