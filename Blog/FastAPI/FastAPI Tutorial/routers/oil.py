from fastapi import APIRouter
from h11 import Data
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json 
from datetime import date

router = APIRouter(
    prefix="/oil",
    tags=["ราคาน้ำมัน ปตท. รายวัน"],
    responses={404: {"message": "Not found"}}
)

@router.get("/")
async def oil():
    today = date.today()
    url= "http://gasprice.kapook.com/gasprice.php"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('article', class_='gasprice ptt')
    dataframe = []

    for list in data:
        for lis in list.find_all('li'):
            names = lis.find('span').text
            price = lis.find('em').text
            dataframe.append({"Oil_type":names, "Price":price})
        return dataframe