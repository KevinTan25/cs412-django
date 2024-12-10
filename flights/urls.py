## flights/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

# all of the URLs that are part of this app
urlpatterns = [
    # Link to show all the flights
    path(r'', views.FlightListView.as_view(), name='all_flights'), # Detail view to show all flights
    path(r'flight/<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),  # Detail view for a specific flight
    path(r'login/', auth_views.LoginView.as_view(template_name='flights/login.html'), name='login'), # Login feature
    path(r'logout/', auth_views.LogoutView.as_view(next_page='all_flights'), name='logout'), # Logout feature
    path(r'register/', views.RegistrationView.as_view(), name='register'), # Register
]