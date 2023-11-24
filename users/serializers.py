from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserNotification


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
        )
    
    def validate_email(self, value):
        # email validation logic
        # Checking if the email is unique in the database
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_phone_number(self, value):
        # phone number validation logic
        # Checking if the phone number is valid
        if not value.isdigit():
            raise serializers.ValidationError("Invalid phone number. Please enter only digits.")
        return value


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)

    class Meta:
        model = get_user_model()
        fields = ('password', 'email')

    #Validation for login in the user
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Validation logic
        user = get_user_model().objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        return data

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)
    email = serializers.EmailField(source='user.email', required=False)
    #include the 'email' field only if the user is authenticated.

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        )


class EmptySerializer(serializers.Serializer):
    pass
