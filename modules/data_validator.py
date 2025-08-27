"""
Data Validator Module
=====================
Provides comprehensive data validation and cleaning for KPI data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

class DataValidator:
    """Data validation and cleaning for KPI data"""
    
    def __init__(self):
        self.required_columns = [
            'kpi_name',
            'project',
            'status',
            'owner',
            'last_updated'
        ]
        
        self.optional_columns = [
            'goal',
            'description',
            'target_value',
            'actual_value',
            'progress',
            'health_score',
            'risk_score',
            'measurement',
            'activities',
            'barriers',
            'successes'
        ]
        
        self.column_types = {
            'kpi_name': str,
            'project': str,
            'goal': str,
            'description': str,
            'owner': str,
            'status': str,
            'progress': int,
            'target_value': float,
            'actual_value': float,
            'health_score': float,
            'risk_score': float,
            'last_updated': 'datetime'
        }
        
        self.valid_statuses = ['G', 'Y', 'R']
        self.valid_progress = range(1, 6)  # 1-5
    
    def validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Comprehensive dataframe validation and cleaning"""
        if df.empty:
            return self._create_empty_dataframe()
        
        # Create a copy to avoid modifying original
        validated_df = df.copy()
        
        # Ensure required columns exist
        validated_df = self._ensure_required_columns(validated_df)
        
        # Clean and validate each column
        validated_df = self._validate_columns(validated_df)
        
        # Remove duplicates
        validated_df = self._remove_duplicates(validated_df)
        
        # Fill missing values
        validated_df = self._fill_missing_values(validated_df)
        
        # Validate data types
        validated_df = self._validate_data_types(validated_df)
        
        # Validate value ranges
        validated_df = self._validate_value_ranges(validated_df)
        
        # Add calculated fields
        validated_df = self._add_calculated_fields(validated_df)
        
        # Final validation check
        validation_report = self._generate_validation_report(validated_df)
        
        return validated_df
    
    def validate_kpi_record(self, record: Dict) -> Tuple[bool, List[str]]:
        """Validate a single KPI record"""
        errors = []
        
        # Check required fields
        for field in self.required_columns:
            if field not in record or not record[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate status
        if 'status' in record and record['status'] not in self.valid_statuses:
            errors.append(f"Invalid status: {record['status']}. Must be G, Y, or R")
        
        # Validate progress
        if 'progress' in record:
            try:
                progress = int(record['progress'])
                if progress not in self.valid_progress:
                    errors.append(f"Invalid progress: {progress}. Must be 1-5")
            except:
                errors.append(f"Progress must be a number 1-5")
        
        # Validate numeric fields
        numeric_fields = ['target_value', 'actual_value', 'health_score', 'risk_score']
        for field in numeric_fields:
            if field in record and record[field] is not None:
                try:
                    float(record[field])
                except:
                    errors.append(f"{field} must be a number")
        
        # Validate date
        if 'last_updated' in record:
            try:
                pd.to_datetime(record['last_updated'])
            except:
                errors.append("Invalid date format for last_updated")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def clean_text_field(self, text: Any) -> str:
        """Clean and standardize text fields"""
        if pd.isna(text) or text is None:
            return 'TBD'
        
        # Convert to string
        text = str(text).strip()
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Limit length
        if len(text) > 500:
            text = text[:497] + '...'
        
        return text if text else 'TBD'
    
    def clean_numeric_field(self, value: Any, default: float = 0.0) -> float:
        """Clean and validate numeric fields"""
        if pd.isna(value) or value is None:
            return default
        
        try:
            # Handle percentage strings
            if isinstance(value, str) and '%' in value:
                value = value.replace('%', '').strip()
            
            # Convert to float
            numeric_value = float(value)
            
            # Ensure non-negative
            return max(0.0, numeric_value)
        except:
            return default
    
    def clean_date_field(self, date: Any) -> datetime:
        """Clean and validate date fields"""
        if pd.isna(date) or date is None:
            return datetime.now()
        
        try:
            # Try to parse the date
            parsed_date = pd.to_datetime(date)
            
            # Ensure date is not in the future
            if parsed_date > datetime.now():
                return datetime.now()
            
            return parsed_date
        except:
            return datetime.now()
    
    def validate_status(self, status: Any) -> str:
        """Validate and clean status field"""
        if pd.isna(status) or status is None:
            return 'R'  # Default to Red/At Risk
        
        status = str(status).upper().strip()
        
        # Map common variations
        status_map = {
            'GREEN': 'G',
            'YELLOW': 'Y',
            'RED': 'R',
            'ON TRACK': 'G',
            'NEEDS ATTENTION': 'Y',
            'AT RISK': 'R',
            'GOOD': 'G',
            'WARNING': 'Y',
            'CRITICAL': 'R'
        }
        
        if status in self.valid_statuses:
            return status
        elif status in status_map:
            return status_map[status]
        else:
            return 'Y'  # Default to Yellow if uncertain
    
    def validate_progress(self, progress: Any) -> int:
        """Validate and clean progress field"""
        if pd.isna(progress) or progress is None:
            return 3  # Default to middle
        
        try:
            # Convert to integer
            progress_val = int(float(progress))
            
            # Ensure within range
            return max(1, min(5, progress_val))
        except:
            return 3
    
    # Private helper methods
    def _create_empty_dataframe(self) -> pd.DataFrame:
        """Create empty dataframe with proper structure"""
        columns = self.required_columns + self.optional_columns
        df = pd.DataFrame(columns=columns)
        
        # Set proper dtypes
        for col, dtype in self.column_types.items():
            if col in df.columns:
                if dtype == 'datetime':
                    df[col] = pd.to_datetime(df[col])
                elif dtype == int:
                    df[col] = df[col].astype('Int64')  # Nullable integer
                elif dtype == float:
                    df[col] = df[col].astype('float64')
                elif dtype == str:
                    df[col] = df[col].astype('object')
        
        return df
    
    def _ensure_required_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure all required columns exist"""
        for col in self.required_columns:
            if col not in df.columns:
                if col == 'kpi_name':
                    df[col] = 'Unnamed KPI'
                elif col == 'project':
                    df[col] = 'Default Project'
                elif col == 'status':
                    df[col] = 'R'
                elif col == 'owner':
                    df[col] = 'TBD'
                elif col == 'last_updated':
                    df[col] = datetime.now()
        
        return df
    
    def _validate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean each column"""
        # Text fields
        text_columns = ['kpi_name', 'project', 'goal', 'description', 'owner', 
                       'measurement', 'activities', 'barriers', 'successes']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_text_field)
        
        # Status field
        if 'status' in df.columns:
            df['status'] = df['status'].apply(self.validate_status)
        
        # Progress field
        if 'progress' in df.columns:
            df['progress'] = df['progress'].apply(self.validate_progress)
        
        # Numeric fields
        numeric_columns = ['target_value', 'actual_value', 'health_score', 'risk_score']
        for col in numeric_columns:
            if col in df.columns:
                default = 100.0 if col == 'target_value' else 0.0
                df[col] = df[col].apply(lambda x: self.clean_numeric_field(x, default))
        
        # Date field
        if 'last_updated' in df.columns:
            df['last_updated'] = df['last_updated'].apply(self.clean_date_field)
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate records"""
        # Remove exact duplicates
        df = df.drop_duplicates()
        
        # Remove duplicates based on key fields
        key_fields = ['kpi_name', 'project', 'owner']
        available_keys = [k for k in key_fields if k in df.columns]
        
        if available_keys:
            # Keep the most recent record for each unique combination
            if 'last_updated' in df.columns:
                df = df.sort_values('last_updated', ascending=False)
            df = df.drop_duplicates(subset=available_keys, keep='first')
        
        return df
    
    def _fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values with appropriate defaults"""
        fill_values = {
            'kpi_name': 'Unnamed KPI',
            'project': 'Default Project',
            'goal': 'TBD',
            'description': 'TBD',
            'owner': 'TBD',
            'status': 'R',
            'progress': 3,
            'target_value': 100.0,
            'actual_value': 0.0,
            'health_score': 50.0,
            'risk_score': 50.0,
            'measurement': 'TBD',
            'activities': 'TBD',
            'barriers': 'TBD',
            'successes': 'TBD',
            'last_updated': datetime.now()
        }
        
        for col, default_value in fill_values.items():
            if col in df.columns:
                df[col] = df[col].fillna(default_value)
        
        return df
    
    def _validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure correct data types"""
        for col, dtype in self.column_types.items():
            if col in df.columns:
                try:
                    if dtype == 'datetime':
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        df[col] = df[col].fillna(datetime.now())
                    elif dtype == int:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(3).astype(int)
                    elif dtype == float:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
                    elif dtype == str:
                        df[col] = df[col].astype(str)
                except Exception as e:
                    print(f"Warning: Could not convert {col} to {dtype}: {e}")
        
        return df
    
    def _validate_value_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate that values are within acceptable ranges"""
        # Progress: 1-5
        if 'progress' in df.columns:
            df['progress'] = df['progress'].clip(1, 5)
        
        # Percentages: 0-100
        percentage_columns = ['health_score', 'risk_score', 'completion_percentage']
        for col in percentage_columns:
            if col in df.columns:
                df[col] = df[col].clip(0, 100)
        
        # Non-negative values
        non_negative_columns = ['target_value', 'actual_value']
        for col in non_negative_columns:
            if col in df.columns:
                df[col] = df[col].clip(lower=0)
        
        # Ensure actual <= target for realistic completion
        if 'actual_value' in df.columns and 'target_value' in df.columns:
            # Don't clip actual if it exceeds target (overachievement is possible)
            pass
        
        return df
    
    def _add_calculated_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add calculated fields if they don't exist"""
        # Completion percentage
        if 'completion_percentage' not in df.columns:
            if 'actual_value' in df.columns and 'target_value' in df.columns:
                df['completion_percentage'] = df.apply(
                    lambda x: min((x['actual_value'] / x['target_value'] * 100) 
                                 if x['target_value'] > 0 else 0, 100),
                    axis=1
                )
        
        # Days since update
        if 'days_since_update' not in df.columns:
            if 'last_updated' in df.columns:
                df['days_since_update'] = (datetime.now() - pd.to_datetime(df['last_updated'])).dt.days
        
        # Risk level (if risk_score exists but risk_level doesn't)
        if 'risk_score' in df.columns and 'risk_level' not in df.columns:
            df['risk_level'] = df['risk_score'].apply(self._get_risk_level)
        
        # KPI ID if not present
        if 'kpi_id' not in df.columns:
            df['kpi_id'] = range(1, len(df) + 1)
        
        return df
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level from risk score"""
        if risk_score >= 70:
            return 'High'
        elif risk_score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_validation_report(self, df: pd.DataFrame) -> Dict:
        """Generate validation report"""
        report = {
            'total_records': len(df),
            'valid_records': 0,
            'warnings': [],
            'errors': [],
            'summary': {}
        }
        
        # Check for critical issues
        if df.empty:
            report['errors'].append("No data to validate")
            return report
        
        # Count valid records
        valid_count = 0
        for idx, row in df.iterrows():
            is_valid, errors = self.validate_kpi_record(row.to_dict())
            if is_valid:
                valid_count += 1
        
        report['valid_records'] = valid_count
        
        # Check for warnings
        if 'status' in df.columns:
            red_count = (df['status'] == 'R').sum()
            if red_count > len(df) * 0.5:
                report['warnings'].append(f"{red_count} KPIs ({red_count/len(df)*100:.0f}%) are at risk")
        
        if 'days_since_update' in df.columns:
            stale_count = (df['days_since_update'] > 30).sum()
            if stale_count > 0:
                report['warnings'].append(f"{stale_count} KPIs haven't been updated in 30+ days")
        
        if 'health_score' in df.columns:
            low_health = (df['health_score'] < 50).sum()
            if low_health > 0:
                report['warnings'].append(f"{low_health} KPIs have health scores below 50%")
        
        # Summary statistics
        report['summary'] = {
            'columns': df.columns.tolist(),
            'missing_required': [col for col in self.required_columns if col not in df.columns],
            'data_types': {col: str(df[col].dtype) for col in df.columns},
            'null_counts': df.isnull().sum().to_dict()
        }
        
        return report