from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel
import jwt, json, datetime, uvicorn, os

app = FastAPI()
secret_key = "my_secret_auth"

cur_path = os.getcwd()
conn = create_engine(f"sqlite:///{cur_path}\\token_db.db")

class User(BaseModel):
    user_id: int
    username: str

@app.post("/generate_token", tags=['Access Token'])
async def gen_token(Item: User):
    datetime_dt = (datetime.datetime.utcnow() + datetime.timedelta(days=3652)).strftime('%Y-%m-%dT%H:%M:%SZ')
    payload = {
        "user_id": int(Item.user_id),
        "username": str(Item.username),
        "exp": datetime_dt
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    if conn.execute(f"select count(*) from tbl_token where username = '{Item.username}'").fetchone()[0] == 0:
        conn.execute(f"""
                    INSERT INTO tbl_token (token, datetime,user_id, username)
                        VALUES ('{token}','{datetime_dt}','{Item.user_id}','{Item.username}')
                    """)
    else:
        return {
            "status_code": 200,
            "already_token": conn.execute(f"select token from tbl_token where username = '{Item.username}'").fetchone()[0]
        }
    return {
        "status_code": 200,
        "access_token": token,
        "user_id": Item.user_id,
        "username": Item.username
    }

@app.get("/get_token", tags=['Access Token'])
async def get_token(username: str):
    fetch_token = conn.execute(f"SELECT token FROM tbl_token WHERE username = '{username}'").fetchone()
    try:
        strToken = fetch_token[0]
        return {
            "status_code": 200,
            "access_token": strToken
        }
    except:
        return {
            "status_code": 401,
            "access_token": "not found token"
        }

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)