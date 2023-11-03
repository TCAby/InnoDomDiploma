from django import forms
from django.forms import Form, ModelForm, TextInput
from django.core.exceptions import ValidationError
import datetime  # for checking renewal date range.
from django.utils import timezone
from .models import Questionare, Question, Answer


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def prepare_value(self, value):
        value = timezone.localtime(value)
        return value.strftime("%Y-%m-%dT%H:%M")


class AddSurveyForm(ModelForm):
    date_from = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    date_upto = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    class Meta:
        model = Questionare
        fields = ['title', 'activity_status', 'date_from', 'date_upto', 'is_anonymous']


class EditSurveyForm(ModelForm):
    date_from = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    date_upto = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-select', 'name': 'date_from'}))
    new_questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.filter(questionare=None),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    exist_questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.filter(questionare=3),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Questionare
        fields = ['title', 'activity_status', 'date_from', 'date_upto', 'is_anonymous', 'new_questions', 'exist_questions']


class AddQuestionForm(Form):
    # switch = forms.BooleanField(widget=forms.CheckboxInput(input_value='off', check_test=lambda value: value == 'on'))
    class Meta:
        widgets = {
            "date_from": DateTimeLocalInput(),
            "date_upto": DateTimeLocalInput(),
        }


class EditQuestionForm(Form):
    pass


