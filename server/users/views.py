from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, UserSerializer


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model()
    serializer_class = UserSerializer

class VerifyOTPView(generics.UpdateAPIView):
    queryset = get_user_model()
    serializer_class = UserSerializer
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
