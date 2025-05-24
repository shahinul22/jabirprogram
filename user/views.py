from django.shortcuts import render, redirect

# Create your views here.

from clubs.models import ClubRegistration
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

def home(request):
    return render(request, 'base.html')
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('home')  # Updated path to admin-panel/dashboard/
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'user/admin_login.html', {'form': form})


def profile(request):
    approved_clubs = ClubRegistration.objects.filter(is_approved=True)
    pending_clubs = ClubRegistration.objects.filter(is_approved=False)
    context = {
        'approved_clubs': approved_clubs,
        'pending_clubs': pending_clubs
    }
    return render(request, 'shared/profile.html', context)                                                                                         