
import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "ml-latest-small")
MOVIES_PATH = os.path.join(DATA_DIR, "movies.csv")
RATINGS_PATH = os.path.join(DATA_DIR, "ratings.csv")

_movies_df = None
_ratings_df = None
_user_item_matrix = None
_item_similarity = None


def _load_data():
    """Load MovieLens CSVs into memory once, and build the item-item
    similarity matrix used for recommendations. Cached at module level
    so this only runs on first use, not on every request."""
    global _movies_df, _ratings_df, _user_item_matrix, _item_similarity

    if _item_similarity is not None:
        return

    if not os.path.exists(MOVIES_PATH) or not os.path.exists(RATINGS_PATH):
        raise FileNotFoundError(
            f"Could not find MovieLens data in {DATA_DIR}. "
            "Download ml-latest-small.zip from "
            "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip "
            "and unzip it next to main.py."
        )

    _movies_df = pd.read_csv(MOVIES_PATH)
    _ratings_df = pd.read_csv(RATINGS_PATH)

  
    _user_item_matrix = _ratings_df.pivot_table(
        index="userId", columns="movieId", values="rating"
    )


    _item_similarity = _user_item_matrix.corr(min_periods=20)

    _user_item_matrix = _ratings_df.pivot_table(
        index="userId", columns="movieId", values="rating"
    )

    
    _item_similarity = _user_item_matrix.corr(min_periods=20)


def get_movie(movie_id: int):
    """Return {id, title, genres} for a MovieLens movieId, or None if not found."""
    _load_data()
    row = _movies_df[_movies_df["movieId"] == movie_id]
    if row.empty:
        return None
    title = row.iloc[0]["title"]
    genres = row.iloc[0]["genres"].split("|") if row.iloc[0]["genres"] != "(no genres listed)" else []
    return {"id": int(movie_id), "title": title, "genres": genres}


def get_recommendations(user_id: int, top_n: int = 10):
    """Item-based collaborative filtering:
    1. Look at movies this user rated highly (>=4).
    2. For each, find similar movies via the item-item correlation matrix.
    3. Score candidate movies by similarity, weighted by the user's rating.
    4. Exclude movies the user already rated. Return the top N.
    """
    _load_data()

    if user_id not in _user_item_matrix.index:
        return []

    user_ratings = _user_item_matrix.loc[user_id].dropna()
    liked = user_ratings[user_ratings >= 4]

    if liked.empty:
        return []

    scores = pd.Series(dtype=float)
    for movie_id, rating in liked.items():
        if movie_id not in _item_similarity.columns:
            continue
        similar = _item_similarity[movie_id].dropna()
        similar = similar * rating  # weight by how much the user liked the seed movie
        scores = scores.add(similar, fill_value=0)

    # Drop movies the user has already rated
    already_rated = set(user_ratings.index)
    scores = scores.drop(labels=[m for m in already_rated if m in scores.index], errors="ignore")

    if scores.empty:
        return []

    top_ids = scores.sort_values(ascending=False).head(top_n).index

    recommendations = []
    for movie_id in top_ids:
        movie = get_movie(int(movie_id))
        if movie:
            recommendations.append(movie)
    return recommendations


def get_available_genres():
    """Return a sorted list of every distinct genre found in movies.csv,
    so a frontend can show them as dropdown/checkbox options."""
    _load_data()

    genres = set()
    for genre_str in _movies_df["genres"]:
        if genre_str == "(no genres listed)":
            continue
        genres.update(genre_str.split("|"))
    return sorted(genres)


