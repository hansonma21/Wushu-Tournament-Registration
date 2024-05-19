from django.urls import path
from . import views

app_name = 'tourney_scoring'

urlpatterns = [
    path('tournaments/', views.main_dashboard_view, name='dashboard'),
    path('tournaments/<int:tournament_id>/events/', views.tournament_dashboard_view, name='tournament_dashboard'),
    path('tournaments/<int:tournament_id>/events/<int:tournament_event_id>/competitors/', views.tournament_event_dashboard_view, name='tournament_event_dashboard'),
    path('tournaments/<int:tournament_id>/events/<int:tournament_event_id>/competitors/<int:order>/', views.event_scoring_view, name='event_scoring'),
    # path('tournaments/<int:tournament_id>/events/<int:tournament_event_id>/competitors/<int:order>/submit_judge_form/', 
    #      views.submit_judge_form_view, name='submit_judge_form'),
    # path('tournaments/<int:tournament_id>/events/<int:tournament_event_id>/competitors/<int:order>/submit_final_form/',
    #         views.submit_final_form_view, name='submit_final_form'),
]
