import git
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

class GitMetricsAnalyzer:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)
        self.metrics = {}
    
    def analyze_commit_frequency(self, days=30):
        """Analyze commit patterns over specified time period"""
        since_date = datetime.now() - timedelta(days=days)
        commits = list(self.repo.iter_commits(since=since_date))
        
        commit_dates = defaultdict(int)
        for commit in commits:
            date = commit.committed_datetime.date()
            commit_dates[date] += 1
            
        df = pd.DataFrame.from_dict(commit_dates, orient='index')
        df.columns = ['commits']
        return df
    
    def analyze_contributor_impact(self):
        """Analyze contribution patterns per author"""
        author_stats = defaultdict(lambda: {'commits': 0, 'insertions': 0, 'deletions': 0})
        
        for commit in self.repo.iter_commits():
            stats = commit.stats.total
            author = commit.author.name
            author_stats[author]['commits'] += 1
            author_stats[author]['insertions'] += stats['insertions']
            author_stats[author]['deletions'] += stats['deletions']
        
        return pd.DataFrame.from_dict(author_stats, orient='index')
    
    def analyze_file_hotspots(self):
        """Identify frequently modified files"""
        file_changes = defaultdict(int)
        
        for commit in self.repo.iter_commits():
            for file in commit.stats.files:
                file_changes[file] += 1
                
        return pd.Series(file_changes).sort_values(ascending=False)
    
    def generate_insights(self):
        """Generate key insights about the repository"""
        insights = {
            'commit_frequency': self.analyze_commit_frequency(),
            'contributor_impact': self.analyze_contributor_impact(),
            'hotspots': self.analyze_file_hotspots()
        }
        
        # Add high-level metrics
        insights['total_commits'] = len(list(self.repo.iter_commits()))
        insights['active_contributors'] = len(insights['contributor_impact'])
        insights['most_active_files'] = insights['hotspots'].head(5)
        
        return insights

    def export_metrics(self, output_path='metrics_report.json'):
        """Export analyzed metrics to JSON file"""
        insights = self.generate_insights()
        
        # Convert DataFrames to dict format for JSON serialization
        export_data = {
            'repository_stats': {
                'total_commits': insights['total_commits'],
                'active_contributors': insights['active_contributors'],
                'commit_frequency': insights['commit_frequency'].to_dict(),
                'contributor_metrics': insights['contributor_impact'].to_dict(),
                'file_hotspots': insights['hotspots'].to_dict()
            }
        }
        
        pd.io.json.to_json(output_path, export_data)
        return output_path