from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.inbound.endpoints import router as inbound_router
from src.outbound.endpoints import router as outbound_router
from src.database import init_db

init_db()

app = FastAPI()
app.include_router(inbound_router)
app.include_router(outbound_router)
