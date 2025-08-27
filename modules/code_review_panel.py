"""
Comprehensive Code Review Panel System
======================================
Multi-perspective team approach for systematic code analysis and review
"""

import os
import ast
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import pandas as pd
import re
from collections import defaultdict

@dataclass
class ReviewFinding:
    """Structure for code review findings"""
    severity: str  # Critical, High, Medium, Low, Info
    category: str  # Security, Performance, Maintainability, etc.
    file_path: str
    line_number: Optional[int]
    issue: str
    recommendation: str
    reviewer: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FileMetrics:
    """Metrics for individual files"""
    file_path: str
    lines_of_code: int
    complexity: int
    functions: int
    classes: int
    imports: int
    comments: int
    test_coverage: float = 0.0

class CodeAnalyst:
    """Team Member 1: Code inspection and technical analysis"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.file_catalog = []
        self.dependencies = set()
        self.architectural_patterns = []
        self.technical_debt = []
        self.analysis_matrix = {}
        
    def catalog_files(self) -> List[Dict]:
        """Catalog all files in the codebase"""
        catalog = []
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                relative_path = file_path.relative_to(self.project_path)
                catalog.append({
                    'path': str(relative_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                    'type': self._classify_file(file_path)
                })
        self.file_catalog = catalog
        return catalog
    
    def _classify_file(self, file_path: Path) -> str:
        """Classify file type based on location and content"""
        path_str = str(file_path).lower()
        if 'test' in path_str:
            return 'test'
        elif 'config' in path_str:
            return 'configuration'
        elif 'module' in path_str:
            return 'module'
        elif 'core' in path_str:
            return 'core'
        elif 'util' in path_str:
            return 'utility'
        else:
            return 'other'
    
    def extract_dependencies(self) -> Dict[str, List[str]]:
        """Extract and analyze project dependencies"""
        dependencies = defaultdict(list)
        
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                dependencies[str(file_path)].append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                dependencies[str(file_path)].append(node.module)
                except:
                    continue
                    
        return dict(dependencies)
    
    def identify_patterns(self) -> List[Dict]:
        """Identify architectural patterns and design patterns"""
        patterns = []
        
        # Check for common patterns
        pattern_checks = {
            'Singleton': self._check_singleton,
            'Factory': self._check_factory,
            'Observer': self._check_observer,
            'MVC/MVP': self._check_mvc,
            'Repository': self._check_repository
        }
        
        for pattern_name, check_func in pattern_checks.items():
            result = check_func()
            if result:
                patterns.append({
                    'pattern': pattern_name,
                    'locations': result,
                    'confidence': 'High' if len(result) > 2 else 'Medium'
                })
                
        self.architectural_patterns = patterns
        return patterns
    
    def _check_singleton(self) -> List[str]:
        """Check for singleton pattern usage"""
        locations = []
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '_instance' in content and '__new__' in content:
                            locations.append(str(file_path))
                except:
                    continue
        return locations
    
    def _check_factory(self) -> List[str]:
        """Check for factory pattern usage"""
        locations = []
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'factory' in content.lower() or 'create_' in content:
                            locations.append(str(file_path))
                except:
                    continue
        return locations
    
    def _check_observer(self) -> List[str]:
        """Check for observer pattern usage"""
        locations = []
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'subscribe' in content or 'notify' in content or 'observer' in content.lower():
                            locations.append(str(file_path))
                except:
                    continue
        return locations
    
    def _check_mvc(self) -> List[str]:
        """Check for MVC/MVP pattern usage"""
        locations = []
        dirs = ['models', 'views', 'controllers', 'core', 'modules']
        for dir_name in dirs:
            if (self.project_path / dir_name).exists():
                locations.append(dir_name)
        return locations
    
    def _check_repository(self) -> List[str]:
        """Check for repository pattern usage"""
        locations = []
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'repository' in content.lower() or 'dao' in content.lower():
                            locations.append(str(file_path))
                except:
                    continue
        return locations
    
    def analyze_technical_debt(self) -> List[ReviewFinding]:
        """Identify technical debt and refactoring opportunities"""
        findings = []
        
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    # Check for long files
                    if len(lines) > 500:
                        findings.append(ReviewFinding(
                            severity='Medium',
                            category='Maintainability',
                            file_path=str(file_path),
                            line_number=None,
                            issue=f'File has {len(lines)} lines, exceeds recommended 500',
                            recommendation='Consider splitting into smaller modules',
                            reviewer='Code Analyst'
                        ))
                    
                    # Check for TODOs and FIXMEs
                    for i, line in enumerate(lines, 1):
                        if 'TODO' in line or 'FIXME' in line:
                            findings.append(ReviewFinding(
                                severity='Low',
                                category='Technical Debt',
                                file_path=str(file_path),
                                line_number=i,
                                issue=f'Unresolved TODO/FIXME: {line.strip()}',
                                recommendation='Address or create ticket for tracking',
                                reviewer='Code Analyst'
                            ))
                            
                    # Check for code duplication indicators
                    content = ''.join(lines)
                    if content.count('copy') > 3 or content.count('duplicate') > 2:
                        findings.append(ReviewFinding(
                            severity='Medium',
                            category='Maintainability',
                            file_path=str(file_path),
                            line_number=None,
                            issue='Potential code duplication detected',
                            recommendation='Review for DRY principle violations',
                            reviewer='Code Analyst'
                        ))
                except:
                    continue
                    
        self.technical_debt = findings
        return findings
    
    def generate_report(self) -> Dict:
        """Generate comprehensive code analysis report"""
        return {
            'file_catalog': self.file_catalog,
            'total_files': len(self.file_catalog),
            'dependencies': self.extract_dependencies(),
            'architectural_patterns': self.architectural_patterns,
            'technical_debt': [
                {
                    'severity': f.severity,
                    'category': f.category,
                    'file': f.file_path,
                    'issue': f.issue,
                    'recommendation': f.recommendation
                }
                for f in self.technical_debt
            ],
            'timestamp': datetime.now().isoformat()
        }


class StandardsSpecialist:
    """Team Member 2: Standards and best practices compliance"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.standards_violations = []
        self.design_pattern_issues = []
        self.documentation_gaps = []
        self.test_coverage_report = {}
        
    def evaluate_coding_standards(self) -> List[ReviewFinding]:
        """Evaluate adherence to PEP 8 and other standards"""
        findings = []
        
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                findings.extend(self._check_naming_conventions(file_path))
                findings.extend(self._check_line_length(file_path))
                findings.extend(self._check_imports(file_path))
                findings.extend(self._check_docstrings(file_path))
                
        self.standards_violations = findings
        return findings
    
    def _check_naming_conventions(self, file_path: Path) -> List[ReviewFinding]:
        """Check Python naming conventions"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if not node.name[0].isupper():
                        findings.append(ReviewFinding(
                            severity='Low',
                            category='Standards',
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue=f'Class name "{node.name}" should be CamelCase',
                            recommendation='Rename to follow PEP 8 conventions',
                            reviewer='Standards Specialist'
                        ))
                        
                elif isinstance(node, ast.FunctionDef):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                        findings.append(ReviewFinding(
                            severity='Low',
                            category='Standards',
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue=f'Function name "{node.name}" should be snake_case',
                            recommendation='Rename to follow PEP 8 conventions',
                            reviewer='Standards Specialist'
                        ))
        except:
            pass
            
        return findings
    
    def _check_line_length(self, file_path: Path) -> List[ReviewFinding]:
        """Check for lines exceeding 79 characters"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                if len(line.rstrip()) > 100:  # Using 100 as practical limit
                    findings.append(ReviewFinding(
                        severity='Info',
                        category='Standards',
                        file_path=str(file_path),
                        line_number=i,
                        issue=f'Line length {len(line.rstrip())} exceeds 100 characters',
                        recommendation='Consider breaking into multiple lines',
                        reviewer='Standards Specialist'
                    ))
        except:
            pass
            
        return findings
    
    def _check_imports(self, file_path: Path) -> List[ReviewFinding]:
        """Check import organization and style"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            import_lines = []
            for i, line in enumerate(lines, 1):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_lines.append((i, line.strip()))
                    
            # Check for import order
            if import_lines:
                last_std = 0
                for i, (line_no, import_stmt) in enumerate(import_lines):
                    if any(import_stmt.startswith(f'from {mod}') or import_stmt == f'import {mod}' 
                           for mod in ['os', 'sys', 'json', 'datetime', 're']):
                        if i > last_std + 3:  # Allow some flexibility
                            findings.append(ReviewFinding(
                                severity='Info',
                                category='Standards',
                                file_path=str(file_path),
                                line_number=line_no,
                                issue='Standard library imports should come first',
                                recommendation='Reorganize imports: standard library, third-party, local',
                                reviewer='Standards Specialist'
                            ))
                        last_std = i
        except:
            pass
            
        return findings
    
    def _check_docstrings(self, file_path: Path) -> List[ReviewFinding]:
        """Check for missing or inadequate docstrings"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        findings.append(ReviewFinding(
                            severity='Medium',
                            category='Documentation',
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue=f'Missing docstring for {node.__class__.__name__[:-3].lower()} "{node.name}"',
                            recommendation='Add descriptive docstring',
                            reviewer='Standards Specialist'
                        ))
                    elif len(docstring) < 20:
                        findings.append(ReviewFinding(
                            severity='Low',
                            category='Documentation',
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue=f'Minimal docstring for "{node.name}"',
                            recommendation='Provide more detailed documentation',
                            reviewer='Standards Specialist'
                        ))
        except:
            pass
            
        return findings
    
    def assess_design_patterns(self) -> List[ReviewFinding]:
        """Assess design pattern usage and implementation"""
        findings = []
        
        # Check for anti-patterns
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                findings.extend(self._check_god_class(file_path))
                findings.extend(self._check_long_methods(file_path))
                
        self.design_pattern_issues = findings
        return findings
    
    def _check_god_class(self, file_path: Path) -> List[ReviewFinding]:
        """Check for god class anti-pattern"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > 20:
                        findings.append(ReviewFinding(
                            severity='High',
                            category='Design',
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue=f'Class "{node.name}" has {len(methods)} methods (god class)',
                            recommendation='Consider splitting into smaller, focused classes',
                            reviewer='Standards Specialist'
                        ))
        except:
            pass
            
        return findings
    
    def _check_long_methods(self, file_path: Path) -> List[ReviewFinding]:
        """Check for overly long methods"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Estimate method length
                    if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                        length = node.end_lineno - node.lineno
                        if length > 50:
                            findings.append(ReviewFinding(
                                severity='Medium',
                                category='Design',
                                file_path=str(file_path),
                                line_number=node.lineno,
                                issue=f'Method "{node.name}" is {length} lines long',
                                recommendation='Consider breaking into smaller functions',
                                reviewer='Standards Specialist'
                            ))
        except:
            pass
            
        return findings
    
    def analyze_test_coverage(self) -> Dict:
        """Analyze test coverage and testing strategies"""
        test_files = list(self.project_path.rglob("test*.py"))
        source_files = [f for f in self.project_path.rglob("*.py") 
                       if "__pycache__" not in str(f) and "test" not in str(f).lower()]
        
        coverage = {
            'test_files': len(test_files),
            'source_files': len(source_files),
            'coverage_ratio': len(test_files) / max(len(source_files), 1),
            'test_locations': [str(f) for f in test_files],
            'untested_modules': []
        }
        
        # Identify potentially untested modules
        for source in source_files:
            module_name = source.stem
            has_test = any(module_name in str(test) for test in test_files)
            if not has_test:
                coverage['untested_modules'].append(str(source))
                
        self.test_coverage_report = coverage
        return coverage
    
    def generate_report(self) -> Dict:
        """Generate standards compliance report"""
        return {
            'standards_violations': [
                {
                    'severity': f.severity,
                    'file': f.file_path,
                    'line': f.line_number,
                    'issue': f.issue,
                    'fix': f.recommendation
                }
                for f in self.standards_violations
            ],
            'design_issues': [
                {
                    'severity': f.severity,
                    'file': f.file_path,
                    'issue': f.issue,
                    'recommendation': f.recommendation
                }
                for f in self.design_pattern_issues
            ],
            'test_coverage': self.test_coverage_report,
            'documentation_gaps': len(self.documentation_gaps),
            'total_issues': len(self.standards_violations) + len(self.design_pattern_issues)
        }


