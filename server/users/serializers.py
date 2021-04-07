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


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    # verify_otp = serializers.IntegerField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'phone_number', 'first_name', 'last_name',
                  'type', 'password', 'confirm_password')
        related_only_fields = ('id', )
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

        # # validate data for updating a user
        # if len(attrs.keys()) <= 0:
        #     raise serializers.ValidationError(
        #         {
        #             'success': False,
        #             'message': _('There\'s nothing to update'),
        #             'status': status.HTTP_400_BAD_REQUEST
        #         }
        #     )

        return super().validate(attrs)

    def create(self, validated_data):
        # remove password confirmation
        confirm_password = validated_data.pop('confirm_password', None)

        return super().create(validated_data)

    # def update(self, instance, validated_data):

    #     # verify user's token from request
    #     sms_otp = int(validated_data.get('verify_otp', 0))

    #     instance.otp = sms_otp

    #     return super().update(instance, validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token
