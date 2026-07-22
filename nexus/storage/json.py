from __future__ import annotations

import json
from pathlib import Path

from .base import StorageProvider


class JSONStorage(StorageProvider):

    def __init__(
        self,
        directory: str = "data/storage",
    ):

        self.directory = Path(directory)

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(
        self,
        key: str,
    ) -> Path:

        return self.directory / f"{key}.json"

    def save(
        self,
        key: str,
        value,
    ):

        with self._path(key).open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                value,
                f,
                indent=2,
                default=str,
            )

    def load(
        self,
        key: str,
    ):

        path = self._path(key)

        if not path.exists():
            return None

        with path.open(
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def delete(
        self,
        key: str,
    ):

        path = self._path(key)

        if path.exists():
            path.unlink()

    def exists(
        self,
        key: str,
    ) -> bool:

        return self._path(key).exists()

    def keys(self):

        return [
            file.stem
            for file in self.directory.glob("*.json")
        ]
