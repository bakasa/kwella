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
    
    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        sms_otp = int(request.data.get('verify_otp', 0))

        print('\nGen OTP', user.generated_otp, 'SMS OTP',
              sms_otp, user.handle_otp(sms_otp))
            
        return super().partial_update(request, *args, **kwargs)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
