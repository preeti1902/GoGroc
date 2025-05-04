from django.contrib import admin
from django.urls import path
from .views import registerView, loginView, emailActivationView, logoutView, forgotPasswordView, passwordResetView

urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('activate/<str:emailToken>/', emailActivationView, name='email-activation'),
    path('logout/', logoutView, name='logout'),
    path('forget-password/', forgotPasswordView, name='forget-password'),
    path('reset-password/<str:token>/', passwordResetView, name='reset-password'),
]