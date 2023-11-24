from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include
from django.urls import path
from django.urls import re_path as url
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view


urlpatterns = [
    url(r'',  include('users.urls')),
    path('api/admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
