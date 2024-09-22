## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.index, name="index"),
]
