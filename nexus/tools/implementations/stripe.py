import os

from nexus.tools.stripe.client import StripeClient


def execute(method: str, **kwargs):
    client = StripeClient(api_key=os.environ.get("STRIPE_API_KEY"))
    return getattr(client, method)(**kwargs)
