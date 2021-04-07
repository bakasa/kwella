import random
from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django_otp.oath import TOTP
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from sendsms import api
from django.conf import settings
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ('id', 'phone_number', 'first_name', 'last_name',
                  'type', 'password', 'confirm_password')
        read_only_fields = ('id', )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # validate signup password
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(
                {
                    'success': False,
                    'message':_('The passwords must be the same!'),
                    'status': status.HTTP_400_BAD_REQUEST
                }, code=400)
        return super().validate(attrs)

    def create(self, validated_data):
        # remove password confirmation from signup data
        confirm_password = validated_data.pop('confirm_password', None)

        return super().create(validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)
        user_data = UserSerializer(user).data

        # add user data to the token payload (except user id)
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token

    # def validate(self, data):
    #     return super().validate(data)

# class LoginSerializer(serializers.Serializer):

#     phone_number = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=128, write_only=True)

#     def validate(self, attrs):
#         phone_number = attrs.get("phone_number", None)
#         password = attrs.get("password", None)


#         try:
#             user = authenticate(phone_number=phone_number, password=password)
#             print(f'\nLOGIN DATA: {user}\n')

#             if user is None:
#                 raise serializers.ValidationError(
#                     'A user with this phone_number and password is not found.'
#                 )

#         except get_user_model().DoesNotExist:
#             raise serializers.ValidationError(
#                 'User with given phone_number and password does not exists'
#             )
#         return super().validate(attrs)
