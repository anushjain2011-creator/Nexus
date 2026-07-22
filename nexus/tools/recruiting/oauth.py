from __future__ import annotations

import time


class OAuthToken:

    def __init__(
        self,
        access_token: str,
        expires_in: int,
        refresh_token: str | None = None,
    ):

        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = time.time() + expires_in

    @property
    def expired(self) -> bool:

        return time.time() >= self.expires_at


class OAuthManager:

    def __init__(self):

        self._tokens = {}

    def register(
        self,
        provider: str,
        token: OAuthToken,
    ):

        self._tokens[provider] = token

    def token(
        self,
        provider: str,
    ) -> OAuthToken | None:

        return self._tokens.get(provider)

    def access_token(
        self,
        provider: str,
    ) -> str | None:

        token = self.token(provider)

        if token is None:
            return None

        if token.expired:
            return None

        return token.access_token
