from django.urls import path
from .views import visa_payment

urlpatterns = [
    path('pay/', visa_payment),
]

