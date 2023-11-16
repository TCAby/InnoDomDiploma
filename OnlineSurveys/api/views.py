from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response
import datetime

from survey.models import Questionare, Question
from accounts.models import SurveyUser
from .serializers import QuestionareSerializer, QuestionSerializer, ResponseSerializer


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
        return [permissions.IsAuthenticated()]


class SubmitSurveyResponseView(generics.CreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def questionare_permission_validation(questionare_id: int) -> bool:
        return Questionare.objects.is_status_daterange_actual(id=questionare_id)

    @staticmethod
    def questionare_filling_validation(response) -> bool:
        keys = ['questionare', 'question', 'answer']
        validation = all(key in response for key in keys)
        validation = validation and all(value.isdigit() for value in response.values())

        return validation

    def create(self, request, *args, **kwargs):
        # Perform validation on related questionare fields
        questionare_id = request.data.get('questionare')

        if not self.questionare_permission_validation(questionare_id):
            return Response({"error": "Validation failed for questionare (status or date range incorrect)"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not self.questionare_filling_validation(request.data):
            return Response({"error": "Validation failed for questionare fields",
                             'details':request.data},
                            status=status.HTTP_400_BAD_REQUEST)

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
