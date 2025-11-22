"""
Logging Middleware
"""
from typing import List

from chain_logging.fastapi import ChainLoggerMiddleware
from fastapi import FastAPI, Request, Response

from tools.observability.log import main_logger, get_logger, log_file_handler


class LoggingMiddleware(ChainLoggerMiddleware):
    def __init__(self, app: FastAPI, ignored_prefixes: List[str] = []):
        super().__init__(
            app,
            logger=main_logger,
            before_request=self.before_request_call,
            after_request=self.after_request_call
        )
        self.ignored_prefixes = ignored_prefixes

    async def before_request_call(self, request: Request):
        if self.is_ignored(request):
            return
        logger = await get_logger(request)
        logger.addHandler(log_file_handler)
        logger.info(f"Received {request.method} {request.url.path}")

    async def after_request_call(self, request: Request, response: Response):
        if self.is_ignored(request):
            return
        logger = await get_logger(request)
        logger.info(f"Request done in {logger.time_elapsed}ms")

    def is_ignored(self, request: Request) -> bool:
        path = str(request.url)
        for prefix in self.ignored_prefixes:
            if prefix in path:
                return True
        return False