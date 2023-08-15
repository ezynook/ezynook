from fastapi import *
from trino.dbapi import connect
from fastapi.responses import RedirectResponse
import pandas as pd
import json
import redis

#Caching in Redis 
rd = redis.Redis(host='localhost', port=6379, decode_responses=True)

description = """
## [Query]
    - table = schema.table หากไม่กรอก schema จะเป็น default.table
    - skip = offset ค่าเริ่มต้นคือ 0
    - limit = limit ค่าเริ้มต้นคือ 10
    - count = True นับข้อมูลทั้งหมดใน Table / False Fetch Row

## [List Schemas Tables]
    - type
        - เลือก SCHEMAS (ไม่จำเป็นต้องใส่ค่า filter) คือ แสดง Databases ทั้งหมด
        - เลือก Tables คือ แสดง Tables ทั้งหมด ที่กรอกใน filter หากไม่กรอกจะมีค่าเริ่มต้นเป็น default
    - filter = SCHEMAS
## [List Field Tables]
    - เลือก SCHEMAS และ TABLE (reqiured)
"""

app = FastAPI(
    prefix="/trino",
    title="Softnix Technology",
    description=description,
    tags=["DataLake API"],
    responses={404: {"message": "Not found"}}
)

def dbCon():
    try:
        conn = connect(
                host="192.168.10.210",
                port=8090,
                user="hive",
                catalog="hive",
                schema="default",
        )
    except:
        conn = connect(
                host="192.168.10.40",
                port=8090,
                user="hive",
                catalog="hive",
                schema="default",
        )
    return conn

@app.get("/", include_in_schema=False)
async def index():
    try:
        return RedirectResponse('/docs')
    except:
        return {"message": "Unable to connect to Data Lake, please contact Softnix Support."}

@app.get("/version", include_in_schema=False)
async def version():
    return {"message": "Last build: 2023-08-03 14:20"}

@app.get("/read/", tags=["Query"])
async def trinoQuery(table: str, skip: int = 0, limit: int = 10, where = None, count: bool = Query(enum=[False, True])):
    cache_name = str(table)+"_"+str(skip)+"_"+str(limit)+"_"+str(where)+"_"+str(count)
    cache = rd.get(cache_name)
    if cache:
        return json.loads(cache)
    else:
        if not where:
            where = None
        else:
            where = f"WHERE {where}"
        tables = table.split(".")
        if len(tables) != 2:
            table_f = f"default.{table}"
        else:
            table_f = table
        if count == True:
            count_val = 'COUNT(*) AS count_data'
        else:
            count_val = '*'

        df = pd.read_sql(f"""
                        SELECT
                            {count_val}
                        FROM
                            hive.{table_f}
                        {where}
                        OFFSET {skip} LIMIT {limit}
                    """,dbCon())
        res = df.to_json(orient="records")
        rd.setex(cache_name, 1800, res)
        parsed = json.loads(res)
        return parsed

@app.get("/list_schema_table/", tags=["List Schema Table"])
async def getSchema(type: str = Query(enum=["TABLES", "SCHEMAS"]), filter: str = "default"):
    cache_name = str(type)+"_"+str(filter)
    cache = rd.get(cache_name)
    if cache:
        return json.loads(cache)
    else:
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
        rd.setex(cache_name, 1800, res)
        parsed = json.loads(res)
        return parsed

@app.get("/list_field/", tags=["List Field Columns"])
async def getField(schema: str, table: str):
    cache_name = str(schema)+"_"+str(table)
    cache = rd.get(cache_name)
    if cache:
        return json.loads(cache)
    else:
        if not schema:
            return {"message": "invalid schema values"}

        if not table:
            return {"message": "invalid table values"}

        df = pd.read_sql(f"""
                        DESCRIBE hive.{schema}.{table}
                    """,dbCon())
        df.drop(['Extra','Comment'], axis = 1, inplace = True)
        res = df.to_json(orient="records")
        rd.setex(cache_name, 1800, res)
        parsed = json.loads(res)
        return parsed