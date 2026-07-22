from datetime import datetime


class CalendarClient:

    def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
    ):

        return {
            "title": title,
            "start": start,
            "end": end,
        }
