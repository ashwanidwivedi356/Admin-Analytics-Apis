from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(email, order_id):
    subject = f"Order #{order_id} Confirmed!"
    message = f"Thank you for your purchase. Your order #{order_id} has been successfully placed."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    return "Email sent"
