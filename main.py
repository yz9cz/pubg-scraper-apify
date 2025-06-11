from fastapi import FastAPI, Query
from pydantic import BaseModel
from scraper import get_pubg_name

app = FastAPI()

class PUBGResponse(BaseModel):
    player_id: str
    player_name: str | None
    status: str

@app.get("/get_pubg_name", response_model=PUBGResponse)
def fetch_name(player_id: str = Query(..., description="معرف لاعب PUBG")):
    player_name = get_pubg_name(player_id)
    return PUBGResponse(
        player_id=player_id,
        player_name=player_name,
        status="success" if player_name else "not_found"
    )
