

from python.cache.repository_with_cache import BaseRepository, RepositoryWithCache, Serializable

class User(Serializable):
    def __init__(self, u_id: str, name: str):
        self.u_id = u_id
        self.name = name

    def get_u_id(self) -> str:
        return self.u_id

    def to_json(self):
        return {"u_id": self.u_id, "name": self.name}

    @classmethod
    def from_json(cls, data):
        return cls(data["u_id"], data["name"])


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)


class Cache:
    def get(self, u_id: str) -> str:
        raise NotImplementedError

    def set(self, u_id: str, value: str):
        raise NotImplementedError

    def clear(self, u_id: str):
        raise NotImplementedError
    
cache: Cache = Cache()


if __name__ == 'main':
    user_repo = UserRepository()
    cache_repo = RepositoryWithCache(cache, user_repo)

    u = cache_repo.query("123")  # 类型自动推断为 User
