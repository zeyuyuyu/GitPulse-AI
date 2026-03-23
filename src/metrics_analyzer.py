import numpy as np

class MetricsAnalyzer:
    def __init__(self):
        self.metrics_data = []

    def add_metrics(self, new_metrics):
        self.metrics_data.append(new_metrics)

    def analyze_metrics(self):
        metrics_array = np.array(self.metrics_data)
        mean_metrics = np.mean(metrics_array, axis=0)
        std_metrics = np.std(metrics_array, axis=0)
        max_metrics = np.max(metrics_array, axis=0)
        min_metrics = np.min(metrics_array, axis=0)

        return {
            'mean': mean_metrics.tolist(),
            'std_dev': std_metrics.tolist(),
            'max': max_metrics.tolist(),
            'min': min_metrics.tolist()
        }
