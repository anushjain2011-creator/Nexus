from __future__ import annotations

from pathlib import Path

from nexus.talent.candidate import Candidate
from nexus.talent.resume import Resume


class ResumeParser:

    def parse(
        self,
        resume: Resume,
    ) -> Candidate:

        text = self.read(
            resume.path
        )

        return self.extract(
            text,
            resume.path,
        )

    def read(
        self,
        path: str,
    ) -> str:

        file = Path(path)

        suffix = file.suffix.lower()

        if suffix in {".txt", ".md"}:
            return file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        raise NotImplementedError(
            f"{suffix} files are not supported yet."
        )

    def extract(
        self,
        text: str,
        path: str,
    ) -> Candidate:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        name = lines[0] if lines else "Unknown"

        parts = name.split(
            maxsplit=1
        )

        first = parts[0]

        last = parts[1] if len(parts) > 1 else ""

        return Candidate(
            id=Path(path).stem,
            first_name=first,
            last_name=last,
            summary=text,
            resume_path=path,
        )
