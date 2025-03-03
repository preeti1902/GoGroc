from django.contrib import admin
from django.urls import path
from .views import registerView, loginView, emailActivationView, logoutView, forgetPasswordView, resetPasswordView

urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('activate/<str:email_token>/', emailActivationView, name='email-activation'),
    path('logout/', logoutView, name='logout'),
    path('forget-password/', forgetPasswordView, name='forget-password'),
    path('reset-password/<str:token>/', resetPasswordView, name='reset-password'),
]