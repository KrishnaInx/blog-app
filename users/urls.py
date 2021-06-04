from django.urls import path
from . import views
from .views import PasswordsChangeView

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('password/', PasswordsChangeView.as_view(template_name='users/change_password.html'), name='change_password'),

    ]

