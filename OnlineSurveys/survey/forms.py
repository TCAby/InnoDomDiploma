from django import forms
from django.forms import Form, ModelForm
from django.utils import timezone
from .models import Questionare, Question, Response


def prepare_value(value):
    value = timezone.localtime(value)
    return value.strftime("%Y-%m-%dT%H:%M")


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class AddSurveyForm(ModelForm):
    date_from = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    date_upto = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    new_questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.filter(questionare=None),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Questionare
        fields = ['title', 'activity_status', 'date_from', 'date_upto', 'is_anonymous', 'must_answers', 'introduction_text', 'new_questions']


class EditSurveyForm(ModelForm):
    questionare_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.questionare_id = self.instance.pk
        self.fields['exist_questions'].queryset = Question.objects.filter(questionare=self.questionare_id)

    class Meta:
        model = Questionare
        fields = ['title', 'activity_status', 'date_from', 'date_upto', 'is_anonymous', 'must_answers', 'introduction_text', 'new_questions', 'exist_questions', ]

    date_from = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    date_upto = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    new_questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.filter(questionare=None),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    exist_questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

class AddQuestionForm(Form):
    class Meta:
        model = Question
        widgets = {
        }


class EditQuestionForm(ModelForm):
    question_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.question_id = self.instance.pk

    class Meta:
        model = Question
        fields = ['text', 'is_allow_multiple_answers']


class FillSurveyForm(Form):

    class Meta:
        model = Response

