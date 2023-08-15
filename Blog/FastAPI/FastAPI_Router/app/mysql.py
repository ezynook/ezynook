from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql as pymysql
from urllib.parse import quote

router = APIRouter(
    prefix="/mysql",
    tags=["ดึงข้อมูลจาก MySQL"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/{limit_row}")
async def mysql(limit: int):
    con = create_engine('mysql+pymysql://root:%s@192.168.10.21/hotspot' % quote('P@ssw0rd'))
    df = pd.read_sql("SELECT * FROM hotspot LIMIT " + str(limit),con)
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed