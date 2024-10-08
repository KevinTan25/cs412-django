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
    
    def get_comments(self):
        '''Return a QuerySet of all comments on this article'''

        # use the ORM to retreme Comments for which the FK is this article
        comments = Comment.objects.filter(article=self)
    

class Comment(models.Model):
    '''
    Encapsulate the idea of a Comment on an Article
    '''

    # model the 1 to many relationship with article (foreign key)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return the string representation of this comment.'''
        return f'{self.text}'
