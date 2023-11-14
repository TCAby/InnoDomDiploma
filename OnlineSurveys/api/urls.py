from django.urls import path

from .views import QuestionareList, QuestionareDetail

urlpatterns = [
    path('surveys/', QuestionareList.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', QuestionareDetail.as_view(), name='survey-detail'),
]