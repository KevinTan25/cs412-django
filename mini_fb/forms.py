# mini_fb/forms.py
# Form to create a profile

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''
    class Meta:
        '''associate this form with the Profile model; select fields.'''
        model = Profile
        fields=['first_name', 'last_name', 'city', 'email', 'image_url']

        first_name = forms.CharField(label="First Name", required=True)
        last_name = forms.CharField(label="Last Name", required=True)
        email = forms.CharField(label="Email")
        image_url = forms.URLInput(attrs={'placeholder': 'Image URL'})


class CreateStatusMessageForm(forms.ModelForm):
    '''associate this form with the Status Message model; select fields.'''
    class Meta:
        model = StatusMessage
        fields = ['message']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']
        