## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.RandomArticleView.as_view(), name="random"), 
    path(r'show_all/', views.ShowAllView.as_view(), name="show_all"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), ## <int:pk> will work with default get_object method
    # path('create_comment', views.CreateCommentView.as_view(), name='create_comment'), ### FIRST (WITHOUT PK)
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'), ### NEW
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'),  ### NEW

    # authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all'), name="logout"),
    path(r'register/', views.RegistrationView.as_view(), name='register'),
]