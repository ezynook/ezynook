from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
from pyhive import hive

router = APIRouter(
    prefix="/hive",
    tags=["ดึงข้อมูลจาก Apache Hive"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/{limit_row}")
async def ApacheHive(limit: int):
    if limit == 0:
        filter = ''
    else:
        filter = 'LIMIT ' + str(limit)
    conn = hive.Connection(host="192.168.10.40", port=10000, username="hive")
    df = pd.read_sql(f"SELECT * FROM default.weatherquality {filter}",conn)
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed