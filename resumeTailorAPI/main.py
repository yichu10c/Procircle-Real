
from fastapi import FastAPI
from inbound.endpoints import router as inbound_router
from outbound.endpoints import router as outbound_router

app = FastAPI()
app.include_router(inbound_router)
app.include_router(outbound_router)
