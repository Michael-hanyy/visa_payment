from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .tasks import send_payment_confirmation

User = get_user_model()  # safer way to get the User model

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    visa_card = request.data.get('visa_card')
    visa_password = request.data.get('visa_password')

    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check Visa card info for extra security
        if profile.visa_card_number != visa_card or profile.visa_password != visa_password:
            return Response({'error': 'Visa card info incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

        # Reset failed attempts on success
        profile.failed_login_attempts = 0
        profile.suspicious_warning = False
        profile.save()

        token, created = Token.objects.get_or_create(user=user)

        # Send token by email
        send_mail(
            'Your Authentication Token',
            f'Hello {user.username}, your token is: {token.key}',
            'noreply@yourdomain.com',
            [user.email],
            fail_silently=True,
        )
        return Response({'token': token.key})
    else:
        # Handle failed login attempt
        try:
            user_obj = User.objects.get(username=username)
            try:
                profile = UserProfile.objects.get(user=user_obj)
                profile.failed_login_attempts += 1
                if profile.failed_login_attempts >= 2:
                    profile.suspicious_warning = True
                profile.save()
            except UserProfile.DoesNotExist:
                pass  # No profile to update
        except User.DoesNotExist:
            pass  # user not found, no profile to update

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if otp == VALID_OTP:
    # Call Celery task asynchronously
     send_payment_confirmation.delay(card_number, amount)

    return JsonResponse({
        "message": "Payment successful",
        "data": {
            "card_number": card_number,
            "amount": amount,
            "otp_token": otp,
            "is_successful": True
        }
    }, status=200)
