from fastapi import FastAPI
from producer import start_producer, stop_producer
from src.interfaces.event import router_event

app = FastAPI()

app.include_router(router_event, prefix="/api/v1", tags=["events"])


@app.on_event("startup")
async def startup_event():
    await start_producer()


@app.on_event("shutdown")
async def shutdown_event():
    await stop_producer()
