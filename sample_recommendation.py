from recommendation import recommend_movies

# Example usage
user_id = 1  # Replace with a valid encoded user ID
description = "I love heartwarming movies with positive and uplifting stories."
recommendations = recommend_movies(user_id, description)
print(recommendations)