from __future__ import annotations

from datetime import datetime

from .manager import storage_manager


class SnapshotManager:

    def save_world(
        self,
        world,
    ):

        storage_manager.save(
            f"world_{datetime.utcnow().isoformat()}",
            world.to_dict(),
        )

    def load_world(
        self,
        key,
    ):

        return storage_manager.load(
            key,
        )
