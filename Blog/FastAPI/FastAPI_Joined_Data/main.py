from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
import pandas as pd
import uvicorn as server
import json

desc = '''
### การใช้งาน Group Data ไปยัง JSON เพื่อส่งข้อมูลให้ Frontend แบบ JSON Nested Join

---

* ```Database``` | Join Table ใน SQL แล้วนำมา Map เป็น rows JSON
* ```API``` | Read CSV, JSON แล้วนพมา Group เป็น rows JSON

---


```javascript
[
  {
    --------Group----------
    "status_code": 200,
    "dilution_group": "1/1",
    --------Group----------
    "result": [
      {
        "idx": 1,
        "dilution": "1/1",
        "n": 43,
        "y": 2
      },
      {
        "idx": 2,
        "dilution": "1/1",
        "n": 47,
        "y": 5
      }
    ]
  }
]
```

---

'''
app = FastAPI(
    title="Joined API JSON",
    description=desc,
    version=1.2
)

def connect():
    db = create_engine("mysql+pymysql://nook:2909@192.168.10.22/test")
    return db

@app.get("/get/database/result/fetch_all", tags=["Database Query"])
def db_query():
    sql = """
        SELECT
            a.id AS id,
            a.customer AS customer,
            a.site AS site,
            a.status_work as status_work,
            a.date_start AS `datetime`,
            e.id AS engineer_id,
            e.engineer_name AS engineer_name 
        FROM
            addjob a
            LEFT JOIN engineer AS e ON a.engineer = e.engineer_name
    """
    #อ่านจาก SQL Query Joined
    df = pd.read_sql(sql, connect())
    #Groupข้อมูลจาก Primary Table
    grouped = df.groupby(['engineer_id', 'engineer_name'])
    #Empty Dict
    grouped_data = []
    #Loop -> GroupBy, Result Data
    for (engineer_id, engineer_name), group_data in grouped:
        engineer_dict = {
            "status_code": 200,
            "engineer_id": engineer_id,
            "engineer_name": engineer_name,
            "jobs": group_data.to_dict(orient='records')
        }
        grouped_data.append(engineer_dict)
        
    return grouped_data
    

@app.get("/get/api/result/fetch_all", tags=["API Result"])
def api_query():
    df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/aod/orob1.csv", encoding='utf-8')
    df = df.rename(columns={"Unnamed: 0":"idx"})
    grouped = df.groupby('dilution')
    grouped_data = []
    
    for group_name, group_data in grouped:
        mydict = {
            "status_code": 200,
            "dilution_group": group_name,
            "result": group_data.to_dict(orient='records')
        }
        grouped_data.append(mydict)
    return grouped_data


'''--------------Run Server in Uvicorn------------------------'''
if __name__ == "__main__":
    server.run("main:app", host="0.0.0.0", port=8000, reload=True)