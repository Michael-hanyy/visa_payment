from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from . import utils


class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        """Render login form."""
        return render(request, self.template_name)

    def post(self, request):
        """Handle login and visa verification."""
        username = request.POST.get("username")
        password = request.POST.get("password")
        visa_card = request.POST.get("visa_card")
        visa_password = request.POST.get("visa_password")

        #Validate inputs
        if not utils.validate_inputs(username, password, visa_card, visa_password):
            return JsonResponse({"error": "Missing credentials"}, status=400)

        #Authenticate user
        user = utils.authenticate_user(request, username, password)
        if user:
            profile = utils.get_user_profile(user)
            if not profile:
                return JsonResponse({"error": "User profile not found"}, status=404)

            #Verify Visa details
            if not utils.verify_visa_info(profile, visa_card, visa_password):
                return JsonResponse({"error": "Incorrect visa info"}, status=401)

            #Reset login attempts
            utils.reset_login_attempts(profile)

            #Trigger Celery task
            utils.trigger_payment_confirmation(visa_card, 100)

            return JsonResponse(
                {"message": "Login success, confirmation sent"}, status=200
            )

        #Handle failed login
        utils.increment_failed_attempts(username)
        return JsonResponse({"error": "Invalid credentials"}, status=401)
