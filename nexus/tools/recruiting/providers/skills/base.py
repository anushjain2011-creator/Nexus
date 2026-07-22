from __future__ import annotations

from abc import ABC, abstractmethod


class Skill(ABC):

    name = ""

    description = ""

    @abstractmethod
    def execute(
        self,
        **kwargs,
    ):
        raise NotImplementedError
