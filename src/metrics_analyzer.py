import numpy as np

class MetricsAnalyzer:
    def __init__(self):
        self.metrics = {}

    def add_metric(self, name, value):
        self.metrics[name] = value

    def analyze_metrics(self):
        """Performs advanced analysis on the collected metrics."""
        # Calculate mean, median, and standard deviation
        metric_values = list(self.metrics.values())
        mean = np.mean(metric_values)
        median = np.median(metric_values)
        std_dev = np.std(metric_values)

        # Identify outliers using z-score
        z_scores = [(x - mean) / std_dev for x in metric_values]
        outliers = [name for name, z in zip(self.metrics.keys(), z_scores) if abs(z) > 3]

        # Generate insights
        insights = {
            'mean': mean,
            'median': median,
            'standard_deviation': std_dev,
            'outliers': outliers
        }

        return insights
