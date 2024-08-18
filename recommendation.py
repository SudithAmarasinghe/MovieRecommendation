import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import torch
from model import MovieRecommendationModel
from sentiment import analyze_sentiment
from download import download_pth, download_movies, download_ratings

# Download the dataset
download_movies()
download_ratings()

# Load dataset
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Merge datasets
data = pd.merge(ratings, movies, on='movieId')

# Preprocess: Combine title and genres for a simplistic content-based filtering approach
data['content'] = data['title'] + " " + data['genres']

# Vectorize content using TF-IDF
tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
tfidf_matrix = tfidf.fit_transform(data['content'])

# Encoding user IDs and movie IDs
user_encoder = LabelEncoder()
data['userId'] = user_encoder.fit_transform(data['userId'])

movie_encoder = LabelEncoder()
data['movieId'] = movie_encoder.fit_transform(data['movieId'])

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Instantiate the model and load the saved weights
num_users = len(data['userId'].unique())
num_movies = len(data['movieId'].unique())
model = MovieRecommendationModel(num_users, num_movies).to(device)
download_pth()
model.load_state_dict(torch.load('best_movie_recommendation_model.pth', map_location=device))
model.eval()

# Movie Recommendation Function with Sentiment Analysis
def recommend_movies(user_id, description, num_recommendations=5):
    model.eval()
    
    # Analyze sentiment of the user's description
    sentiment_scores = analyze_sentiment(description)
    sentiment_factor = 1 + sentiment_scores['compound'] * 0.1  # Adjust factor based on sentiment
    
    # Move user_id_tensor to GPU
    user_id_tensor = torch.tensor([user_id], dtype=torch.long).to(device)
    
    predictions = []
    for movie_id in range(num_movies):
        # Move movie_id_tensor to GPU
        movie_id_tensor = torch.tensor([movie_id], dtype=torch.long).to(device)
        
        # Predict rating without computing gradients
        with torch.no_grad():
            predicted_rating = model(user_id_tensor, movie_id_tensor).item()
        
        # Adjust predicted rating based on sentiment
        adjusted_rating = predicted_rating * sentiment_factor
        predictions.append((movie_id, adjusted_rating))
    
    # Sort movies by predicted rating
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Get top N recommendations
    recommended_movie_ids = [movie_id for movie_id, _ in predictions[:num_recommendations]]
    
    # Decode movie IDs and get the corresponding titles
    recommended_movie_titles = []
    for mid in recommended_movie_ids:
        original_movie_id = movie_encoder.inverse_transform([mid])[0]
        movie_title = movies[movies['movieId'] == original_movie_id]['title'].values[0]
        recommended_movie_titles.append(movie_title)
    
    return recommended_movie_titles


