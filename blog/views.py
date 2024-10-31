# blog/views.py
# define the views for the blog app
from django.http import HttpRequest
from django.shortcuts import render
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import * # import the models (e.g., Article)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # The model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # this is the context variable to use in the html

    def dispatch(self, *args, **kwargs):
        '''implement this method to add some debug tracing'''

        print("ShowAllView.dispatch; self.request.user={self.request.user}")
        # let the superclass version of this method do the work
        return super().dispatch(*args, **kwargs)

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

from django.views.generic.edit import CreateView
from .forms import CreateCommentForm
from django.urls import reverse
from typing import Any

class CreateCommentView(CreateView):
    # '''A view to create a new comment and save it to the database.'''
    # form_class = CreateCommentForm
    # template_name = "blog/create_comment_form.html"
    # ## show how the reverse function uses the urls.py to find the URL pattern
    # def get_success_url(self) -> str:
    #     '''Return the URL to redirect to after successfully submitting form.'''
    #     return reverse('show_all')
    #     ## note: this is not ideal, because we are redirected to the main page.
    
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        article = Article.objects.get(pk=pk)
        # add article to context data
        context['article'] = article
        return context

    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.article = article
        return super().form_valid(form)
        
    ## also:  revise the get_success_url
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
    
from .forms import CreateArticleForm, CreateCommentForm ## new import
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # find the user who is logged in
        user = self.request.user

        # attach that user as a FK to the new Article instance
        form.instance.user = user

        # delegate work to the superclass version of this method
        return super().form_valid(form) 

class RegistrationView(CreateView):
    '''Handle registration of new Users.'''

    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''Handle the User creation form submission'''

        if self.request.POST:
            print(f"ReigstrationView.dispatch: self.request.POST={self.request.POST}")

            # reconstruct the UserCreateForm from the POST data
            form = UserCreationForm(self.request.POST)
            
            # if the form isn't value e.c. passwords don't match
            if not form.is_valid():
                print(f"form.errors={form.errors}")
                
                # let CreateView.dispatch handle the problem
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save() # this will commit the insert to the database
            print(f"RegistrationView.dispatch: created user {user}")

            # log the user in
            login(self.request, user)
            print(f"RegistrationView.dispatch: {user} is logged in")

            # note for mini_fb: attach the FK user to the Profile form instance
            

            # return a response
            return redirect(reverse('show_all'))

        # let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)