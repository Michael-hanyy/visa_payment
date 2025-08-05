from django.contrib import admin
from django.urls import path
from visa_payment.views import UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLoginView.as_view(), name='login'),      # keep root path if you want
    path('login/', UserLoginView.as_view(), name='login'),  # add this line to handle /login/
]
