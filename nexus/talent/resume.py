from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from nexus.talent.candidate import Candidate


@dataclass
class Resume:

    path: str

    raw_text: str = ""

    filename: str = ""

    parsed: bool = False

    metadata: dict = field(default_factory=dict)

    def __post_init__(self):

        if not self.filename:
            self.filename = Path(self.path).name

    def exists(self) -> bool:

        return Path(self.path).exists()

    def load(self) -> str:

        path = Path(self.path)

        self.raw_text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return self.raw_text

    def set_text(
        self,
        text: str,
    ):

        self.raw_text = text

    def parse(
        self,
        parser,
    ) -> Candidate:

        candidate = parser.parse(self)

        self.parsed = True

        return candidate

    def word_count(self) -> int:

        return len(
            self.raw_text.split()
        )

    def to_dict(self):

        return {
            "path": self.path,
            "filename": self.filename,
            "parsed": self.parsed,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(**data)
