#pip install "fastapi[all]"
#pip install "uvicorn[standard]"
#pip install trino
from fastapi import *
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from trino.dbapi import connect
import pandas as pd
import json

description = """
## [API Authentication with APIKey]
        - APIKey for authentication, please contact us Softnix Team
        - for test
            15869221d3a0a96ebd75aeb144e20259

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
API_KEY = [
        '15869221d3a0a96ebd75aeb144e20259'
        ]
API_KEY_NAME = "apikey"
COOKIE_DOMAIN = "localhost"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
# api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_query: str = Security(api_key_query)
    # api_key_header: str = Security(api_key_header),
    # api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query in API_KEY:
        return api_key_query
    # elif api_key_header in API_KEY:
    #     return api_key_header
    # elif api_key_cookie in API_KEY:
    #     return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="A key must be provided for the API."
        )

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
async def trinoQuery(table: str, skip: int = 0, limit: int = 10, where = None, api_key: APIKey = Depends(get_api_key)):
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

@app.get("/list_schema_table/", tags=["List Schema Table"])
async def getSchema(type: str = Query(enum=["TABLES", "SCHEMAS"]), filter: str = "default", api_key: APIKey = Depends(get_api_key)):
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
