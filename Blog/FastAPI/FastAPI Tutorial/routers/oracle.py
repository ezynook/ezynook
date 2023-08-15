from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import cx_Oracle
import json

router = APIRouter(
    prefix="/oracle",
    tags=["ดึงข้อมูลจาก Oracle"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/{limit_row}")
async def oracle(limit: int):
    conn = cx_Oracle.connect('username/password@10.31.1.69:1521/schema')
    # cursor = db.cursor()
    # cursor.execute(f"SELECT *  FROM table")
    # arr = []
    # for row in cursor:
    #     arr.append(row)
    df = pd.read_sql("SELECT * FROM schema.table", conn)
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed
    