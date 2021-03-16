from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import asyncio

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'type', 'password', 'confirm_password')
        related_only_fields = ('id', )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('The passwords must be the same!')
        return super().validate(attrs)
    
    def create(self, validated_data):
        
        # remove password confirmation
        confirm_password = validated_data.pop('confirm_password', None)
        return super().create(validated_data)

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token


class VerifyOTPSerializer(serializers.ModelSerializer):

    # def update(self, instance, validated_data):
    #     print(f'Updating {instance.phone_number} with {validated_data}')
    #     return super().update(instance, validated_data)
    
    class Meta:
        model = get_user_model()
        fields = '__all__'
    
