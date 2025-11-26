from typing import Protocol, TypeVar, Generic, Self, runtime_checkable
import json


@runtime_checkable
class Serializable(Protocol):
    def get_u_id(self) -> str: ...
    def to_json(self) -> dict: ...
    
    @classmethod
    def from_json(cls, data: dict) -> Self: ...


T = TypeVar("T", bound=Serializable)

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def save(self, obj: T): ...
    def query(self, u_id: str) -> T: ...



class RepositoryWithCache(Generic[T]):
    def __init__(self, cache, rep: BaseRepository[T]):
        self.cache = cache
        self.rep = rep

    def save(self, obj: T):
        self.rep.save(obj)
        self.cache.clear(obj.get_u_id())

    def query(self, u_id: str) -> T:
        cache_str = self.cache.get(u_id)
        
        if cache_str is None:
            obj = self.rep.query(u_id)
            if obj:
                self.cache.set(u_id, json.dumps(obj.to_json()))
            return obj
        
        return self.rep.model.from_json(json.loads(cache_str))
