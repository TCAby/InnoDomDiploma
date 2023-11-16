from django.urls import path

from .views import QuestionareList, QuestionareDetail, QuestionList, QuestionDetail, SubmitSurveyResponseView

urlpatterns = [
    path('surveys/', QuestionareList.as_view(), name='surveys-list'),
    path('surveys/<int:pk>', QuestionareDetail.as_view(), name='survey-detail'),
    path('surveys/<int:pk>/', QuestionareDetail.as_view(), name='survey-detail'),
    path('questions/', QuestionList.as_view(), name='questions-list'),
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('submit-survey-response/', SubmitSurveyResponseView.as_view(), name='submit-survey-response'),
]