from fastapi import APIRouter
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import pandas as pd


router = APIRouter(
    prefix="/movie",
    tags=["รายชื่อหนังใหม่ น่าดูประจำวัน"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/")
async def gold():
    URL = "https://www.037hdmovie.com/"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('div', attrs={'class': 'filmcontent'}) 
    quotes=[]

    for row in table.findAll('div',attrs = {'class':'moviefilm'}):
        quote = {}
        quote['movie_name'] = row.img['alt']
        # quote['link'] = row.a['href']
        quotes.append(quote)
    return quotes