import datetime
from typing import Dict, List, Optional

class MetricsAnalyzer:
    def __init__(self):
        self.health_weights = {
            'commit_frequency': 0.3,
            'pr_velocity': 0.2,
            'issue_resolution': 0.2,
            'code_churn': 0.15,
            'contributor_growth': 0.15
        }

    def calculate_commit_frequency_score(self, commits: List[Dict]) -> float:
        if not commits:
            return 0.0

        now = datetime.datetime.now()
        commit_dates = [c['date'] for c in commits]
        date_diffs = [(now - date).days for date in commit_dates]
        
        if not date_diffs:
            return 0.0

        avg_days_between = sum(date_diffs) / len(date_diffs)
        # Score decreases as average days between commits increases
        score = max(0, 1 - (avg_days_between / 30))
        return min(1.0, score)

    def calculate_pr_velocity_score(self, prs: List[Dict]) -> float:
        if not prs:
            return 0.0

        merged_prs = [pr for pr in prs if pr['merged']]
        avg_time_to_merge = sum(
            (pr['merged_at'] - pr['created_at']).days 
            for pr in merged_prs
        ) / len(merged_prs) if merged_prs else 0

        # Score decreases as average merge time increases
        score = max(0, 1 - (avg_time_to_merge / 14))
        return min(1.0, score)

    def calculate_issue_resolution_score(self, issues: List[Dict]) -> float:
        if not issues:
            return 0.0

        closed_issues = [i for i in issues if i['state'] == 'closed']
        resolution_ratio = len(closed_issues) / len(issues)

        avg_resolution_time = sum(
            (i['closed_at'] - i['created_at']).days 
            for i in closed_issues
        ) / len(closed_issues) if closed_issues else 30

        time_score = max(0, 1 - (avg_resolution_time / 30))
        return min(1.0, (resolution_ratio * 0.6 + time_score * 0.4))

    def calculate_code_churn_score(self, commits: List[Dict]) -> float:
        if not commits:
            return 0.0

        total_changes = sum(c['additions'] + c['deletions'] for c in commits)
        avg_changes = total_changes / len(commits)

        # Score decreases as average changes per commit increases
        score = max(0, 1 - (avg_changes / 500))
        return min(1.0, score)

    def calculate_contributor_growth(self, 
                                   contributors: List[Dict], 
                                   timeframe_days: int = 90) -> float:
        if not contributors:
            return 0.0

        now = datetime.datetime.now()
        recent_contributors = [
            c for c in contributors 
            if (now - c['first_contribution']).days <= timeframe_days
        ]

        growth_rate = len(recent_contributors) / len(contributors)
        return min(1.0, growth_rate)

    def calculate_repository_health(self,
                                  commits: List[Dict],
                                  prs: List[Dict],
                                  issues: List[Dict],
                                  contributors: List[Dict]) -> Dict[str, float]:
        """Calculate overall repository health score and individual metrics."""
        
        scores = {
            'commit_frequency': self.calculate_commit_frequency_score(commits),
            'pr_velocity': self.calculate_pr_velocity_score(prs),
            'issue_resolution': self.calculate_issue_resolution_score(issues),
            'code_churn': self.calculate_code_churn_score(commits),
            'contributor_growth': self.calculate_contributor_growth(contributors)
        }

        # Calculate weighted average for overall health score
        overall_score = sum(
            scores[metric] * self.health_weights[metric]
            for metric in scores
        )

        scores['overall_health'] = overall_score
        return scores

    def get_health_insights(self, scores: Dict[str, float]) -> List[str]:
        """Generate actionable insights based on health scores."""
        insights = []
        
        if scores['commit_frequency'] < 0.5:
            insights.append(
                'Consider increasing commit frequency to improve code velocity'
            )
        
        if scores['pr_velocity'] < 0.5:
            insights.append(
                'PR review times are high - try implementing PR size limits'
            )
            
        if scores['issue_resolution'] < 0.5:
            insights.append(
                'Issue resolution needs attention - consider triage protocols'
            )
            
        if scores['code_churn'] < 0.5:
            insights.append(
                'High code churn detected - review refactoring practices'
            )
            
        if scores['contributor_growth'] < 0.3:
            insights.append(
                'Low contributor growth - consider improving documentation'
            )
            
        return insights