from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from authentication.forms import SignupForm
from authentication.models import User


def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignupForm()
    
    return render(request, 'authentication/signup.html', context={'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})