from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation(card_number, amount):
    message = f"Payment of ${amount} from card {card_number} is confirmed."
    send_mail(
        'Payment Confirmation',
        message,
        'noreply@visa-payment.com',
        ['user@example.com'],  # You can make this dynamic
        fail_silently=False,
    )
