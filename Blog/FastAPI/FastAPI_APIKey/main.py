#pip install "fastapi[all]"
#pip install "uvicorn[standard]"
#pip install trino
from fastapi import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from trino.dbapi import connect
import pandas as pd
import json

description = """
## [API Authentication with Basic Auth]
        - Username and password for authentication, please contact us Softnix Team
        - for test
            [admin, admin]

## [Query Trino]
    - table = schema.table หากไม่กรอก schema จะเป็น default.table
    - skip = offset ค่าเริ่มต้นคือ 0
    - limit = limit ค่าเริ้มต้นคือ 10

## [List Schemas Tables]
    - type
        - เลือก SCHEMAS (ไม่จำเป็นต้องใส่ค่า filter) คือ แสดง Databases ทั้งหมด
        - เลือก Tables คือ แสดง Tables ทั้งหมด ที่กรอกใน filter หากไม่กรอกจะมีค่าเริ่มต้นเป็น default
    - filter = SCHEMAS
"""

app = FastAPI(
    prefix="/trino",
    title="Softnix API",
    description=description,
    tags=["TrinoDB Query"],
    responses={404: {"message": "Not found"}}
)

security = HTTPBasic()

userData = {
    'admin':'admin',
    'hive':'hive',
    'softnix':'softnixteam'
}

def dbCon():
    conn = connect(
            host="192.168.10.40",
            port=8090,
            user="hive",
            catalog="hive",
            schema="default",
        )
    return conn

@app.get("/read/", tags=["Query Trino"])
async def trinoQuery(table: str, skip: int = 0, limit: int = 10, where = None, credentials: HTTPBasicCredentials = Depends(security)):
    val_user = credentials.username.strip()
    val_pass = credentials.password.strip()
    if val_user in userData and val_pass in userData[val_user]:
        if not where:
            where = None
        else:
            where = f"WHERE {where}"
        tables = table.split(".")
        if len(tables) != 2:
            table_f = f"default.{table}"
        else:
            table_f = table

        df = pd.read_sql(f"""
                        SELECT
                            *
                        FROM
                            hive.{table_f}
                        {where}
                        OFFSET {skip} LIMIT {limit}
                    """,dbCon())
        res = df.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    else:
        return {"message": "Not authenticated"}

@app.get("/list_schema_table/", tags=["List Schema Table"])
async def getSchema(type: str = Query(enum=["TABLES", "SCHEMAS"]), filter: str = "default", credentials: HTTPBasicCredentials = Depends(security)):
    val_user = credentials.username.strip()
    val_pass = credentials.password.strip()
    if val_user in userData and val_pass in userData[val_user]:
        if type == "SCHEMAS":
            df = pd.read_sql(f"SHOW SCHEMAS",dbCon())
        else:
            df = pd.read_sql(f"""
                        SELECT
                            table_schema,
                            table_name
                        FROM
                            hive.information_schema.tables 
                        WHERE
                            table_schema = '{filter}'
                    """,dbCon())
        res = df.to_json(orient="records")
        parsed = json.loads(res)
        return parsed
    else:
        return {"message": "Not authenticated"}
