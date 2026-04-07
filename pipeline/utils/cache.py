import diskcache
from pipeline.config import settings


class ResponseCache:
    def __init__(self, cache_dir=None):
        cache_dir = cache_dir or settings.cache_dir
        self.cache = diskcache.Cache(str(cache_dir))
        self.enabled = settings.enable_cache

    def get(self, key: str):
        if not self.enabled:
            return None
        return self.cache.get(key)

    def set(self, key: str, value):
        if self.enabled:
            self.cache.set(key, value)

    def clear(self):
        self.cache.clear()
