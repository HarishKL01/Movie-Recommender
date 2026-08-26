from pydantic import BaseModel
from typing import List, Optional

class RecommendedMovie(BaseModel):
    id: int
    title: str
    genres: List[str]
    score: float
    recommended_because: Optional[str] = None
