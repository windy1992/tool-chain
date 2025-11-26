# coding: utf-8
from functools import wraps
from typing import Awaitable, Optional, ParamSpec, Protocol, Callable, TypeVar


class Cache(Protocol):
    async def get(self, key: str) -> str: ...
    async def set(self, key: str, value: str): ...
    async def clear(self, key: str): ...


T = TypeVar("T")
P = ParamSpec("P")


def cache_put(
    cache: Cache,
    key_func: Callable[..., str],
    load_func: Optional[Callable[[str], T]] = None,
    dump_func: Optional[Callable[[T], str]] = None,
):
    load = load_func or (lambda x: x)
    dump = dump_func or (lambda x: x)

    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = key_func(*args, **kwargs)

            cached = await cache.get(key)
            if cached is not None:
                return load(cached)

            result = await func(*args, **kwargs)

            if result is not None:
                await cache.set(key, dump(result))

            return result

        return wrapper

    return decorator


def cache_evict(
    cache: Cache,
    key_func: Callable[..., str],
):
    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = key_func(*args, **kwargs)

            result = await func(*args, **kwargs)

            await cache.clear(key)
            return result

        return wrapper
    return decorator