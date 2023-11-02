from django import forms
from django.forms import Form, ModelForm, TextInput
from django.core.exceptions import ValidationError
import datetime  # for checking renewal date range.
from .models import Questionare

class AddSurveyForm(Form):
    pass


class EditSurveyForm(Form):
    pass


class AddQuestionForm(Form):
    # switch = forms.BooleanField(widget=forms.CheckboxInput(input_value='off', check_test=lambda value: value == 'on'))
    pass


class EditQuestionForm(Form):
    pass


