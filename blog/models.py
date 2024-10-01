# blog/models.py
# Define the data objects for our application
from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the idea of one Article by some author.'''

    # data attributes of an Article:
    title = models.TextField(blank=False) # Can't be blank. Creates a text field for title
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True) # When we create an object set the time to now
    image_url = models.URLField(blank=True) # URL that will refer to an image url (it will not upload an image)

    def __str__(self):
        '''Return a string representation of this object'''

        return f'{self.title} by {self.author}'