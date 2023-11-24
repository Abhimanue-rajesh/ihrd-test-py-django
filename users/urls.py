from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginViewSet
from .views import MeViewSet
from .views import RegisterViewSet
from .views import home


router = DefaultRouter(trailing_slash=False)

router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'me', MeViewSet, basename='me')

urlpatterns = [
    path('', home, name='home'),
    path(r'', include(router.urls)),
    
]
