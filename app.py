import streamlit as st
import pickle
import requests
import os

BASE_DIR = r"C:\Users\Acer\Desktop\Movie Recommender System\models"

@st.cache_data
def load_data():
    try:
        movies_path = os.path.join(BASE_DIR, "movies.pkl")
        similarity_path = os.path.join(BASE_DIR, "similarity.pkl")

        with open(movies_path, "rb") as f:
            movies = pickle.load(f)

        with open(similarity_path, "rb") as f:
            similarity = pickle.load(f)

        return movies, similarity

    except Exception as e:
        st.error(f"❌ Error loading pickle files: {e}")
        st.stop()

movies, similarity = load_data()


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda u: u[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

st.markdown("### 🔍 Select a movie to get recommendations")

movie_list = movies['title'].drop_duplicates().values

selected_movie_name = st.selectbox(
    "Choose Movie",
    movie_list
)

if st.button('Recommend'):
    with st.spinner('Finding best movies for you...'):
        names, posters = recommend(selected_movie_name)

    st.markdown("### 🎥 Recommended Movies")

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)