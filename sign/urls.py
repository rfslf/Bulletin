from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, GetCode

urlpatterns = [
     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
     path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
     path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
     path('code/<str:user>', GetCode.as_view(), name='code'),
]