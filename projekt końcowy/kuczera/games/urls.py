from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("games", views.games_view, name="games"),
    path("events", views.events_view, name="events"),
    path("scoreboard", views.scoreboard_view, name="scoreboard"),
]