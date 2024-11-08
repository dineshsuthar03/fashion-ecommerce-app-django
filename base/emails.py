
from django.core.mail import send_mail
from django.conf import settings


def send_account_activation_email(email, email_token):
    subject = "Your account needs to be verified"
    email_from = settings.DEFAULT_FROM_EMAIL
    base_url = settings.APP_BASE_URL
    activation_link = f"{base_url}/accounts/activate/{email_token}"
    message = f"Hi, please verify your account.\nClick on the link to activate your account: {activation_link}"
    send_mail(subject, message, email_from, [email])