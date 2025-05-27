from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def home(request):
    return render(request, 'base.html')


@login_required
def user_profile_view(request):
    return render(request, 'user/profile.html')



def user_logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return redirect('home')