def get_recommendations_by_genre(genre: str, top_n: int = 10, min_ratings: int = 20):
    """Content-based recommendation for a new/anonymous user who has no
    rating history — just a favorite genre.

    Movies are ranked using a weighted rating (the same idea IMDB's "Top
    250" uses), so a movie with a handful of 5-star ratings doesn't beat
    a movie with hundreds of ratings averaging 4.5:

        WR = (v / (v + m)) * R + (m / (v + m)) * C

    where:
        R = the movie's own average rating
        v = number of ratings the movie has
        m = min_ratings, the minimum ratings required to be trusted
        C = the mean rating across the whole dataset
    """
    _load_data()

    matches = _movies_df[
        _movies_df["genres"].str.contains(genre, case=False, na=False, regex=False)
    ]
    if matches.empty:
        return []

    matched_ids = set(matches["movieId"])
    genre_ratings = _ratings_df[_ratings_df["movieId"].isin(matched_ids)]
    if genre_ratings.empty:
        return []

    stats = genre_ratings.groupby("movieId")["rating"].agg(["mean", "count"])
    stats = stats.rename(columns={"mean": "avg_rating", "count": "num_ratings"})

    C = _ratings_df["rating"].mean()
    m = min_ratings

    stats["weighted_rating"] = (
        (stats["num_ratings"] / (stats["num_ratings"] + m)) * stats["avg_rating"]
        + (m / (stats["num_ratings"] + m)) * C
    )

    top_ids = stats.sort_values("weighted_rating", ascending=False).head(top_n).index

    recommendations = []
    for movie_id in top_ids:
        movie = get_movie(int(movie_id))
        if movie:
            movie["avg_rating"] = round(float(stats.loc[movie_id, "avg_rating"]), 2)
            movie["num_ratings"] = int(stats.loc[movie_id, "num_ratings"])
            recommendations.append(movie)
    return recommendations


def search_movies(query: str, limit: int = 10):
    """Return {id, title} for movies whose title contains the query
    (case-insensitive). Used to power a movie-title search/autocomplete
    box on the frontend."""
    _load_data()

    if not query:
        return []

    matches = _movies_df[
        _movies_df["title"].str.contains(query, case=False, na=False, regex=False)
    ].head(limit)

    return [
        {"id": int(row["movieId"]), "title": row["title"]}
        for _, row in matches.iterrows()
    ]


def _find_movie_id_by_title(title: str):
    """Find the closest movieId match for a given title string.
    Tries an exact (case-insensitive) match first, then falls back to
    a substring match. Returns None if nothing matches."""
    _load_data()

    exact = _movies_df[_movies_df["title"].str.lower() == title.strip().lower()]
    if not exact.empty:
        return int(exact.iloc[0]["movieId"])

    partial = _movies_df[
        _movies_df["title"].str.contains(title.strip(), case=False, na=False, regex=False)
    ]
    if not partial.empty:
        return int(partial.iloc[0]["movieId"])

    return None


def get_recommendations_by_movie(favorite_movie: str, top_n: int = 10):
    """Content-based recommendation from a single favorite movie, using
    the item-item correlation matrix: find movies whose rating patterns
    most closely resemble the favorite, and return the top N (excluding
    the favorite itself).
    """
    _load_data()

    movie_id = _find_movie_id_by_title(favorite_movie)
    if movie_id is None or movie_id not in _item_similarity.columns:
        return []

    similar = _item_similarity[movie_id].dropna()
    similar = similar.drop(labels=[movie_id], errors="ignore")

    if similar.empty:
        return []

    top_ids = similar.sort_values(ascending=False).head(top_n).index

    recommendations = []
    for other_id in top_ids:
        movie = get_movie(int(other_id))
        if movie:
            movie["similarity"] = round(float(similar.loc[other_id]), 3)
            recommendations.append(movie)
    return recommendations


def get_recommendations_for_user(
    name: str,
    age: int,
    favorite_genre: str = None,
    favorite_movie: str = None,
    top_n: int = 10,
):
    """Entry point for a brand-new user who just gives us their details
    instead of an existing MovieLens userId. Accepts either a favorite
    genre or a favorite movie (whichever the frontend collected) and
    routes to the matching recommender.

    `name` and `age` aren't used in the scoring (there's no data linking
    them to taste) — they're accepted so the API/frontend has a place to
    collect them and so this function is easy to extend later (e.g.
    age-appropriate filtering).
    """
    if favorite_movie:
        recommendations = get_recommendations_by_movie(favorite_movie, top_n=top_n)
        basis = {"favorite_movie": favorite_movie}
    elif favorite_genre:
        recommendations = get_recommendations_by_genre(favorite_genre, top_n=top_n)
        basis = {"favorite_genre": favorite_genre}
    else:
        recommendations = []
        basis = {}

    return {
        "user": {"name": name, "age": age, **basis},
        "recommendations": recommendations,
    }