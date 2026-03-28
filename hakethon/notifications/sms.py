"""
SMS Provider abstraction.
Supports: console (dev), Fast2SMS, Twilio.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_otp_sms(phone, otp_code):
    message = f"KaamSetu OTP: {otp_code}. Valid for 10 minutes. Do not share with anyone."
    _send(phone, message, 'otp')


def send_job_alert_sms(phone, job_title, location, rate):
    message = f"KaamSetu: New job near you! {job_title} at {location}. Rate: Rs.{rate}/day. Open app to apply."
    _send(phone, message, 'job_alert')


def send_hired_sms(phone, job_title, contractor_name, start_date):
    message = f"Congrats! You're hired for {job_title} by {contractor_name}. Start: {start_date}. Open KaamSetu for details."
    _send(phone, message, 'hired')


def send_urgent_broadcast_sms(phone, job_title, location, rate):
    message = f"URGENT JOB TODAY: {job_title} at {location}. Rs.{rate}/day. Apply NOW on KaamSetu."
    _send(phone, message, 'urgent')


def _send(phone, message, msg_type):
    provider = getattr(settings, 'SMS_PROVIDER', 'console')

    if provider == 'console':
        logger.info(f"[SMS Console] To: {phone} | {msg_type}: {message}")
        print(f"\n📱 SMS to {phone}: {message}\n")
        return True

    elif provider == 'fast2sms':
        try:
            import requests
            resp = requests.post(
                'https://www.fast2sms.com/dev/bulkV2',
                headers={'authorization': settings.FAST2SMS_API_KEY},
                json={'route': 'q', 'message': message, 'language': 'english', 'numbers': phone},
                timeout=5
            )
            return resp.json().get('return', False)
        except Exception as e:
            logger.error(f"Fast2SMS error: {e}")
            return False

    elif provider == 'twilio':
        try:
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(body=message, from_=settings.TWILIO_PHONE_NUMBER, to=f'+91{phone}')
            return True
        except Exception as e:
            logger.error(f"Twilio error: {e}")
            return False

    return False
