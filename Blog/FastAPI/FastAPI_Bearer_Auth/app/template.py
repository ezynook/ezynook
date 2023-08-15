# @app.get("/template/")
# async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     return {"message": "You have access to the protected route!"+token}