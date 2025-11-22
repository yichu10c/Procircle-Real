"""
Logging Handler
"""
import logging
import logging.handlers
import os
import uuid

from chain_logging.fastapi import get_chained_logger as get_logger
from chain_logging.base import ChainFilter, ChainLogger


log_filter = ChainFilter(id_generator=lambda: uuid.uuid4().hex)

main_logger = ChainLogger(
    name="ProCircleAppLogger",
    filter_object=log_filter
)

log_file_handler = logging.handlers.RotatingFileHandler(
    filename=os.environ["LOG_PATH"].format(os.environ["SERVICE_NAME"]),
    maxBytes=int(os.environ["LOG_MAX_SIZE_BYTES"]),
    backupCount=int(os.environ["LOG_MAX_BACKUP"]),
)
log_file_handler.setFormatter(logging.Formatter(log_filter._log_format))
main_logger.addHandler(log_file_handler)