import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Sentiment Analysis Initialization
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(description):
    sentiment_scores = sia.polarity_scores(description)
    return sentiment_scores