class SecurityReviewer:
    """Team Member 3: Security validation and risk assessment"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.security_findings = []
        self.vulnerabilities = []
        self.compliance_issues = []
        
    def identify_security_vulnerabilities(self) -> List[ReviewFinding]:
        """Identify potential security vulnerabilities"""
        findings = []
        
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                findings.extend(self._check_sql_injection(file_path))
                findings.extend(self._check_hardcoded_secrets(file_path))
                findings.extend(self._check_input_validation(file_path))
                findings.extend(self._check_file_operations(file_path))
                findings.extend(self._check_command_injection(file_path))
                
        self.security_findings = findings
        return findings
    
    def _check_sql_injection(self, file_path: Path) -> List[ReviewFinding]:
        """Check for potential SQL injection vulnerabilities"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            dangerous_patterns = [
                (r'\.format\(.*\).*(?:SELECT|INSERT|UPDATE|DELETE)', 'String formatting in SQL'),
                (r'%s.*(?:SELECT|INSERT|UPDATE|DELETE)', 'String interpolation in SQL'),
                (r'f["\'].*{.*}.*(?:SELECT|INSERT|UPDATE|DELETE)', 'F-string in SQL'),
                (r'[\"\'].*\+.*(?:SELECT|INSERT|UPDATE|DELETE)', 'String concatenation in SQL')
            ]
            
            for i, line in enumerate(lines, 1):
                for pattern, issue in dangerous_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append(ReviewFinding(
                            severity='Critical',
                            category='Security',
                            file_path=str(file_path),
                            line_number=i,
                            issue=f'Potential SQL injection: {issue}',
                            recommendation='Use parameterized queries or prepared statements',
                            reviewer='Security Reviewer'
                        ))
        except:
            pass
            
        return findings
    
    def _check_hardcoded_secrets(self, file_path: Path) -> List[ReviewFinding]:
        """Check for hardcoded secrets and credentials"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            secret_patterns = [
                (r'(?:password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
                (r'(?:api_key|apikey|api-key)\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
                (r'(?:secret|token)\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret/token'),
                (r'(?:aws_access_key|aws_secret)\s*=\s*["\'][^"\']+["\']', 'Hardcoded AWS credentials')
            ]
            
            for i, line in enumerate(lines, 1):
                for pattern, issue in secret_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Skip if it's reading from environment
                        if 'os.environ' not in line and 'getenv' not in line:
                            findings.append(ReviewFinding(
                                severity='Critical',
                                category='Security',
                                file_path=str(file_path),
                                line_number=i,
                                issue=issue,
                                recommendation='Use environment variables or secure vaults',
                                reviewer='Security Reviewer'
                            ))
        except:
            pass
            
        return findings
    
    def _check_input_validation(self, file_path: Path) -> List[ReviewFinding]:
        """Check for missing input validation"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for direct use of user input
            if 'request.' in content or 'input(' in content:
                if not any(validation in content for validation in ['validate', 'sanitize', 'clean', 'escape']):
                    findings.append(ReviewFinding(
                        severity='High',
                        category='Security',
                        file_path=str(file_path),
                        line_number=None,
                        issue='User input used without apparent validation',
                        recommendation='Implement input validation and sanitization',
                        reviewer='Security Reviewer'
                    ))
        except:
            pass
            
        return findings
    
    def _check_file_operations(self, file_path: Path) -> List[ReviewFinding]:
        """Check for unsafe file operations"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                if 'open(' in line and '..' in line:
                    findings.append(ReviewFinding(
                        severity='High',
                        category='Security',
                        file_path=str(file_path),
                        line_number=i,
                        issue='Potential path traversal vulnerability',
                        recommendation='Validate and sanitize file paths',
                        reviewer='Security Reviewer'
                    ))
                    
                if 'pickle.load' in line:
                    findings.append(ReviewFinding(
                        severity='High',
                        category='Security',
                        file_path=str(file_path),
                        line_number=i,
                        issue='Unsafe deserialization with pickle',
                        recommendation='Use safer serialization formats like JSON',
                        reviewer='Security Reviewer'
                    ))
        except:
            pass
            
        return findings
    
    def _check_command_injection(self, file_path: Path) -> List[ReviewFinding]:
        """Check for command injection vulnerabilities"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            dangerous_funcs = ['os.system', 'subprocess.call', 'subprocess.run', 'exec', 'eval']
            
            for i, line in enumerate(lines, 1):
                for func in dangerous_funcs:
                    if func in line and any(c in line for c in ['+', 'format', '%', 'f"', "f'"]):
                        findings.append(ReviewFinding(
                            severity='Critical',
                            category='Security',
                            file_path=str(file_path),
                            line_number=i,
                            issue=f'Potential command injection using {func}',
                            recommendation='Use subprocess with list arguments, avoid shell=True',
                            reviewer='Security Reviewer'
                        ))
        except:
            pass
            
        return findings
    
    def evaluate_authentication(self) -> List[ReviewFinding]:
        """Evaluate authentication and authorization implementations"""
        findings = []
        
        auth_files = []
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if any(term in content.lower() for term in ['auth', 'login', 'session', 'token']):
                        auth_files.append(file_path)
                except:
                    continue
                    
        if not auth_files:
            findings.append(ReviewFinding(
                severity='High',
                category='Security',
                file_path='Project',
                line_number=None,
                issue='No authentication mechanism detected',
                recommendation='Implement proper authentication and authorization',
                reviewer='Security Reviewer'
            ))
        else:
            for file_path in auth_files:
                findings.extend(self._check_auth_implementation(file_path))
                
        return findings
    
    def _check_auth_implementation(self, file_path: Path) -> List[ReviewFinding]:
        """Check authentication implementation details"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for weak session management
            if 'session' in content.lower() and 'secure' not in content:
                findings.append(ReviewFinding(
                    severity='Medium',
                    category='Security',
                    file_path=str(file_path),
                    line_number=None,
                    issue='Session cookies may not be secure',
                    recommendation='Set secure flag on session cookies',
                    reviewer='Security Reviewer'
                ))
                
            # Check for missing CSRF protection
            if 'post' in content.lower() and 'csrf' not in content.lower():
                findings.append(ReviewFinding(
                    severity='Medium',
                    category='Security',
                    file_path=str(file_path),
                    line_number=None,
                    issue='Missing CSRF protection',
                    recommendation='Implement CSRF tokens for state-changing operations',
                    reviewer='Security Reviewer'
                ))
        except:
            pass
            
        return findings
    
    def review_error_handling(self) -> List[ReviewFinding]:
        """Review error handling and logging practices"""
        findings = []
        
        for file_path in self.project_path.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ExceptHandler):
                            if node.type is None:  # Bare except clause
                                findings.append(ReviewFinding(
                                    severity='Medium',
                                    category='Security',
                                    file_path=str(file_path),
                                    line_number=node.lineno,
                                    issue='Bare except clause can hide errors',
                                    recommendation='Specify exception types explicitly',
                                    reviewer='Security Reviewer'
                                ))
                except:
                    continue
                    
        return findings
    
    def generate_report(self) -> Dict:
        """Generate security assessment report"""
        severity_counts = defaultdict(int)
        for finding in self.security_findings:
            severity_counts[finding.severity] += 1
            
        return {
            'total_findings': len(self.security_findings),
            'critical': severity_counts['Critical'],
            'high': severity_counts['High'],
            'medium': severity_counts['Medium'],
            'low': severity_counts['Low'],
            'findings': [
                {
                    'severity': f.severity,
                    'category': f.category,
                    'file': f.file_path,
                    'line': f.line_number,
                    'issue': f.issue,
                    'recommendation': f.recommendation
                }
                for f in self.security_findings
            ]
        }


class SeniorReviewLead:
    """Team Member 4: Final integration and strategic oversight"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.code_analyst = CodeAnalyst(project_path)
        self.standards_specialist = StandardsSpecialist(project_path)
        self.security_reviewer = SecurityReviewer(project_path)
        self.integrated_findings = []
        self.remediation_roadmap = []
        
    def integrate_all_reviews(self) -> Dict:
        """Integrate feedback from all review perspectives"""
        print("Running comprehensive code review...")
        
        # Code Analysis
        print("  Phase 1: Code Analysis...")
        self.code_analyst.catalog_files()
        self.code_analyst.identify_patterns()
        code_debt = self.code_analyst.analyze_technical_debt()
        
        # Standards Review
        print("  Phase 2: Standards Compliance...")
        standards_findings = self.standards_specialist.evaluate_coding_standards()
        design_findings = self.standards_specialist.assess_design_patterns()
        test_coverage = self.standards_specialist.analyze_test_coverage()
        
        # Security Review
        print("  Phase 3: Security Assessment...")
        security_findings = self.security_reviewer.identify_security_vulnerabilities()
        auth_findings = self.security_reviewer.evaluate_authentication()
        error_findings = self.security_reviewer.review_error_handling()
        
        # Combine all findings
        all_findings = (
            code_debt + 
            standards_findings + 
            design_findings + 
            security_findings + 
            auth_findings + 
            error_findings
        )
        
        self.integrated_findings = all_findings
        
        return {
            'total_findings': len(all_findings),
            'by_severity': self._group_by_severity(all_findings),
            'by_category': self._group_by_category(all_findings),
            'by_file': self._group_by_file(all_findings)
        }
    
    def _group_by_severity(self, findings: List[ReviewFinding]) -> Dict:
        """Group findings by severity"""
        grouped = defaultdict(list)
        for finding in findings:
            grouped[finding.severity].append(finding)
        return dict(grouped)
    
    def _group_by_category(self, findings: List[ReviewFinding]) -> Dict:
        """Group findings by category"""
        grouped = defaultdict(list)
        for finding in findings:
            grouped[finding.category].append(finding)
        return dict(grouped)
    
    def _group_by_file(self, findings: List[ReviewFinding]) -> Dict:
        """Group findings by file"""
        grouped = defaultdict(list)
        for finding in findings:
            grouped[finding.file_path].append(finding)
        return dict(grouped)
    
    def prioritize_findings(self) -> List[Dict]:
        """Prioritize findings by severity and business impact"""
        severity_weights = {
            'Critical': 5,
            'High': 4,
            'Medium': 3,
            'Low': 2,
            'Info': 1
        }
        
        # Sort by severity weight
        sorted_findings = sorted(
            self.integrated_findings,
            key=lambda f: severity_weights.get(f.severity, 0),
            reverse=True
        )
        
        # Create prioritized list
        prioritized = []
        for finding in sorted_findings[:20]:  # Top 20 issues
            prioritized.append({
                'priority': severity_weights[finding.severity],
                'severity': finding.severity,
                'category': finding.category,
                'file': finding.file_path,
                'issue': finding.issue,
                'recommendation': finding.recommendation,
                'estimated_effort': self._estimate_effort(finding)
            })
            
        return prioritized
    
    def _estimate_effort(self, finding: ReviewFinding) -> str:
        """Estimate effort required to fix an issue"""
        if finding.severity == 'Critical':
            return 'High (4-8 hours)'
        elif finding.severity == 'High':
            return 'Medium (2-4 hours)'
        elif finding.severity == 'Medium':
            return 'Low (1-2 hours)'
        else:
            return 'Minimal (<1 hour)'
    
    def create_remediation_roadmap(self) -> List[Dict]:
        """Create actionable remediation roadmap"""
        roadmap = []
        
        # Phase 1: Critical Security Issues
        critical_security = [
            f for f in self.integrated_findings 
            if f.severity == 'Critical' and f.category == 'Security'
        ]
        if critical_security:
            roadmap.append({
                'phase': 1,
                'name': 'Critical Security Remediation',
                'duration': '1-2 days',
                'tasks': [
                    {
                        'file': f.file_path,
                        'issue': f.issue,
                        'action': f.recommendation
                    }
                    for f in critical_security[:5]
                ]
            })
        
        # Phase 2: High Priority Issues
        high_priority = [
            f for f in self.integrated_findings 
            if f.severity == 'High'
        ]
        if high_priority:
            roadmap.append({
                'phase': 2,
                'name': 'High Priority Fixes',
                'duration': '2-3 days',
                'tasks': [
                    {
                        'file': f.file_path,
                        'issue': f.issue,
                        'action': f.recommendation
                    }
                    for f in high_priority[:10]
                ]
            })
        
        # Phase 3: Code Quality Improvements
        quality_issues = [
            f for f in self.integrated_findings 
            if f.category in ['Maintainability', 'Standards', 'Design']
            and f.severity == 'Medium'
        ]
        if quality_issues:
            roadmap.append({
                'phase': 3,
                'name': 'Code Quality Improvements',
                'duration': '3-5 days',
                'tasks': [
                    {
                        'file': f.file_path,
                        'issue': f.issue,
                        'action': f.recommendation
                    }
                    for f in quality_issues[:10]
                ]
            })
        
        # Phase 4: Documentation and Testing
        roadmap.append({
            'phase': 4,
            'name': 'Documentation and Testing',
            'duration': '2-3 days',
            'tasks': [
                {
                    'action': 'Add missing docstrings',
                    'scope': 'All public APIs'
                },
                {
                    'action': 'Increase test coverage',
                    'scope': f'Target {self.standards_specialist.test_coverage_report.get("untested_modules", []).__len__()} untested modules'
                },
                {
                    'action': 'Update README and documentation',
                    'scope': 'Project-wide'
                }
            ]
        })
        
        self.remediation_roadmap = roadmap
        return roadmap
    
    def generate_comprehensive_report(self) -> Dict:
        """Generate final comprehensive code review report"""
        integration = self.integrate_all_reviews()
        priorities = self.prioritize_findings()
        roadmap = self.create_remediation_roadmap()
        
        report = {
            'executive_summary': {
                'project_path': str(self.project_path),
                'review_date': datetime.now().isoformat(),
                'total_files_reviewed': len(self.code_analyst.file_catalog),
                'total_findings': integration['total_findings'],
                'critical_issues': len([f for f in self.integrated_findings if f.severity == 'Critical']),
                'high_issues': len([f for f in self.integrated_findings if f.severity == 'High']),
                'estimated_remediation_time': self._estimate_total_time(roadmap)
            },
            'code_analysis': self.code_analyst.generate_report(),
            'standards_compliance': self.standards_specialist.generate_report(),
            'security_assessment': self.security_reviewer.generate_report(),
            'prioritized_issues': priorities[:10],  # Top 10
            'remediation_roadmap': roadmap,
            'recommendations': self._generate_recommendations(),
            'metrics': self._calculate_metrics()
        }
        
        return report
    
    def _estimate_total_time(self, roadmap: List[Dict]) -> str:
        """Estimate total remediation time"""
        total_days = 0
        for phase in roadmap:
            duration = phase.get('duration', '0 days')
            # Extract number from duration string
            match = re.search(r'(\d+)', duration)
            if match:
                total_days += int(match.group(1))
        return f"{total_days}-{total_days + 5} days"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Security recommendations
        critical_security = len([f for f in self.integrated_findings 
                                if f.severity == 'Critical' and f.category == 'Security'])
        if critical_security > 0:
            recommendations.append(
                f"URGENT: Address {critical_security} critical security vulnerabilities immediately"
            )
        
        # Test coverage recommendations
        coverage = self.standards_specialist.test_coverage_report
        if coverage.get('coverage_ratio', 0) < 0.5:
            recommendations.append(
                "Improve test coverage - currently below 50% threshold"
            )
        
        # Code quality recommendations
        if len(self.code_analyst.technical_debt) > 20:
            recommendations.append(
                "Schedule technical debt reduction sprint to address accumulated issues"
            )
        
        # Documentation recommendations
        doc_issues = len([f for f in self.integrated_findings if f.category == 'Documentation'])
        if doc_issues > 10:
            recommendations.append(
                "Establish documentation standards and update existing documentation"
            )
        
        # Process recommendations
        recommendations.extend([
            "Implement pre-commit hooks for automatic code quality checks",
            "Set up continuous integration with security scanning",
            "Establish regular code review process",
            "Create coding standards document for team alignment"
        ])
        
        return recommendations
    
    def _calculate_metrics(self) -> Dict:
        """Calculate code quality metrics"""
        total_lines = 0
        for file_info in self.code_analyst.file_catalog:
            if file_info['type'] != 'test':
                # Estimate lines from file size
                total_lines += file_info['size'] // 50  # Rough estimate
                
        return {
            'total_lines_of_code': total_lines,
            'files_analyzed': len(self.code_analyst.file_catalog),
            'architectural_patterns': len(self.code_analyst.architectural_patterns),
            'test_coverage_ratio': self.standards_specialist.test_coverage_report.get('coverage_ratio', 0),
            'issues_per_file': len(self.integrated_findings) / max(len(self.code_analyst.file_catalog), 1),
            'security_score': self._calculate_security_score()
        }
    
    def _calculate_security_score(self) -> float:
        """Calculate security score (0-100)"""
        security_findings = [f for f in self.integrated_findings if f.category == 'Security']
        
        if not security_findings:
            return 100.0
            
        severity_penalties = {
            'Critical': 25,
            'High': 15,
            'Medium': 8,
            'Low': 3,
            'Info': 1
        }
        
        total_penalty = sum(severity_penalties.get(f.severity, 0) for f in security_findings)
        score = max(0, 100 - total_penalty)
        
        return round(score, 1)


def create_review_panel():
    """Factory function to create complete review panel"""
    return {
        'CodeAnalyst': CodeAnalyst,
        'StandardsSpecialist': StandardsSpecialist,
        'SecurityReviewer': SecurityReviewer,
        'SeniorReviewLead': SeniorReviewLead
    }