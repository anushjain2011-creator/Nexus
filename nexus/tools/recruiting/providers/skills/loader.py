from __future__ import annotations

import importlib
import pkgutil

import nexus.skills.builtin


class SkillLoader:

    def load_builtin(self):

        package = nexus.skills.builtin

        for _, module, _ in pkgutil.iter_modules(
            package.__path__
        ):

            importlib.import_module(
                f"{package.__name__}.{module}"
            )
