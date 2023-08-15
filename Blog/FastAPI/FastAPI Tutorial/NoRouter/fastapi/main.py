from fastapi import FastAPI,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
import json

app = FastAPI()
security = HTTPBasic()

@app.get("/")
async def index(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == 'nook' and credentials.password == 'nook':
        return {'message': 'welcome index API'}
    else:
        exit


@app.get("/user/id={user_id}&user={user_name}")
async def get_user(user_id, user_name):
    return user_id + ' ' + user_name

@app.get("/covid/{type}")
async def covid_today(type):
    if type == 'today':
        df = pd.read_json("https://covid19.ddc.moph.go.th/api/Cases/today-cases-all")
    elif type == 'province':
        df = pd.read_json("https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces")
    else:
        exit
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed