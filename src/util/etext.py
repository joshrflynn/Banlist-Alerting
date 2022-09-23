import email, smtplib, ssl

from os.path import basename

from .providers import PROVIDERS
from .exceptions import (
    ProviderNotFoundException,
    NoMMSSupportException,
    NumberNotValidException,
)


def validate_number(number: str):
    num = ""
    valid = False

    for character in number:
        if character.isdigit():
            num += character

    if len(num) == 10:
        valid = True

    if not valid:
        raise exceptions.NumberNotValidException(number)

    return num


def format_provider_email_address(number: str, provider: str, mms=False):
    provider_info = PROVIDERS.get(provider)

    if provider_info == None:
        raise exceptions.ProviderNotFoundException(provider)

    domain = provider_info.get("sms")

    if mms:
        mms_support = provider_info.get("mms_support")
        mms_domain = provider_info.get("mms")

        if not mms_support:
            raise exceptions.NoMMSSupportException(provider)

        # use mms domain if provider has one
        if mms_domain:
            domain = mms_domain

    return f"{number}@{domain}"


def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "Yugioh Ban List Alert!",
    smtp_server: str = "smtp.office365.com",
    smtp_port: int = 587,
    name: str = "",
):
    number = validate_number(number)
    sender_email, email_password = sender_credentials
    receiver_email = format_provider_email_address(number, provider)
    email_message = f"Subject: {subject}\nTo:{receiver_email}\n{message}"
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, email_message)
        print(f"Message sent to {name}")

