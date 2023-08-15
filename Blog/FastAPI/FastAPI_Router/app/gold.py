from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json 
from datetime import date

router = APIRouter(
    prefix="/gold",
    tags=["ราคาทองคำรายวัน"],
    responses={404: {"message": "Not found"}}
)

@router.get("/")
async def gold():
    today = date.today()
    dt = today.strftime("%d-%m-%Y")
    url= "https://www.goldtraders.or.th/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('table', attrs={'style':'height:132px;width:100%;color:Black;'})
    dataframe = {}
    for list in data:
        gold1 = list.find('span', id="DetailPlace_uc_goldprices1_lblBLSell").text.replace('\n', '')
        gold2 = list.find('span', id="DetailPlace_uc_goldprices1_lblBLBuy").text.replace('\n', '')
        gold3 = list.find('span', id="DetailPlace_uc_goldprices1_lblOMSell").text.replace('\n', '')
        gold4 = list.find('span', id="DetailPlace_uc_goldprices1_lblOMBuy").text.replace('\n', '')
        dataframe = {
            "update_dt": dt,
            "gold_bar_sell": gold1,
            "gold_bar_buy": gold2,
            "gold_jewelry_sell": gold3,
            "gold_jewelry_buy": gold4,
        }
    return dataframe