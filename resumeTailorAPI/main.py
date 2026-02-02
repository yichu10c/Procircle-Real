
from fastapi import FastAPI
from src.inbound.endpoints import router as inbound_router
from src.database import init_db

# Initialize database on startup
init_db()

app = FastAPI()
app.include_router(inbound_router)
