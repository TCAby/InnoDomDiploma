from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from .models import UserProfile


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


