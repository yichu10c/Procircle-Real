# load env
from dotenv import load_dotenv
load_dotenv()

# Set service name for logging
import os
os.environ["SERVICE_NAME"] = "application"

# Import frameworks and modules
from fastapi import APIRouter, FastAPI
from app.tools.middleware.cors import CORSMiddleware
from app.tools.middleware.log import LoggingMiddleware
from app.utils.exceptions import exception_handler
from app.utils.lifecycle import healthcheck, lifespan
from app.views.v1 import asset_view, job_view as job_view_v1, user_view, li_profile_view
from app.views.v2 import job_view as job_view_v2

# instantiate app
app = FastAPI(lifespan=lifespan)

# add health check
app.get("/healthcheck")(healthcheck)

# add middleware
app.add_middleware(LoggingMiddleware, ignored_prefixes=["/healthcheck"])
app.add_middleware(CORSMiddleware)

# register v1 routers
router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(user_view.router, tags=["V1 Users"])
router_v1.include_router(asset_view.router, tags=["V1 Assets"])
router_v1.include_router(job_view_v1.router, tags=["V1 Jobs"])
router_v1.include_router(li_profile_view.router, tags=["V1 Profiles"])

# register v2 routers
router_v2 = APIRouter(prefix="/v2")
router_v2.include_router(job_view_v2.router, tags=["V2 Jobs"])

# register router to app
app.include_router(router_v1)
app.include_router(router_v2)

# add exception handlers
app.add_exception_handler(Exception, exception_handler)
