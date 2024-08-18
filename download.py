import gdown

# Download .pth file
def download_pth():
    url = 'https://drive.google.com/uc?id=1UYe2gf_Ik_jRM4rcJROkJHHQM36FR518'
    output = 'best_movie_recommendation_model.pth'
    gdown.download(url, output, quiet=False)

def download_movies():
    url = 'https://drive.google.com/uc?id=1X5VA7n2TDpjDR-CIdYcSoQNcJ7oebpdZ'
    output = 'dataset/movies.csv'
    gdown.download(url, output, quiet=False)

def download_ratings():
    url = 'https://drive.google.com/uc?id=1E9BemxeY1Fu6yAHXnJCmTn2UlhhvIKxm'
    output = 'dataset/ratings.csv'
    gdown.download(url, output, quiet=False)