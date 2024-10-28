# mini_fb/views.py
# define the views for the mini_fb app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import * # import the models (e.g., Profile)
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views import View
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
        
        # save the status message to the database
        sm = form.save()
        #read tehe file from the form:
        files = self.request.FILES.getlist('files')
        for file in files:
            # Create an Image object for each uploaded file and link it to the status message
            image = Image(status_message=sm, image_file=file)
            image.save()  # Save the Image object

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    

class DeleteStatusMessageView(DeleteView):
    '''Delete Status Message'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})

class UpdateStatusMessageView(UpdateView):
    '''Update Status Message'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})

from django.shortcuts import get_object_or_404, redirect
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])

        profile.add_friend(other_profile)

        # Redirect back to the profile page
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context