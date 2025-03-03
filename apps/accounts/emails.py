from django.conf import settings
from django.core.mail import send_mail

def sendPasswordResetEmail(email,token):    
    subject = 'Reset Your Password'
    email_from = settings.EMAIL_HOST_USER
    message = f'''<p>Hi,</p>
<p>Click here to reset your password: <a href="http://127.0.0.1:8000/accounts/reset-password/{token}/">Reset Password</a></p>'''
    send_mail(subject, message, email_from, [email], html_message=message)
    return True