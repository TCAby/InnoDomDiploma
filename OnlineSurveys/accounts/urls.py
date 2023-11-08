from django.urls import path
from . import views
from .views import UserForgotPasswordView, UserPasswordResetConfirmView


urlpatterns = [
    path('profile/', views.surveyuser_profile, name='profile'),
    path('login/', views.surveyuser_login, name='login'),
    path('register/', views.surveyuser_register, name='register'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('reset-password/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]