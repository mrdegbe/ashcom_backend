from twilio.rest import Client
import os

# Load from env vars
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv(
    "TWILIO_WHATSAPP_NUMBER"
)  # e.g., 'whatsapp:+14155238886'
TWILIO_SMS_NUMBER = os.getenv("TWILIO_SMS_NUMBER")  # e.g., '+1234567890'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_message(to: str, body: str):
    """
    Send a WhatsApp message using Twilio.
    `to` must be in format: 'whatsapp:+233xxxxxxx'
    """
    message = client.messages.create(
        body=body, from_=TWILIO_WHATSAPP_NUMBER, to=f"whatsapp:{to}"
    )
    return message.sid


def send_sms(to: str, body: str):
    """
    Send an SMS.
    `to` must be in E.164 format: '+233xxxxxxx'
    """
    message = client.messages.create(body=body, from_=TWILIO_SMS_NUMBER, to=to)
    return message.sid
