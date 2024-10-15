# mini_fb/views.py
# define the views for the mini_fb app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import * # import the models (e.g., Profile)
from django.views.generic import DetailView
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse

# class-based view
class ShowAllProfilesView(ListView):
    '''the view to show all Profiles'''
    model = Profile # The model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # this is the context variable to use in the html

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'  # The template that will render the profile
    context_object_name = 'profile' 

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])  # Get the Profile object
        form.instance.profile = profile  # Set the profile of the status message
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
