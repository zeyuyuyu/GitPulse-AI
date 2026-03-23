import numpy as np
from textblob import TextBlob

def analyze_sentiment(comments):
    """
    Analyze the sentiment of a list of user comments.
    
    Args:
        comments (list): A list of user comments as strings.
        
    Returns:
        dict: A dictionary containing the average sentiment score and the percentage of positive, negative, and neutral comments.
    """
    sentiment_scores = [TextBlob(comment).sentiment.polarity for comment in comments]
    avg_sentiment = np.mean(sentiment_scores)
    
    num_positive = sum(1 for score in sentiment_scores if score > 0)
    num_negative = sum(1 for score in sentiment_scores if score < 0)
    num_neutral = sum(1 for score in sentiment_scores if score == 0)
    
    total_comments = len(comments)
    
    return {
        'avg_sentiment': avg_sentiment,
        'positive_percent': num_positive / total_comments * 100,
        'negative_percent': num_negative / total_comments * 100,
        'neutral_percent': num_neutral / total_comments * 100
    }