import torch
import torch.nn as nn

# Movie Recommendation Model
class MovieRecommendationModel(nn.Module):
    def __init__(self, num_users, num_movies, embedding_size=50):
        super(MovieRecommendationModel, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_size)
        self.movie_embedding = nn.Embedding(num_movies, embedding_size)
        self.fc1 = nn.Linear(embedding_size * 2, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)
        
    def forward(self, user_id, movie_id):
        user_embedded = self.user_embedding(user_id)
        movie_embedded = self.movie_embedding(movie_id)
        x = torch.cat([user_embedded, movie_embedded], dim=-1)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        rating = self.fc3(x)
        return rating
