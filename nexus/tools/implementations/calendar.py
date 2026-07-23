from nexus.tools.calendar.client import CalendarClient


def execute(method: str, **kwargs):
    client = CalendarClient()
    return getattr(client, method)(**kwargs)
