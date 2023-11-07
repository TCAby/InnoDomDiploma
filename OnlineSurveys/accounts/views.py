from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group

from .models import UserProfile
from .forms import SurveyUserRegistrationForm


def register(request):
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
            group.user_set.add(new_user
                               )
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = SurveyUserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


def login(DataMixin, LoginView):
    #form_class = AuthenticationForm
    #template_name = 'accounts/login.html'
    pass



@login_required
def profile(request):
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


