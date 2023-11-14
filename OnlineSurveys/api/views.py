from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics, permissions, authentication, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from survey.models import Questionare, Question
from .serializers import QuestionareSerializer, QuestionSerializer, ResponseSerializer
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


class ResponseList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

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


class SubmitSurveyResponseView(generics.CreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # To use this endpoint (take survey) admin user can make a POST request with the user's survey responses
        # in the request body.
        # For example:
        # {
        #   "questionare": 1,
        #   "question": 1,
        #   "answer": 1
        # }
        # This will submit a response to question 1 of survey 1 with answer 1.

