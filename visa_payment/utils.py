import re
import logging
from functools import wraps
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.http import JsonResponse
from .models import UserProfile
from .tasks import send_payment_confirmation
import uuid

def generate_transaction_id():
    return f"TXN_{uuid.uuid4()}"

import uuid

def generate_transaction_id():
    return f"TXN_{uuid.uuid4()}"

def calculate_discount(amount, discount_percent):
    """
    Calculate the discounted amount based on percentage.

    Example:
    - amount=200, discount_percent=50 → 200 - 50% of 200 = 100
    """
    return amount * (1 - discount_percent / 100)


# Django User model
User = get_user_model()

# Logger setup
logger = logging.getLogger(__name__)

# ====================================================
# Input Validation & Sanitization
# ====================================================

def sanitize_input(value):
    """Trim whitespace and normalize input strings."""
    if isinstance(value, str):
        return value.strip()
    return value

def is_valid_visa_card(card_number):
    """Check if visa card is 16 digits and starts with 4."""
    return bool(card_number and re.fullmatch(r"4[0-9]{15}", card_number))

def is_strong_password(password):
    """
    Check if password is strong:
    - At least 8 characters
    - Contains at least 1 digit
    - Contains at least 1 letter
    """
    return (
        isinstance(password, str)
        and len(password) >= 8
        and any(char.isdigit() for char in password)
        and any(char.isalpha() for char in password)
    )

# ====================================================
# JSON Response Helpers
# ====================================================

def success_response(message, data=None, status=200):
    """Standard success JSON response."""
    payload = {"message": message}
    if data is not None:
        payload["data"] = data
    return JsonResponse(payload, status=status)

def error_response(message, status=400):
    """Standard error JSON response."""
    logger.error(f"Error Response: {message} (status={status})")
    return JsonResponse({"error": message}, status=status)

# ====================================================
# Suspicious Activity Logging
# ====================================================

def log_suspicious_activity(username, reason):
    """Log suspicious activity for monitoring and alerts."""
    logger.warning(f"[SUSPICIOUS] User={username}, Reason={reason}")

# ====================================================
# DB Transaction Helper
# ====================================================

def atomic_operation(func):
    """Decorator to run DB ops in a safe atomic block."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction.atomic():
            return func(*args, **kwargs)
    return wrapper

# ====================================================
# Auth & Profile Management
# ====================================================

def validate_login_input(username, password, visa_card, visa_password):
    """Ensure all required inputs are present."""
    if not all([username, password, visa_card, visa_password]):
        return error_response("Missing credentials", status=400)
    return None

def authenticate_user(request, username, password):
    """Wrapper around Django's authenticate system."""
    user = authenticate(request, username=username, password=password)
    if not user:
        logger.info(f"Authentication failed for username='{username}'")
    else:
        logger.info(f"Authentication success for username='{username}'")
    return user

def check_user_profile(user, visa_card, visa_password):
    """
    Check if user's profile exists and visa credentials match.
    Returns (error_response, profile).
    """
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        logger.error(f"Profile not found for user='{user.username}'")
        return error_response("User profile not found", status=404), None

    if profile.visa_card_number != visa_card or profile.visa_password != visa_password:
        logger.warning(f"Visa info mismatch for user='{user.username}'")
        return error_response("Incorrect visa info", status=401), None

    return None, profile

@atomic_operation
def reset_failed_attempts(profile):
    """Reset failed login attempts after successful login."""
    profile.failed_login_attempts = 0
    profile.suspicious_warning = False
    profile.save()
    logger.info(f"Reset login attempts for user='{profile.user.username}'")

@atomic_operation
def record_failed_attempt(username):
    """Increment failed login attempts and mark suspicious if needed."""
    try:
        user_obj = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user_obj)
        profile.failed_login_attempts += 1
        if profile.failed_login_attempts >= 2:
            profile.suspicious_warning = True
            log_suspicious_activity(username, "Too many failed login attempts")
        profile.save()
        logger.info(
            f"Failed login recorded for user='{username}', "
            f"attempts={profile.failed_login_attempts}"
        )
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        logger.warning(f"Failed login attempt for non-existing user='{username}'")

# ====================================================
# Celery Task Wrapper
# ====================================================

def trigger_confirmation(visa_card, amount=100):
    """
    Send Celery confirmation task.
    Keeps the view unaware of Celery internals.
    """
    try:
        send_payment_confirmation.delay(visa_card, amount)
        logger.info(f"Payment confirmation triggered for card={visa_card[-4:]} amount={amount}")
    except Exception as e:
        log_suspicious_activity("system", f"Celery error: {str(e)}")
        return error_response("Failed to send confirmation", status=500)
    return None

