from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name="surveys-home"),
    path('survey/<int:id>/', views.survey, name="survey"),
    path('surveys/', views.surveys, name="surveys"),
    path('surveys/edit/<int:id>/', views.edit_survey, name="edit-survey"),
    path('surveys/add/', views.add_survey, name="add-survey"),
    path('surveys/remove/<int:id>/', views.remove_survey, name="remove-survey"),
    path('surveys/questions/', views.questions, name="questions"),
    path('surveys/questions/add/', views.add_question, name="add-question"),
    path('surveys/questions/edit/<int:id>/', views.edit_question, name="edit-question"),
    path('surveys/questions/remove/<int:id>/', views.remove_question, name="remove-question"),
    # Redirects typical /admin URLs to the customs
    re_path(r'^admin/survey/questionnaire/(?P<questionnaire_id>\d+)/change/$', views.edit_survey),
    re_path(r'^admin/survey/questionare/$', views.surveys),
    re_path(r'^admin/survey/questionare/add/$', views.add_survey),
    re_path(r'^admin/survey/question/(?P<questionnaire_id>\d+)/change/$', views.edit_question),
    re_path(r'^admin/survey/question/$', views.questions),
    re_path(r'^admin/survey/question/add/$', views.add_question),

]
