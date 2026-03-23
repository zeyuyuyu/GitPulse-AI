import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class MetricsAnalyzer:
    def __init__(self):
        self.health_weights = {
            'commit_frequency': 0.25,
            'issue_resolution_time': 0.2,
            'contributor_growth': 0.15,
            'code_churn': 0.2,
            'pr_velocity': 0.2
        }

    def calculate_commit_frequency_score(self, commits: List[Dict]) -> float:
        if not commits:
            return 0.0
            
        now = datetime.now()
        commit_dates = [datetime.fromisoformat(c['date']) for c in commits]
        
        # Calculate commits per week over last 3 months
        ninety_days_ago = now - timedelta(days=90)
        recent_commits = [d for d in commit_dates if d > ninety_days_ago]
        
        weeks = max(1, (now - ninety_days_ago).days / 7)
        commits_per_week = len(recent_commits) / weeks
        
        # Score from 0-1 based on commits per week
        return min(1.0, commits_per_week / 10)

    def calculate_issue_resolution_score(self, issues: List[Dict]) -> float:
        if not issues:
            return 0.0
            
        resolution_times = []
        for issue in issues:
            if issue['closed_at']:
                created = datetime.fromisoformat(issue['created_at'])
                closed = datetime.fromisoformat(issue['closed_at'])
                resolution_times.append((closed - created).days)
                
        if not resolution_times:
            return 0.0
            
        avg_resolution_time = np.mean(resolution_times)
        # Score inversely proportional to resolution time (faster is better)
        # Normalize to 0-1 range assuming 30 days is average
        return min(1.0, 30 / max(1, avg_resolution_time))

    def calculate_contributor_growth(self, contributors: List[Dict]) -> float:
        if not contributors:
            return 0.0
            
        now = datetime.now()
        three_months_ago = now - timedelta(days=90)
        six_months_ago = now - timedelta(days=180)
        
        recent_contributors = set()
        old_contributors = set()
        
        for c in contributors:
            contrib_date = datetime.fromisoformat(c['date'])
            if contrib_date > three_months_ago:
                recent_contributors.add(c['author'])
            elif contrib_date > six_months_ago:
                old_contributors.add(c['author'])
                
        if not old_contributors:
            return 1.0 if recent_contributors else 0.0
            
        growth_rate = len(recent_contributors) / len(old_contributors)
        return min(1.0, growth_rate)

    def calculate_code_churn_score(self, commits: List[Dict]) -> float:
        if not commits:
            return 0.0
            
        total_changes = sum(c['additions'] + c['deletions'] for c in commits)
        avg_changes_per_commit = total_changes / len(commits)
        
        # Score inversely proportional to average changes
        # Normalize to 0-1 range assuming 200 lines is optimal
        return min(1.0, 200 / max(1, avg_changes_per_commit))

    def calculate_pr_velocity_score(self, pull_requests: List[Dict]) -> float:
        if not pull_requests:
            return 0.0
            
        now = datetime.now()
        ninety_days_ago = now - timedelta(days=90)
        
        recent_prs = [pr for pr in pull_requests 
                     if datetime.fromisoformat(pr['created_at']) > ninety_days_ago]
        
        if not recent_prs:
            return 0.0
            
        merged_prs = [pr for pr in recent_prs if pr['merged_at']]
        merge_ratio = len(merged_prs) / len(recent_prs)
        
        # Calculate average time to merge
        merge_times = []
        for pr in merged_prs:
            created = datetime.fromisoformat(pr['created_at'])
            merged = datetime.fromisoformat(pr['merged_at'])
            merge_times.append((merged - created).days)
            
        avg_merge_time = np.mean(merge_times) if merge_times else 0
        merge_time_score = min(1.0, 7 / max(1, avg_merge_time))
        
        return (merge_ratio * 0.5 + merge_time_score * 0.5)

    def calculate_repository_health(self,
                                 commits: List[Dict],
                                 issues: List[Dict],
                                 contributors: List[Dict],
                                 pull_requests: List[Dict]) -> Dict[str, float]:
        scores = {
            'commit_frequency': self.calculate_commit_frequency_score(commits),
            'issue_resolution_time': self.calculate_issue_resolution_score(issues),
            'contributor_growth': self.calculate_contributor_growth(contributors),
            'code_churn': self.calculate_code_churn_score(commits),
            'pr_velocity': self.calculate_pr_velocity_score(pull_requests)
        }
        
        # Calculate weighted total health score
        total_score = sum(scores[metric] * self.health_weights[metric] 
                         for metric in scores)
        
        scores['overall_health'] = total_score
        return scores