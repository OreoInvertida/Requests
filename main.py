from fastapi import FastAPI
from routers.request_router import router as request_router
from database.mongodb import mongo

app = FastAPI(title="Requests Microservice")

@app.on_event("startup")
async def startup():
    await mongo.connect()

@app.on_event("shutdown")
async def shutdown():
    await mongo.close()

app.include_router(request_router, tags=["Requests"])
