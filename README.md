# Movie Recommender System

A content-based movie recommendation app that returns the top 5 similar titles with posters, similarity match percentages, and movie overviews.

## Live Demo
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://movie-recommender-system-iqko7nhkvwvuoeglp4pwid.streamlit.app/)

## About the Project
This project implements a content-based filtering recommender using TMDB-style movie metadata. It creates a unified text representation from curated tags, lowercases and stems tokens with NLTK (Porter stemmer), vectorizes text with `CountVectorizer` (`max_features=5000`, English stop words), computes pairwise cosine similarity, and serves recommendations through a Streamlit interface.

The app loads `movies.pkl` and `similarity.pkl` from the `models/` directory and calls the TMDB API at runtime for poster images.

## Features
- Recommends the top 5 most similar movies for a selected title.
- Displays similarity scores as percentage-based match values.
- Shows movie descriptions (overview) for each recommended movie.
- Uses a precomputed similarity matrix for low-latency retrieval.
- Fetches movie posters dynamically from the TMDB movie endpoint.
- Falls back to placeholder images when poster requests fail or data is missing.
- Provides an interactive Streamlit UI with a deduplicated movie selectbox and one-click recommendation flow.
- Uses `@st.cache_data` to cache loaded pickle artifacts between interactions.

## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2C3E50?logo=python&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F6B?logo=python&logoColor=white)

Python, Streamlit, Pandas, NumPy, scikit-learn, Requests, and NLTK (see `requirements.txt`).

## Screenshots
| Landing Page | Movie Selection |
|---|---|
| ![Landing Page](Screenshots/screenshot_landing.png) | ![Movie Selection](Screenshots/screenshot_selection.png) |

| Recommendation Results | Recommendation Results (Alt Example) |
|---|---|
| ![Recommendation Results](Screenshots/screenshot_results.png) | ![Recommendation Results Alt](Screenshots/screenshot_results(2).png) |

## How It Works
Training and preprocessing are performed offline; the Streamlit app loads only serialized artifacts for inference.

### 1. Data Loading
- Source files: `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` (read via `pd.read_csv`).
- This repository includes equivalent comma-separated files under `data/tmdb_5000_movies.txt` and `data/tmdb_5000_credits.txt`. You can rename/copy them to `.csv` or read them directly.

### 2. Merge and Clean
- Merges movies and credits on `title`.
- Retains: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
- Drops null rows with `dropna`.

### 3. Feature Engineering
- Parses JSON-like columns with `ast.literal_eval`.
- Extracts `name` values for `genres` and `keywords`.
- `convertCast`: keeps first 3 cast members.
- `fetch_Director`: extracts crew member where `job == 'Director'`.
- Tokenizes `overview`, removes inner spaces in multi-word tokens (for example, `Science Fiction` -> `ScienceFiction`).
- Builds `tags` from `overview + genres + keywords + cast` (director is extracted but not added to `tags` in the notebook).
- Joins tokens, lowercases text, and applies NLTK Porter stemming.

### 4. Vectorization
- Applies `CountVectorizer(max_features=5000, stop_words='english')` on `tags`.
- `fit_transform(...).toarray()` gives a matrix with notebook-reported shape `(4806, 5000)`.

### 5. Similarity
- Computes `cosine_similarity(vectors)` with shape `(4806, 4806)`.
- Saves artifacts using pickle:
  - `movies.pkl`: DataFrame containing `movie_id`, `title`, `tags` (plus any saved columns).
  - `similarity.pkl`: cosine similarity matrix aligned with movie row order.

### 6. Recommendation Flow (`app.py`)
- Resolves `models/movies.pkl` and `models/similarity.pkl` relative to the script directory.
- On `Recommend`: finds selected movie index, sorts similarity scores in descending order, takes indices `[1:6]` (excluding self), maps to `movie_id` and title, then fetches posters with `fetch_poster(movie_id)`.
- Displays recommended titles with poster, match percentage, and overview text.

## Project Structure
```text
Movie Recommender System/
├── app.py
├── README.md
├── requirements.txt
├── MIT_LICENSE.txt
├── .gitignore
├── .gitattributes
├── data/
│   ├── tmdb_5000_movies.txt
│   └── tmdb_5000_credits.txt
├── models/
│   ├── movies.pkl
│   └── similarity.pkl
└── Screenshots/
    ├── screenshot_landing.png
    ├── screenshot_selection.png
    ├── screenshot_results.png
    └── screenshot_results(2).png
```

## Installation & Setup
### Prerequisites
- Python 3.9 or later
- Git
- Virtual environment (recommended)

### Local Setup
```bash
git clone <YOUR_REPO_URL>
cd "Movie Recommender System"
python -m venv .venv
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

```bash
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Ensure `models/movies.pkl` and `models/similarity.pkl` are present before running the app.

## Configuration
### TMDB API Key
`fetch_poster` in `app.py` currently uses a hard-coded TMDB API key.

For production or shared deployments, prefer Streamlit secrets or environment variables:

**Streamlit secrets**
```toml
# .streamlit/secrets.toml
TMDB_API_KEY="YOUR_TMDB_API_KEY"
```

**Environment variable (PowerShell)**
```powershell
$env:TMDB_API_KEY="YOUR_TMDB_API_KEY"
```

## Usage
1. Start the app with `streamlit run app.py`.
2. Select a movie from the dropdown.
3. Click `Recommend`.
4. Review the top 5 recommendations with poster, similarity percentage, and overview.

## Model Artifacts
| File | Role |
|------|------|
| `models/movies.pkl` | DataFrame containing `movie_id`, `title`, `tags` (and any additional saved columns). |
| `models/similarity.pkl` | Precomputed cosine similarity matrix aligned with movie row order. |

## Future Improvements
- Move TMDB key handling to secrets or environment variables in code.
- Add fuzzy / typo-tolerant movie search.
- Add filters (genre, year, language) before or after ranking.
- Explore hybrid recommendation strategies (content + collaborative).
- Add evaluation workflows (for example, precision@k and qualitative spot checks).
- Add automated tests for data loading and recommendation output quality.

## License
This project is licensed under the MIT License.
