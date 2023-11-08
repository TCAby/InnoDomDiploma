from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SurveyUser


# class SurveyUserRegistrationForm(ModelForm):
class SurveyUserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, label='UserName')
    first_name = forms.CharField(max_length=50, required=True, label='Name')
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = SurveyUser
        fields = ('username', 'first_name', 'email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class SurveyUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SurveyUserProfileForm(forms.Form):
    pass


class UserForgotPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
