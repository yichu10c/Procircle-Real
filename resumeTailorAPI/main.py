
from fastapi import FastAPI
from inbound.endpoints import router as inbound_router

app = FastAPI()
app.include_router(inbound_router)
