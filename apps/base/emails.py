from django.conf import settings
from django.core.mail import send_mail


def sendAccountActivationEmail(email, emailToken):
    subject = 'Please Verify your account'
    emailFrom = settings.EMAIL_HOST_USER
    message = f'Hi, Click here to verify your account http://127.0.0.1:8000/accounts/activate/{emailToken}'
    send_mail(subject,message,emailFrom,[email])