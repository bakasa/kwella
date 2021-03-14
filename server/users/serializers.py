from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
