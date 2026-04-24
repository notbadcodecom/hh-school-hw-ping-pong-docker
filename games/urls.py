from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/start-match/', views.start_match, name='start_match'),
    path('api/match-status/<str:match_id>/', views.match_status, name='match_status'),
    path('api/matches/', views.matches_list, name='matches_list'),
    path('api/matches/clear/', views.clear_matches, name='clear_matches'),
]
