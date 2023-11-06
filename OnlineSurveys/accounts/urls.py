from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]