from __future__ import annotations

from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    def save(self, key: str, value):
        raise NotImplementedError

    @abstractmethod
    def load(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def exists(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def keys(self):
        raise NotImplementedError
