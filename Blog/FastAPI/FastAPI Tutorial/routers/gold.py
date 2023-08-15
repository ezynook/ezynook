from fastapi import Security, Depends, FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json 
from datetime import date
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

router = APIRouter(
    prefix="/gold",
    tags=["ราคาทองคำรายวัน"],
    responses={404: {"message": "Not found"}}
)
###########Authentication By APIKey###############
API_KEY = [
        'admin',
        'nook'
        ]
API_KEY_NAME = "apikey"
COOKIE_DOMAIN = "localhost"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)
async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query in API_KEY:
        return api_key_query
    elif api_key_header in API_KEY:
        return api_key_header
    elif api_key_cookie in API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="A key must be provided for the API."
        )
###########Authentication By APIKey###############
@router.get("/")
async def gold(api_key: APIKey = Depends(get_api_key)):
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