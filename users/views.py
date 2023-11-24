from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.response import Response

# for generating tokens
import jwt
from user_management import settings

# for updating the user login activity
from datetime import datetime, timedelta
from django.utils import timezone

#session_auth
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login

#serializers
from .serializers import LoginSerializer
from .serializers import RegisterSerializer
from .serializers import UserSerializer

from core_viewsets.custom_viewsets import CreateViewSet

from rest_framework import status
from rest_framework import viewsets


class RegisterViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # This will raise a validation error if the data is invalid
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({'code': 200, 'message': 'success', 'user_id': user.pk})


class LoginViewSet(CreateViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = ()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user_obj = get_user_model().objects.get(email=email)

        # Generate JWT token
        access_token = jwt.encode(
            {'user_id': user_obj.pk, 'exp': datetime.utcnow() + timedelta(days=1)},
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        # Generate JWT refresh token
        refresh_token = jwt.encode(
            {'user_id': user_obj.pk, 'exp': datetime.utcnow() + timedelta(days=30)},
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        # Log the user in (create a session)
        login(request, user_obj)

        user_obj.last_login = timezone.now()
        user_obj.save()

        return Response(
            {
                'code': 200,
                'message': 'success',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_id': user_obj.pk,
                'name': user_obj.first_name,
                'email': user_obj.email,
                'last_login': user_obj.last_login,
            },
        )

class MeViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]  # ToDo: Specify Auth class
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer  # Use the UserSerializer
    queryset = get_user_model().objects.all()

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

from django.shortcuts import render
from .models import CountryPopulation

def home(request):
    countries_data = CountryPopulation.objects.all()
    return render(request, 'home.html', {'countries_data': countries_data})