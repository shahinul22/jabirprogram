from django.shortcuts import render
from clubs.models import ClubRegistration
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    club = None

    try:
        club_reg = ClubRegistration.objects.get(club_username=user.username, is_approved=True)
        club = club_reg.approved_club  # the linked Club object
    except ClubRegistration.DoesNotExist:
        pass

    return render(request, 'base.html', {'club': club})
