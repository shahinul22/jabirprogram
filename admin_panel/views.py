from django.shortcuts import render, redirect
from clubs.models import ClubRegistration
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login  # ✅ Rename to avoid conflict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def admin_login_view(request):  # ✅ Renamed from 'login'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                auth_login(request, user)  # ✅ Now calls the correct login()
                return redirect('profile')  # Or 'admin_dashboard' if you have one
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_panel/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_profile_view(request):  # ✅ Renamed to avoid duplication
    approved_clubs = ClubRegistration.objects.filter(is_approved=True)
    pending_clubs = ClubRegistration.objects.filter(is_approved=False)
    context = {
        'approved_clubs': approved_clubs,
        'pending_clubs': pending_clubs
    }
    return render(request, 'admin_panel/profile.html', context)
