from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql as pymysql
from urllib.parse import quote
#pip install psycopg2
router = APIRouter(
    prefix="/postgres",
    tags=["ดึงข้อมูลจาก PostgreSQL"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/{limit_row}")
async def postgres(limit: int):
    con = create_engine("postgresql://postgres:%s@192.168.10.21/airflow" % quote('postgres'))
    df = pd.read_sql("SELECT * FROM public.job LIMIT " + str(limit),con)
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed