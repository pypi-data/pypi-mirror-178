"""Utility functions for email sending."""
import logging
import smtplib
import sys

from urllib.parse import urlparse
from email.message import EmailMessage

LOGGER = logging.getLogger(__name__)


def prepare_message(settings, addr_to, subject):
    """Prepares an email message with the right headers.

    The body of the message can be set by using
    :meth:`~email.message.EmailMessage.set_content` on the returned message.

    :param settings: The application settings, used to access the email
        specific settings.
    :type settings: dict
    :param addr_to: Address of the recipient.
    :type addr_to: str
    :param subject: Subject of the message.
    :type subject: str
    :return: A prepared message.
    :rtype: email.message.EmailMessage
    """
    from_address = settings.get('email.from')
    if not from_address:
        LOGGER.warning("`email.from` is not set, make sure to check your configuration!")
    message = EmailMessage()
    message['To'] = addr_to
    message['From'] = f'Fietsboek <{from_address}>'
    message['Subject'] = subject
    return message


def send_message(settings, message):
    """Sends an email message using the STMP server configured in the settings.

    The recipient is taken from the 'To'-header of the message.

    :parm settings: The application settings.
    :type settings: dict
    :param message: The message to send.
    :type message: email.message.EmailMessage
    """
    smtp_server = settings.get('email.smtp_url')
    if not smtp_server:
        LOGGER.warning("`email.smtp_url` not set, no email can be sent!")
        return
    smtp_url = urlparse(smtp_server)
    if smtp_url.scheme == 'debug':
        print(message, file=sys.stderr)
        return
    try:
        if smtp_url.scheme == 'smtp':
            client = smtplib.SMTP(smtp_url.hostname, smtp_url.port)
        elif smtp_url.scheme == 'smtp+ssl':
            client = smtplib.SMTP_SSL(smtp_url.hostname, smtp_url.port)
        elif smtp_url.scheme == 'smtp+starttls':
            client = smtplib.SMTP(smtp_url.hostname, smtp_url.port)
            client.starttls()
        if 'email.smtp_user' in settings and 'email.smtp_password' in settings:
            client.login(settings['email.smtp_user'], settings['email.smtp_password'])
        client.send_message(message)
        client.quit()
    except smtplib.SMTPException:
        LOGGER.error("Error when sending an email", exc_info=sys.exc_info())
