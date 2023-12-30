import os

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')


def twilio_send_message(to: str, message: str) -> None:
    '''
    Send message to a Telegram user.

    Parameters:
        - to(str): sender whatsapp number in this whatsapp:+919558515995 form
        - message(str): text message to send

    Returns:
        - None
    '''
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=os.getenv('FROM'),
        body=message,
        to=to
    )
