from slack_sdk import WebClient


class SlackClient:

    def __init__(self, token: str):
        self.client = WebClient(token=token)

    def send_message(
        self,
        channel: str,
        text: str,
    ):

        return self.client.chat_postMessage(
            channel=channel,
            text=text,
        )
