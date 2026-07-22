from __future__ import annotations

import time


class Cache:

    def __init__(self):

        self._cache = {}

    def get(
        self,
        key,
    ):

        item = self._cache.get(key)

        if item is None:
            return None

        value, expires = item

        if expires < time.time():

            del self._cache[key]

            return None

        return value

    def set(
        self,
        key,
        value,
        ttl: int = 300,
    ):

        self._cache[key] = (
            value,
            time.time() + ttl,
        )

    def clear(self):

        self._cache.clear()
