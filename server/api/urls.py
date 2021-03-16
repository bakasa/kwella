from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import LoginView, SignUpView, VerifyOTPView

app_name = 'api'

# non-viewsets views
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),

    path('verify-token/<pk>/', VerifyOTPView.as_view(), name='verify-otp'),
]
