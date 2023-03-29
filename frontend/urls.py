from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name = "Home"),
    path('login/', views.CustomLoginView.as_view(), name='Login'),
    path('check_profile/', views.check_profile, name='check_profile'),
]