# payments/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# For simplicity, hardcoded OTP token for validation
VALID_OTP = "123456"

@csrf_exempt
def visa_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_number = data.get('card_number')
            amount = data.get('amount')
            otp = data.get('otp')

            if otp == VALID_OTP:
                # Simulate saving transaction, or just respond success
                return JsonResponse({
                    "message": "Payment successful",
                    "data": {
                        "card_number": card_number,
                        "amount": amount,
                        "otp_token": otp,
                        "is_successful": True
                    }
                }, status=200)
            else:
                return JsonResponse({"message": "Wrong OTP"}, status=400)

        except Exception as e:
            return JsonResponse({"message": "Invalid data", "error": str(e)}, status=400)

    return JsonResponse({"message": "Method not allowed"}, status=405)
