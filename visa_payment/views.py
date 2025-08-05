from django.contrib.auth import authenticate, get_user_model
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from .models import UserProfile
from .tasks import send_payment_confirmation

User = get_user_model()

class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        visa_card = request.POST.get('visa_card')
        visa_password = request.POST.get('visa_password')

        user = authenticate(request, username=username, password=password)

        if user:
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User profile not found'}, status=404)

            if profile.visa_card_number != visa_card or profile.visa_password != visa_password:
                return JsonResponse({'error': 'Incorrect visa info'}, status=401)

            # Reset suspicious flags
            profile.failed_login_attempts = 0
            profile.suspicious_warning = False
            profile.save()

            # Trigger Celery task
            send_payment_confirmation.delay(visa_card, 100)

            return JsonResponse({'message': 'Login success, confirmation sent'})

        # Handle failed login attempt
        try:
            user_obj = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user_obj)
            profile.failed_login_attempts += 1
            if profile.failed_login_attempts >= 2:
                profile.suspicious_warning = True
            profile.save()
        except:
            pass

        return JsonResponse({'error': 'Invalid credentials'}, status=401)
