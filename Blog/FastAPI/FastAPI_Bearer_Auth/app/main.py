'''
  _____             _  _    __     __
 |  __ \           (_)| |   \ \   / /
 | |__) |__ _  ___  _ | |_   \ \_/ / 
 |  ___// _` |/ __|| || __|   \   /  
 | |   | (_| |\__ \| || |_     | | _ 
 |_|    \__,_||___/|_| \__|    |_|(_)   
 -----------------------------------------------------
 Last Deploy: 2023-07-25
 Author: Pasit Yodsoi Softnix.Co.,ltd | Data Engineer                            
 -----------------------------------------------------
'''
from fastapi import *
from fastapi.security import *
from pydantic import BaseModel
from sqlalchemy import create_engine
import pandas as pd
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json, secrets, string, os, requests
from fastapi.responses import HTMLResponse

description = """
Example Description By Pasit Yodsoi
Last Builded: 2023-07-24 16:00
"""

app = FastAPI(
    title="Pasit API",
    description=description,
    tags=["Example Auth Bearer"],
    responses={404: {"message": "Not found"}},
    swagger_ui_parameters={"defaultModelsExpandDepth": 0}
)
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

'''
Database Connect (SQLite) เชื่อมต่อแบบ 
Absoluth path: sqlite:////path/to/temp.db
'''
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, "temp.db")
conn = create_engine(f"sqlite:///{db_file_path}")

'''
สุ่มออก Token keys สามารถเปลี่ยนแปลงจำนวนหลังได้ **(length=82)**
'''
def generate_token_key(length=82):
    characters = string.ascii_letters + string.digits
    token_key = ''.join(secrets.choice(characters) for _ in range(length))
    return token_key

'''
วนหา Token ใน Database ที่ต้องตรงกันเวลา User กรอกเข้ามา
'''
def auth_key():
    result = []
    for v in pd.read_sql("select token from tbl_token", conn).itertuples():
        result.append(v.token)
    return list(result)

'''
หน้าแรก Example
'''
@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def home():
    return """
        <div>
            <h1>Welcome to API Backend</h1>
            <hr>
            <p>กรุณาลงทะเบียนเพื่อรับ Bearer Token Keys เพื่อใช้งาน API</p>
            <a href="/docs">Go to Swagger ui</a>
        </div>
    """
    
'''
ค้นหา Token โดยระบุ Username ที่เคย Signin เข้ามาแล้ว (ส่วนนี้ไม่ต้อง Auth)
'''
@app.get("/get/token", tags=['Authorization'])
async def get_token(username: str):
    if username:
        try:
            token_key = conn.execute("SELECT * FROM tbl_token WHERE username = ?", (username,)).fetchone()[1]
            if token_key:
                return {"token":token_key}
        except TypeError:
            return {"message": "invalid username!"}
    else:
        return {"message": "invalid username!"}
    
'''
เพิ่ม Token keys โดยต้องระบุ Uusername เพื่อทำการ Register
'''
@app.post("/add/token", tags=['Authorization'])
async def add_token(username: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in auth_key():
        return {"detail": "Not authenticated"}
    else:
        token_key = generate_token_key()
        username = username.strip()
        if username:
            if conn.execute(f"SELECT COUNT(*) as total FROM tbl_token WHERE username = '{username}'").fetchone()[0] == 0:
                conn.execute(f"INSERT INTO tbl_token (token, username) VALUES ('{token_key}','{username}')")
                return {
                    "username": username,
                    "token": token_key
                }
            else:
                conn.execute(f"UPDATE tbl_token SET token = '{token_key}' WHERE username = '{username}'")
                return {
                    "username": username,
                    "token": token_key
                }
        else:
            return {"message": "no user name entered!"}
        
'''
ข้อมูลตัวอย่างจาก Open-Data
'''
@app.get("/get/data/example", tags=['Example Data'])
async def get_data_example(limit: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in auth_key():
        return {"detail": "Not authenticated"}
    else:
        df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv", encoding='utf-8')
        df = df.rename(columns={"Unnamed: 0":"idx"})
        df = df[:limit]
        result_data = df.to_json(orient='records')
        parsed = json.loads(result_data)
        return {
            "status_code": 200,
            "result": parsed
        }
'''
Get Engineer Job By API
'''
@app.get("/get/engineer/data", tags=["Example Data"])
async def get_engineer():
    r = requests.get("http://engineer.da.co.th/api_json.php?all")
    result = json.loads(r.text)[:100]
    return result
 
'''
Runnign Server in Uvicorn
'''
# if __name__ == '__main__':
#     uvicorn.run(
#                 "main:app",
#                 port=3000,
#                 log_level="info",
#                 reload=True,
#                 host="0.0.0.0"
#     )
