"""
CORS Middleware
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as BaseCORSMiddleware


class CORSMiddleware(BaseCORSMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(
            app,
            allow_origins=[
                "http://localhost",
                "http://localhost:8000",
		        "http://localhost:3000",
                "https://procircle-fe-next-dev.vercel.app",
                "https://procircle-fe-next-prod.vercel.app",
                "https://procircle-fe-next.vercel.app",
                "https://ec2-18-119-114-50.us-east-2.compute.amazonaws.com",
                "https://ec2-18-119-114-50.us-east-2.compute.amazonaws.com:8000",
                "http://api.procircle.ai",
                "http://api.procircle.ai:8000",
                "http://ec2-3-12-74-254.us-east-2.compute.amazonaws.com",
                "http://ec2-3-12-74-254.us-east-2.compute.amazonaws.com:8000",
                "http://ec2-52-221-221-213.ap-southeast-1.compute.amazonaws.com",
                "http://ec2-52-221-221-213.ap-southeast-1.compute.amazonaws.com:8000",
                "http://ec2-3-22-99-130.us-east-2.compute.amazonaws.com",
                "http://ec2-3-22-99-130.us-east-2.compute.amazonaws.com:8000",
		        "https://resume-review-web-app.vercel.app",
                "https://dev-api-pc.mms-internal.my.id",
                "https://resume-analysis.procircle.ai",
                "https://procircle.ai",
            ],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
            allow_origin_regex=None,
            expose_headers=None,
            max_age=300
        )
