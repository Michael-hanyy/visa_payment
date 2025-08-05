from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from .views import user_login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# def home(request):
#     return HttpResponse("Welcome to Visa Payment API!")

urlpatterns = [
    # path('', home),   
    path('admin/', admin.site.urls),
    # path('api/', include('payments.urls')),
     path('login/', user_login, name='user_login'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
