from rest_framework import serializers

from survey.models import Questionare, Question, Answer, Response

class QuestionareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionare
        fields = [
            'id',
            'title',
            'introduction_text',
            'activity_status',
            'date_from',
            'date_upto',
            'is_anonymous',
            'must_answers'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'is_allow_multiple_answers', 'questionare']


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'user', 'questionare', 'question', 'answer', 'survey_session', 'timestamp']
