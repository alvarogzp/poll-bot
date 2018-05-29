from typing import Callable

from poll.inject.injector.cache import InjectorCache


class BaseInjector:
    def __init__(self, cache: InjectorCache):
        self.cache = cache

    def _cache(self, key, create_func: Callable):
        if self.cache.is_cached(key):
            return self.cache.get(key)
        value = create_func()
        self.cache.set(key, value)
        return value
