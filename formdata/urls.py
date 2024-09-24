## formdata/urls.py

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns:
# everything related to the form data app will be here
urlpatterns = [
    path(r'', views.show_form, name="show_form"), ## new homepage for form
    path(r'submit', views.submit, name="submit"), ## handle submit button
]