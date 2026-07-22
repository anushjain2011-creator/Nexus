from __future__ import annotations

from .json import JSONStorage


class StorageManager:

    def __init__(self):

        self.provider = JSONStorage()

    def register(
        self,
        provider,
    ):

        self.provider = provider

    def save(
        self,
        key,
        value,
    ):

        self.provider.save(
            key,
            value,
        )

    def load(
        self,
        key,
    ):

        return self.provider.load(
            key,
        )

    def delete(
        self,
        key,
    ):

        self.provider.delete(
            key,
        )

    def exists(
        self,
        key,
    ):

        return self.provider.exists(
            key,
        )

    def keys(self):

        return self.provider.keys()


storage_manager = StorageManager()
