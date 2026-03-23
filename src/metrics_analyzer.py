import git
import re
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class MetricsAnalyzer:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.repo_path = repo_path

    def analyze_code_quality(self) -> Dict:
        """Analyzes code quality metrics across the repository"""
        files = self._get_all_source_files()
        metrics = {
            'complexity': self._calculate_complexity(files),
            'tech_debt': self._identify_tech_debt(files),
            'code_smells': self._detect_code_smells(files),
            'documentation': self._analyze_documentation(files)
        }
        return metrics

    def _get_all_source_files(self) -> List[str]:
        """Returns all Python source files in the repository"""
        source_files = []
        for root, _, files in git.os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    source_files.append(git.os.path.join(root, file))
        return source_files

    def _calculate_complexity(self, files: List[str]) -> Dict:
        """Calculates cyclomatic complexity for each file"""
        complexity_metrics = {}
        for file_path in files:
            with open(file_path, 'r') as f:
                content = f.read()
                # Basic complexity calculation based on control structures
                complexity = (
                    content.count('if ') +
                    content.count('for ') +
                    content.count('while ') +
                    content.count('except') +
                    1  # Base complexity
                )
                complexity_metrics[file_path] = complexity
        return complexity_metrics

    def _identify_tech_debt(self, files: List[str]) -> List[Dict]:
        """Identifies potential technical debt markers"""
        tech_debt_markers = []
        debt_patterns = [
            (r'# TODO:', 'TODO comment'),
            (r'# FIXME:', 'FIXME comment'),
            (r'# HACK:', 'Hack implementation'),
            (r'except\s+Exception:', 'Bare exception handler')
        ]

        for file_path in files:
            with open(file_path, 'r') as f:
                content = f.read()
                line_number = 1
                for line in content.split('\n'):
                    for pattern, debt_type in debt_patterns:
                        if re.search(pattern, line):
                            tech_debt_markers.append({
                                'file': file_path,
                                'line': line_number,
                                'type': debt_type,
                                'content': line.strip()
                            })
                    line_number += 1
        return tech_debt_markers

    def _detect_code_smells(self, files: List[str]) -> List[Dict]:
        """Detects common code smells"""
        code_smells = []
        smell_patterns = [
            (r'def\s+\w+\s*\([^)]{120,}\):', 'Long parameter list'),
            (r'class\s+\w+:\s*(?:\s*def\s+\w+)*\s*pass\s*$', 'Empty class'),
            (r'if\s+[^:]+and\s+[^:]+and\s+[^:]+:', 'Complex condition')
        ]

        for file_path in files:
            with open(file_path, 'r') as f:
                content = f.read()
                for pattern, smell_type in smell_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        code_smells.append({
                            'file': file_path,
                            'type': smell_type,
                            'line': content[:match.start()].count('\n') + 1
                        })
        return code_smells

    def _analyze_documentation(self, files: List[str]) -> Dict:
        """Analyzes documentation coverage and quality"""
        doc_metrics = {
            'total_functions': 0,
            'documented_functions': 0,
            'documentation_ratio': 0.0,
            'files_without_docstrings': []
        }

        for file_path in files:
            with open(file_path, 'r') as f:
                content = f.read()
                functions = re.finditer(r'def\s+\w+\s*\(', content)
                
                for func in functions:
                    doc_metrics['total_functions'] += 1
                    # Check for docstring after function definition
                    func_pos = func.end()
                    next_chars = content[func_pos:func_pos+100]
                    if '"""' in next_chars or "'''" in next_chars:
                        doc_metrics['documented_functions'] += 1
                
                if '"""' not in content and "'''" not in content:
                    doc_metrics['files_without_docstrings'].append(file_path)

        if doc_metrics['total_functions'] > 0:
            doc_metrics['documentation_ratio'] = (
                doc_metrics['documented_functions'] / doc_metrics['total_functions']
            )

        return doc_metrics