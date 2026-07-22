import stripe


class StripeClient:

    def __init__(self, api_key: str):

        stripe.api_key = api_key

    def customer(self, customer_id: str):
        return stripe.Customer.retrieve(customer_id)

    def payment(self, payment_id: str):
        return stripe.PaymentIntent.retrieve(payment_id)

    def create_customer(
        self,
        email: str,
        name: str,
    ):

        return stripe.Customer.create(
            email=email,
            name=name,
        )
