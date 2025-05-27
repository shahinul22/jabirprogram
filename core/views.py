from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from clubs.models import ClubRegistration

@login_required
def profile_redirect_view(request):
    user = request.user

    if user.is_superuser:
        return redirect('admin_panel:admin_profile_view')  # ✅ fixed name

    elif ClubRegistration.objects.filter(club_username=user.username).exists():
        return redirect('clubs:club_profile')

    else:
        return redirect('user:user_profile')
