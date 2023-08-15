from fastapi import APIRouter
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json 
import datetime

router = APIRouter(
    prefix="/weather",
    tags=["สภาพอากาศรายวัน"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/")
async def weather():
    today = datetime.datetime.now()
    now = today.strftime('%d-%m-%Y %H:%M:%S')
    url= "https://www.tmd.go.th/region.php?RegionID=3"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('table', class_='Panel')
    dataframe = []

    weather = soup.find('td', class_='PM').text.replace('\r\n','')
    all_data = {"province": 'Bangkok',"weather": weather,"update_dt": now}
    return all_data