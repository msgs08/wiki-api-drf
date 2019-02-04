"""wiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ui/', TemplateView.as_view(template_name='index.html')),  # simple javascript UI
    path('swagger/', schema_view),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # base drf auth api
    path('users/', include('users.urls')),
    path('articles/', include('articles.urls'), name='articles'),
    path('notes/', include('notes.urls'), name='notes'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
