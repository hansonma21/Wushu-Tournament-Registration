from django.urls import path
from . import views

app_name = 'tourney_reg'

urlpatterns = [
    path('', views.registration_view, name='registration'),
]
