from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from pymongo import MongoClient
from bson import json_util

router = APIRouter(
    prefix="/mongodb",
    tags=["ดึงข้อมูลจาก MongoDB"],
    responses={
            404: {"message": "Not found"}}
)

@router.get("/")
async def mongodb():
    mongo_client = MongoClient('mongodb://nook:2909@192.168.10.21:27017/test')
    db = mongo_client['test']
    result = db.test.find().limit(10)
    return json_util.dumps(result)