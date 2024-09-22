## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.quote, name="quote"), # Main page
    path('quote', views.quote, name='quote'), # Same as main page
    path('show_all', views.show_all, name='show_all'), # Show all the quotes/images
    path('about', views.about, name='about'),  # About page of person
]
