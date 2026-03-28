# 🎬 Movie Recommender System

Explore a movie recommender that returns the **top 5 similar titles** with live poster previews.

## Live Demo
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://movie-recommender-system-iqko7nhkvwvuoeglp4pwid.streamlit.app/)


## About
This project implements a **content-based filtering** recommender for movies using metadata from TMDB-style datasets.  
It builds a text field from curated tags, **lowercases** and **stems** tokens with **NLTK** (Porter stemmer), vectorizes with **`CountVectorizer`** (English stop words, `max_features=5000`), computes pairwise **cosine similarity**, and serves recommendations through a **Streamlit** UI.

The app loads **`movies.pkl`** and **`similarity.pkl`** from the **`models/`** directory and calls the **TMDB API** at runtime for poster images.

## Features
- Recommends **top 5** similar movies for a selected title.
- Uses a precomputed similarity matrix for fast retrieval.
- Fetches movie posters dynamically from the TMDB movie endpoint.
- Handles missing or failed poster responses with placeholder images.
- Interactive Streamlit UI: centered title, movie **selectbox** (duplicate titles deduplicated), **Recommend** button, five-column results.
- **`@st.cache_data`** caches loaded pickle artifacts so they are not re-read on every interaction.

## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2C3E50?logo=python&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F6B?logo=python&logoColor=white)

Python · Streamlit · Pandas · NumPy · scikit-learn · Requests · NLTK (see `requirements.txt`).

## Screenshots
| Landing Page | Movie Selection |
|---|---|
| ![Landing Page](Screenshots/screenshot_landing.png) | ![Movie Selection](Screenshots/screenshot_selection.png) |

| Recommendation Results | Recommendation Results (Alt Example) |
|---|---|
| ![Recommendation Results](Screenshots/screenshot_results.png) | ![Recommendation Results Alt](Screenshots/screenshot_results(2).png) |

## How It Works

Training and preprocessing live in **`notebooks/Movie_Recommender_System.ipynb`**. The Streamlit app only loads the serialized outputs.

### 1. Data loading
- The notebook expects **`tmdb_5000_movies.csv`** and **`tmdb_5000_credits.csv`** (via `pd.read_csv`).
- This repository also stores the same TMDB extract under **`data/tmdb_5000_movies.txt`** and **`data/tmdb_5000_credits.txt`** (comma-separated content). You can copy or rename them to `.csv` to match the notebook paths, or point `read_csv` at these files.

### 2. Merge and clean
- Merges movies and credits on **`title`**.
- Keeps: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
- Drops rows with missing values (`dropna`).

### 3. Feature engineering
- Parses JSON-like columns with `ast.literal_eval`.
- Extracts `name` lists for **`genres`** and **`keywords`**.
- **`convertCast`**: first **3** cast names.
- **`fetch_Director`**: crew member with `job == 'Director'`.
- Tokenizes **`overview`** with `.split()`, removes inner spaces in tokens (e.g. `Science Fiction` → `ScienceFiction`).
- Builds **`tags`** as: **`overview` + `genres` + `keywords` + `cast`** (director is computed but not added to `tags` in the notebook).
- Joins tag lists into a single string, **lowercases**, then applies **NLTK Porter stemming** per word.

### 4. Vectorization
- `CountVectorizer(max_features=5000, stop_words='english')` on `tags`.
- `fit_transform(...).toarray()` → notebook-reported shape **`(4806, 5000)`**.

### 5. Similarity
- `cosine_similarity(vectors)` → matrix shape **`(4806, 4806)`**.
- Saved with **`pickle`**: `movies.pkl` (DataFrame with `movie_id`, `title`, `tags`), `similarity.pkl` (place these under **`models/`** for the current app).

### 6. Recommendation flow (`app.py`)
- Resolves **`models/movies.pkl`** and **`models/similarity.pkl`** relative to the script directory.
- On **Recommend**: finds the row index for the selected title, sorts similarity scores descending, takes indices **`[1:6]`** (skip self), maps each index to **`movie_id`** and title, fetches posters via **`fetch_poster(movie_id)`**.

## Project Structure
```text
Movie Recommender System/
├── app.py
├── README.md
├── requirements.txt
├── MIT_LICENSE.txt
├── .gitignore
├── .gitattributes
├── .devcontainer/
│   └── devcontainer.json
├── data/
│   ├── tmdb_5000_credits.txt
│   └── tmdb_5000_movies.txt
├── models/
│   ├── movies.pkl
│   └── similarity.pkl
├── notebooks/
│   └── Movie_Recommender_System.ipynb
└── Screenshots/
    ├── screenshot_landing.png
    ├── screenshot_selection.png
    ├── screenshot_results.png
    └── screenshot_results(2).png
```

## Installation & Setup

### Prerequisites
- Python 3.9+ (dev container image uses Python 3.11)
- Git
- (Recommended) virtual environment

### Local run
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

Ensure **`models/movies.pkl`** and **`models/similarity.pkl`** exist (train with the notebook or use committed artifacts).

### Dev Containers (GitHub Codespaces / VS Code)
The **`.devcontainer/devcontainer.json`** installs `requirements.txt`, forwards port **8501**, and can run Streamlit after attach. Adjust commands there if you need extra flags for your environment.

## Configuration
### TMDB API key
`fetch_poster` in **`app.py`** uses a **hard-coded** TMDB API key in the request URL.

For anything beyond local demos:

- Prefer **Streamlit secrets** (e.g. `.streamlit/secrets.toml`, gitignored) or **environment variables**, and build the request URL from that value.

**Streamlit secrets**
```toml
# .streamlit/secrets.toml
TMDB_API_KEY="YOUR_TMDB_API_KEY"
```

**Environment variable (PowerShell)**
```powershell
$env:TMDB_API_KEY="YOUR_TMDB_API_KEY"
```

Wire the key in code in place of the literal string when you implement this.

## Model artifacts
| File | Role |
|------|------|
| `models/movies.pkl` | DataFrame with **`movie_id`**, **`title`**, **`tags`** (and any columns saved at training time). |
| `models/similarity.pkl` | Precomputed **cosine similarity** matrix aligned with movie row order. |

## Usage
1. Start the app: `streamlit run app.py`
2. Choose a movie in the dropdown.
3. Click **Recommend**.
4. Review the top **5** similar titles and posters.

## Future improvements
- Read the TMDB key from secrets or env in code (no hard-coded keys).
- Fuzzy / typo-tolerant title search.
- Filters (genre, year, language) on top of similarity ranking.
- Hybrid recommendations (content + collaborative).
- Evaluation notebook (e.g. precision@k, spot checks).
- Automated tests for data loading and recommendation outputs.

## License
This project is licensed under the **MIT License.**
