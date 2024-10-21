# mini_fb/models.py
# Define the data objects for our application
from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    '''Encapsulate the profile of one person'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object'''

        return f'{self.first_name} {self.last_name}'

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this object'''

        return f'Status by {self.profile.first_name} on {self.timestamp}'

    def get_images(self):
        '''Return a QuerySet of all images'''

        images = Image.objects.filter(status_message=self).exclude(image_file='')
        return images

    
class Image(models.Model):
    image_file = models.ImageField(blank=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Returns a message about the image'''
        return f"Image for {self.status_message} uploaded on {self.timestamp}"