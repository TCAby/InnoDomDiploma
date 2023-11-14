from rest_framework import serializers

from survey.models import Questionare, Question

class QuestionareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionare
        fields = ['id', 'title', 'introduction_text', 'activity_status', 'date_from', 'date_upto', 'is_anonymous']