from fastapi import APIRouter
from numpy import record
from pydantic import BaseModel
import json
import pandas as pd
from trino.dbapi import connect

router = APIRouter(
    prefix="/trino",
    tags=["ดึงข้อมูลจาก TrinoDB"],
    responses={404: {"message": "Not found"}}
)

@router.get("/{limit_row}")
async def trino(limit_row: int):
    row_set = str(limit_row)
    conn = connect(
        host="trino.mnre.go.th",
        port=80,
        user="hive",
        catalog="hive",
        schema="default",
    )
    df = pd.read_sql("SELECT * FROM hive.default.weatherquality LIMIT " + str(row_set),conn)
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed