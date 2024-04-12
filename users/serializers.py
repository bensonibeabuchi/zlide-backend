from djoser.serializers import UserCreateSerializer
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers




class UserCreateSerializer(UserCreateSerializer):
    class Meta (UserCreateSerializer.Meta):
        model = CustomUser
        fields= ('id', 'email', 'password', 'first_name', 'last_name', 'job_title', 'company')

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'job_title', 'company']
        extra_kwargs = {'password': {'write_only': True}}
        error_messages = {
            'email': {
                'invalid': ("Enter a valid email."),
                'unique': ("user with this email address already exists.")
            },
        }
        

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError()
        return value

    def validate_password(self, value):
        validate_password(value)
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user