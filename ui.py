import streamlit as st
from recommendation import recommend_movies

# Streamlit UI
st.title("Movie Recommendation System")
st.write("Enter your details to get personalized movie recommendations.")

name = st.text_input("Name")
user_id = st.number_input("User ID", min_value=1)
description = st.text_area("Describe the types of movies you like")

if st.button("Get Recommendations"):
    if name and user_id and description:    
        # Get recommendations
        recommendations = recommend_movies(user_id, description)
        
        st.write(f"Hello, {name}! Based on your preferences, we recommend the following movies:")
        for i, movie in enumerate(recommendations, start=1):
            st.write(f"{i}. {movie}")
    else:
        st.write("Please fill in all fields.")