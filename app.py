import streamlit as st
from dotenv import load_dotenv
import pickle
import requests
import os
 
load_dotenv()  
st.set_page_config(page_title="Movie Recommender", layout="wide")

BASE_DIR = os.path.join(os.path.dirname(__file__), "models")

movie_api = os.getenv("MY_TMDB_API_KEY")

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


def fetch_movie_details(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={movie_api}&language=en-US",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        overview = data.get("overview", "No description available.")
        release_date = data.get("release_date", "Unknown")

        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            poster_url = "https://via.placeholder.com/500x750?text=No+Image"

        return {
            "poster": poster_url,
            "overview": overview,
            "release_date": release_date
        }

    except Exception:
        return {
            "poster": "https://via.placeholder.com/500x750?text=Error",
            "overview": "Could not load description.",
            "release_date": "Unknown"
        }


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda u: u[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_overview = []
    recommended_movies_similarity = []
    recommended_movies_release = []

    for i in movies_list:
        index = i[0]
        sim_score = i[1]

        movie_id = movies.iloc[index].movie_id
        title = movies.iloc[index].title

        details = fetch_movie_details(movie_id)

        recommended_movies.append(title)
        recommended_movies_poster.append(details["poster"])
        recommended_movies_overview.append(details["overview"])
        recommended_movies_release.append(details["release_date"])

        similarity_percent = round(sim_score * 100, 2)
        recommended_movies_similarity.append(similarity_percent)

    return (
        recommended_movies,
        recommended_movies_poster,
        recommended_movies_overview,
        recommended_movies_similarity,
        recommended_movies_release
    )


st.markdown(
    "<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

st.markdown("### 🔍 Select a movie to get recommendations")

movie_list = movies['title'].drop_duplicates().values

selected_movie_name = st.selectbox("Choose Movie", movie_list)

if st.button("Recommend"):
    with st.spinner("Finding best movies for you..."):
        names, posters, overviews, similarities, release_dates = recommend(selected_movie_name)

    st.markdown("### 🎥 Recommended Movies")

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**")
            st.markdown(f"**Similarity:** {similarities[i]}%")
            st.markdown(f"**Release Date:** {release_dates[i]}")

            with st.expander("See Description"):
                
                st.write(overviews[i])
                
