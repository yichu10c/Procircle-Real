"""
Garbage Collector
"""
import enum
import gc
import time
import worker
from worker import ThreadWorker

from tools.observability.log import main_logger

class GarbageCollectorType(enum.Enum):
    MINOR: int = 0
    MAJOR: int = 2


def periodic_garbage_collector(gctype: GarbageCollectorType, period: float) -> ThreadWorker:
    @worker.worker
    def run_periodic_gc():
        if not period:
            raise ValueError("period cannot be zero")
        main_logger.info(f"{gctype.name} GARBAGE COLLECTOR INSTANTIATED")
        while True:
            time.sleep(period)
            potential_garbage = sum(gc.get_count()[:gctype.value + 1])
            main_logger.debug(f"{gctype.name} GC is collecting {potential_garbage} potential garbage")
            gc.collect(gctype.value)
    return run_periodic_gc()
