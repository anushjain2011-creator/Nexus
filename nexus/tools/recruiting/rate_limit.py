from __future__ import annotations

import time


class RateLimiter:

    def __init__(
        self,
        requests_per_second: float = 2,
    ):

        self.delay = 1 / requests_per_second

        self.last_request = 0.0

    def wait(self):

        now = time.time()

        elapsed = now - self.last_request

        if elapsed < self.delay:

            time.sleep(
                self.delay - elapsed
            )

        self.last_request = time.time()
