from django.urls import path
from . import views

app_name = 'tourney_pages'

urlpatterns = [
    path('', views.index, name='home'),
    path('learn_more/', views.learn_more_view, name='learn_more'),
    path('news/', views.news_view, name='news'),
]