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
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this object'''

        return f'{self.first_name} {self.last_name}'

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        # Combine and get the Profile instances
        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        return Profile.objects.filter(id__in=friend_ids)
    
    def add_friend(self, other):
        from django.db.models import Q
        if self == other:
            return

        # Check if the friendship already exists
        existing_friendship = Friend.objects.filter(
            (Q(profile1=self) & Q(profile2=other)) | (Q(profile1=other) & Q(profile2=self))
        ).exists()

        if not existing_friendship:
            # Create a new Friend instance if it doesn't exist
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        friends = self.get_friends()
        return Profile.objects.exclude(id__in=[self.id] + [friend.id for friend in friends])
    
    def get_news_feed(self):
        from django.db.models import Q
        friends = self.get_friends()
        
        # Retrieve StatusMessages for the profile and their friends
        news_feed = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__in=friends)
        ).order_by('-timestamp')
        
        return news_feed

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

class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', related_name='profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey('Profile', related_name='profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"