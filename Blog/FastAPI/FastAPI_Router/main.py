import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from app import gold, oil, movie, weather, trino, mongodb, mysql, postgres, hive, oracle

app = FastAPI(
        title="Softnix API",
        description="Softnix Data Engineer Teams",
        version="2.0",
        terms_of_service="https://softnix.co.th",
)

app.include_router(gold.router)
app.include_router(oil.router)
app.include_router(movie.router)
app.include_router(weather.router)
app.include_router(trino.router)
app.include_router(mongodb.router)
app.include_router(mysql.router)
app.include_router(postgres.router)
app.include_router(hive.router)
app.include_router(oracle.router)


@app.get("/")
async def default():
       return {"message":"myFAST"}