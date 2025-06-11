# app.py

from fastapi import FastAPI, Query
from pydantic import BaseModel
from scraper import PUBGScraper

app = FastAPI(title="PUBG Player Name API")

scraper = PUBGScraper()

class PlayerRequest(BaseModel):
    player_id: str

@app.get("/")
def root():
    return {"message": "مرحباً بك في PUBG Name Scraper API"}

@app.get("/get_name")
def get_name(player_id: str = Query(..., min_length=9, max_length=10)):
    name = scraper.get_player_name(player_id)
    if name:
        return {"player_id": player_id, "name": name}
    return {"error": "تعذر العثور على اسم اللاعب"}
