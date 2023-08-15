from fastapi import APIRouter
from pydantic import BaseModel
import pyodbc 
import pandas as pd
import json

router = APIRouter(
    prefix="/mssql",
    tags=["ดึงข้อมูลจาก MSSQL"],
    responses={404: {"message": "Not found"}}
)
@router.get("/")
async def mssql():
    conn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                "Server=INTFPHDDB-DEV;"
                "Database=dexProjDb;"
                "UID=dlpoc;"
                "PWD=pocdlread@2022;")
    df = pd.read_sql("SELECT * FROM schema.table", conn)
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed
