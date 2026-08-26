from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import recommender

app = FastAPI()          

app.add_middleware(       
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    name: str
    age: int
    favorite_genre: Optional[str] = None
    favorite_movie: Optional[str] = None

@app.get("/genres")
def list_genres():
    return recommender.get_available_genres()


@app.get("/movies/search")
def search_movies(query: str):
    return recommender.search_movies(query)

@app.post("/recommend")
def recommend_for_user(profile: UserProfile):
    return recommender.get_recommendations_for_user(
        name=profile.name,
        age=profile.age,
        favorite_genre=profile.favorite_genre,
        favorite_movie=profile.favorite_movie
    )
