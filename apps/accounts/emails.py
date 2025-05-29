from django.conf import settings
from django.core.mail import send_mail

def sendPasswordResetEmail(email,token):    
    subject = 'Reset Your Password'
    email_from = settings.EMAIL_HOST_USER
    message = f'''<p>Hi,</p>
<p>Click here to reset your password: <a href="http://127.0.0.1:8000/accounts/reset-password/{token}/">Reset Password</a></p>'''
    send_mail(subject, message, email_from, [email], html_message=message)
    return True


def sendPaymentSuccessEmail(email, order_number):
    subject = '🎉 Payment Successful - Your Order Confirmation'

    email_from = settings.EMAIL_HOST_USER

    order_url = f"http://127.0.0.1:8000/store/orders/{order_number}"

    message = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f7f7f7;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 30px;">
            <h2 style="color: #4CAF50;">✅ Payment Successful!</h2>
            <p style="font-size: 16px; color: #333;">Hi,</p>
            <p style="font-size: 16px; color: #333;">
                Thank you for shopping with <strong>GoGroc</strong>! Your payment has been successfully received.
            </p>
            <p style="font-size: 16px; color: #333;">
                Your order number is <strong>{order_number}</strong>. You can view the details of your order by clicking the button below:
            </p>
            <div style="text-align: center; margin: 20px 0;">
                <a href="{order_url}" style="display: inline-block; padding: 12px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; font-size: 16px;">
                    View Order
                </a>
            </div>
            <p style="font-size: 14px; color: #999;">
                If you have any questions, feel free to reach out to our support team.
            </p>
            <p style="font-size: 14px; color: #999;">– The GoGroc Team</p>
        </div>
    </div>
    """

    send_mail(subject, '', email_from, [email], html_message=message)
    return True