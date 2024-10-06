# mini_fb/views.py
# define the views for the mini_fb app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import * # import the models (e.g., Profile)

# class-based view
class ShowAllProfilesView(ListView):
    '''the view to show all Profiles'''
    model = Profile # The model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # this is the context variable to use in the html