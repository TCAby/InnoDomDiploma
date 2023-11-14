from django.urls import path

from .views import QuestionareList, QuestionareDetail, QuestionList, QuestionDetail

urlpatterns = [
    path('surveys/', QuestionareList.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', QuestionareDetail.as_view(), name='survey-detail'),
    path('questions/', QuestionList.as_view(), name='survey-list'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='survey-detail'),
]