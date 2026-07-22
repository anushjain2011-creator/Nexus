from __future__ import annotations

import hashlib


def candidate_id(
    value: str,
) -> str:

    return hashlib.sha256(
        value.encode()
    ).hexdigest()


def normalize(
    value: str,
) -> str:

    return " ".join(
        value.lower().split()
    )
