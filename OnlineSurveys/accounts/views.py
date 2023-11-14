from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import UserProfile, SurveyUser
from .forms import SurveyUserRegistrationForm, SurveyUserLoginForm
from .forms import UserForgotPasswordForm, UserSetNewPasswordForm


def surveyuser_register(request):
    if request.method == 'POST':
        user_form = SurveyUserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Add new user to the specified group
            group = Group.objects.get(name='Survey Users')
            group.surveyuser_set.add(new_user)
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'accounts/register.html', {'user_form': user_form})
    else:
        user_form = SurveyUserRegistrationForm()
        return render(request, 'accounts/register.html', {'user_form': user_form})


def surveyuser_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SurveyUserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Sorry, your account had been disabled')
            else:
                return HttpResponse('Invalid login/password')
        else:
            print(form.errors)
    else:
        form = SurveyUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def surveyuser_logout(request):
    logout(request)
    return redirect('/')


@login_required
def surveyuser_profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'accounts/profile.html', {'user': user, 'profile': profile})


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('survey/home')
    return render(request, 'accounts/admin_dashboard.html')


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = UserForgotPasswordForm
    template_name = 'accounts/user_password_reset.html'
    success_url = reverse_lazy(surveyuser_login)
    success_message = 'Email with password recovery instructions sent to your email address'
    subject_template_name = 'accounts/email/password_subject_reset_mail.txt'
    email_template_name = 'accounts/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password recovery request'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = 'accounts/user_password_set_new.html'
    success_url = reverse_lazy(surveyuser_login)
    success_message = 'Password successfully changed. You can login to the site.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a new password'
        return context


@login_required
def users(request):
    context = {
        'users': SurveyUser.objects.all(),
    }
    return render(request, 'accounts/users.html', context)
