class InjectorCache:
    def __init__(self):
        self.cache = {}

    def is_cached(self, key):
        return key in self.cache

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value
