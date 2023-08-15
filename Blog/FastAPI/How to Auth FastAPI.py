from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

API_KEY = ['1234','admin']
API_KEY_NAME = "api_key"
COOKIE_DOMAIN = "localhost"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

"""
FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
	- None คือปิดการใช้งานเข้าถึง
	- ถ้าจะให้เข้าถึงได้ให้ใส่ดังนี้ docs_url="/urlที่ต้องการ"
"""
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app = FastAPI()

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
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

#ใส่ params ใน Function
async def(api_key: APIKey = Depends(get_api_key)):
		response = JSONResponse(
	        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
	    )
	    return response
# Credit: https://nilsdebruin.medium.com/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
