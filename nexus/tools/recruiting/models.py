from dataclasses import dataclass


@dataclass
class ProviderJob:

    id: str

    title: str

    location: str

    company: str


@dataclass
class ProviderCandidate:

    id: str

    name: str

    profile_url: str

    source: str
