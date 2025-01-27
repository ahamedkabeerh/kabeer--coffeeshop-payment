"""django_razorpay URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.urls')),
] + static(settings.STATIC_URL,document_too=settings.STATIC_ROOT)
