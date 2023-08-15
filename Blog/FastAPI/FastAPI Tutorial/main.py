from fastapi import Security, Depends, FastAPI, HTTPException
from pydantic import BaseModel
from routers import gold, oil, movie, weather, trino, mongodb, mysql, postgres, hive, oracle
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

API_KEY = [
        'admin',
        'nook'
        ]
API_KEY_NAME = "apikey"
COOKIE_DOMAIN = "localhost"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

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

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query in API_KEY:
        return api_key_query
    elif api_key_header in API_KEY:
        return api_key_header
    elif api_key_cookie in API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="A key must be provided for the API."
        )

@app.get("/")
async def default(api_key: APIKey = Depends(get_api_key)):
        response = JSONResponse(
        (title="API Authentication Secure", version=1, routes=app.routes)
    )
        return response