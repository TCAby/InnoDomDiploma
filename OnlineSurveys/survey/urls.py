from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="surveys-home"),
    path('survey/<int:id>/', views.survey, name="survey"),
    path('surveys/', views.surveys, name="surveys"),
    path('edit-survey/<int:id>/', views.edit_survey, name="edit-survey"),
    path('add-survey/', views.add_survey, name="add-survey"),
    path('remove-survey/<int:id>/', views.remove_survey, name="remove-survey"),
    path('questions/', views.questions, name="questions"),
    path('add-question/', views.add_question, name="add-question"),
    path('answer/', views.answer, name="answer"),
]
