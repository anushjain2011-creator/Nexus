from __future__ import annotations


class PermissionManager:

    def __init__(self):

        self._roles = {}

    def allow(
        self,
        role: str,
        action: str,
    ):

        self._roles.setdefault(
            role,
            set(),
        ).add(action)

    def revoke(
        self,
        role: str,
        action: str,
    ):

        self._roles.setdefault(
            role,
            set(),
        ).discard(action)

    def can(
        self,
        role: str,
        action: str,
    ) -> bool:

        return action in self._roles.get(
            role,
            set(),
        )
