# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import * # import the models (e.g., Article)

import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # The model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # this is the context variable to use in the html

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''
    model = Article # The model to display
    template_name = 'blog/article.html'
    context_object_name = 'article' # this is the context variable to use in the html

    # AttributeError: Generic detail view RandomArticleView must be called with either
    # one solution: implement get_object method

    def get_object(self):
        '''Return one Article chose at random'''

        # explicitly add an error to generate a call stack trace:
        # y = 3 / 0

        # Retrieve all of the articles
        all_articles = Article.objects.all()
        # pick one at random
        random_article = random.choice(all_articles)
        return random_article
    

class ArticleView(DetailView):
    '''Display one Article selected by PK'''
    model = Article # The model to display
    template_name = 'blog/article.html'
    context_object_name = 'article' # this is the context variable to use in the html