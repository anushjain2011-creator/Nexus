from __future__ import annotations

from .base import RecruitingProvider


class RecruitingManager:

    def __init__(self):

        self._providers: dict[
            str,
            RecruitingProvider,
        ] = {}

    def register(
        self,
        provider: RecruitingProvider,
    ):

        self._providers[
            provider.name
        ] = provider

    def unregister(
        self,
        name: str,
    ):

        self._providers.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ):

        return self._providers.get(
            name
        )

    def providers(self):

        return list(
            self._providers.values()
        )

    def names(self):

        return list(
            self._providers.keys()
        )

    def clear(self):

        self._providers.clear()
