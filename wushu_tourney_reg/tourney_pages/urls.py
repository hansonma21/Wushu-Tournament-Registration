from django.urls import path
from . import views

app_name = 'tourney_pages'

urlpatterns = [
    path('', views.index, name='index'),
]