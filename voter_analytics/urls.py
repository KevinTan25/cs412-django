# voter_analytics/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    path(r'', views.VoterListView.as_view(), name='voters'),
    path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter_detail'),
    path(r'graphs/', views.GraphsView.as_view(), name='graphs'),
]