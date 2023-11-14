from django.shortcuts import render
from rest_framework import generics

from survey.models import Questionare, Question
from .serializers import QuestionareSerializer


class QuestionareList(generics.ListCreateAPIView):
    queryset = Questionare.objects.all()
    serializer_class = QuestionareSerializer


class QuestionareDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionare.objects.all()
    serializer_class = Questionare
