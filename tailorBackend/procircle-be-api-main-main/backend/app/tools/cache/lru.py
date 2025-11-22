"""
LRU Cache Handler
"""
import inspect
import functools
import threading
import time
from typing import Any, Awaitable, Callable, Dict, List
from worker import worker

# dict used for LRU
__cache_items__: Dict[Any, Dict[str, Any]] = {}
__cache_ttl__: Dict[Any, Dict[str, List[float]]] = {}
__cache_size__: Dict[Any, int] = {}
__cache_lastkey__: Dict[Any, str] = {}
__cache_miss__: Dict[Any, int] = {}
__cache_hit__: Dict[Any, str] = {}
cachelock = threading.Lock()


def is_key_expired(fun: Callable | Awaitable, cache_key: str):
    cachelock.acquire(True)
    try:
        if fun not in __cache_items__:
            return True
        if cache_key not in __cache_items__[fun]:
            return True
        created_at, ttl = __cache_ttl__[fun][cache_key]
        expired = time.time() - created_at >= ttl
        overlimit = len(__cache_items__[fun]) > __cache_size__[fun]
        if expired or overlimit:
            __cache_items__[fun].pop(cache_key)
            __cache_ttl__[fun].pop(cache_key)
            __cache_size__.pop(fun)
            __cache_lastkey__.pop(fun)
        return expired
    finally:
        cachelock.release()


def count_cache_miss(fun: Awaitable | Callable):
    cachelock.acquire(True)
    if fun not in __cache_miss__:
        __cache_miss__[fun] = 0
    __cache_miss__[fun] += 1
    cachelock.release()


def count_cache_hit(fun: Awaitable | Callable):
    cachelock.acquire(True)
    if fun not in __cache_hit__:
        __cache_hit__[fun] = 0
    __cache_hit__[fun] += 1
    cachelock.release()


@worker
def insert_cache(
    fun: Awaitable | Callable,
    cache_key: str,
    cache_value: Any,
    ttl: float,
    max_size: int
):
    cachelock.acquire(True)
    try:
        if fun not in __cache_items__:
            __cache_items__[fun] = {}
            __cache_ttl__[fun] = {}

        if fun in __cache_size__:
            overlimit = len(__cache_items__[fun]) > __cache_size__[fun]
            if overlimit:
                __cache_items__[fun].pop(cache_key)
                __cache_ttl__[fun].pop(cache_key)
                __cache_size__.pop(fun)
                __cache_lastkey__.pop(fun)

        __cache_items__[fun][cache_key] = cache_value
        __cache_ttl__[fun][cache_key] = (time.time(), ttl)
        __cache_size__[fun] = max_size
        __cache_lastkey__[fun] = cache_key
    finally:
        cachelock.release()


def resolve_non_primitive_type(value: Any) -> Any:
    if isinstance(value, (int, float, bool, str, dict, list, tuple)):
        return value
    return f"{value.__class__}.nonprimitive"


def create_cache_key(
    primitive: bool,
    args: List[Any],
    kwargs: Dict[str, Any]
) -> str:
    candidate_args = tuple([resolve_non_primitive_type(v) for v in args]) if primitive else args
    candidate_kwargs = {k: resolve_non_primitive_type(v) for k, v in kwargs.items()} if primitive else kwargs
    return functools._make_key(candidate_args, candidate_kwargs, False)


def _wrapped(
    ttl: float,
    max_size: int,
    primitive: bool,
    fun: Awaitable | Callable,
    args: List[Any],
    kwargs: Dict[str, Any]
) -> Any:
    # no ttl means no cache
    if not ttl:
        return fun(*args, **kwargs)

    # handle cache
    cache_key = create_cache_key(primitive, args, kwargs)
    if is_key_expired(fun, cache_key):
        count_cache_miss(fun)
        result = fun(*args, **kwargs)
        insert_cache(fun, cache_key, result, ttl, max_size)
        return result
    else:
        count_cache_hit(fun)
        return __cache_items__[fun][cache_key]


async def _awrapped(
    ttl: float,
    max_size: int,
    primitive: bool,
    fun: Awaitable | Callable,
    args: List[Any],
    kwargs: Dict[str, Any]
):
    # no ttl means no cache
    if not ttl:
        return await fun(*args, **kwargs)

    # handle cache
    cache_key = create_cache_key(primitive, args, kwargs)
    if is_key_expired(fun, cache_key):
        count_cache_miss(fun)
        result = await fun(*args, **kwargs)
        insert_cache(fun, cache_key, result, ttl, max_size)
        return result
    else:
        count_cache_hit(fun)
        return __cache_items__[fun][cache_key]


def cache(ttl: float, max_size: int = 128, primitive: bool = True):
    """
    LRU (Least Recently Used) Cache Decorator

    Args:
    - ttl (float): TTL (time to leave) for cache to be expired
    - max_size (int): total unique cache key could be stored
    - primitive (bool): if true, any object passed as arguments will be converted into primitives type
        e.g.
        ```
        session = DummyClass() # non primitive
        session_primitived = str(type(session)) # primitived as string
        ```
    """
    def final_func(fun: Awaitable | Callable):
        if inspect.iscoroutinefunction(fun):
            async def wrapped(*args, **kwargs):
                return await _awrapped(ttl, max_size, primitive, fun, args, kwargs)
            return wrapped
        else:
            def wrapped(*args, **kwargs):
                return _wrapped(ttl, max_size, primitive, fun, args, kwargs)
            return wrapped
    return final_func
