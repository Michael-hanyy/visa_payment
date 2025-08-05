from celery import shared_task

@shared_task
def send_payment_confirmation(card_number, amount):
    print(f"[CELERY] Payment confirmed for card {card_number} - ${amount}")
    return True
