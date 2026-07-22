from dataclasses import dataclass


@dataclass(slots=True)
class Repository:

    name: str

    owner: str

    private: bool
