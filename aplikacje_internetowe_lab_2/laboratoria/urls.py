from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("lab_1", views.lab_1, name="lab_1"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout')
]
