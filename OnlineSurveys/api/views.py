from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics, permissions, authentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from survey.models import Questionare, Question
from .serializers import QuestionareSerializer, QuestionSerializer, AnswerSerializer, ResponseSerializer
from accounts.models import SurveyUser


class QuestionareList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Questionare.objects.all()
    serializer_class = QuestionareSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]


class QuestionareDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Questionare.objects.all()
    serializer_class = QuestionareSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]



class QuestionList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]



class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]


class AnswerList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]



class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]


class QuestionList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]



class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]
