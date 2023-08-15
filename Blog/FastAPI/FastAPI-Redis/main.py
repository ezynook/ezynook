from fastapi import FastAPI
import redis as rd
import json
import pandas as pd

app = FastAPI()
redis = rd.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/")
async def index():
    parse = redis.get("index")
    if parse:
        return json.loads(parse)
    else:
        df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CPSSW04.csv", encoding='utf-8')
        raw = df.to_json(orient='records')
        redis.setex('index',5, raw)
        return json.loads(raw)
