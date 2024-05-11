from django.urls import path
from . import views

app_name = 'tourney_profiles'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
]