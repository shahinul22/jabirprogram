from django.shortcuts import render
from clubs.models import ClubRegistration
from django.contrib.auth.decorators import login_required


def home(request):
    user = request.user
    try:
        club = ClubRegistration.objects.get(club_username=user.username)
    except ClubRegistration.DoesNotExist:
        club = None

    return render(request, 'base.html', {'club': club})

# user/views.py
from django.contrib.auth.views import LoginView

