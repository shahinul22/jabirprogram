from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import ClubRegistration


# ========== Private Views ==========
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from clubs.models import ClubRegistration
@login_required
def club_profile_view(request):
    username = request.user.username
    club_reg = ClubRegistration.objects.filter(club_username=username).first()

    if club_reg:
        if club_reg.approved_club:
            return render(request, 'clubs/profile.html', {
                'club': club_reg.approved_club,
                'status': 'approved',
                'club_registration': club_reg  # <-- added this
            })
        else:
            return render(request, 'clubs/profile.html', {
                'club': club_reg,
                'status': 'pending'
            })

    return redirect('clubs:club_register')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ClubRegistration
from .forms import ClubRegistrationForm  # We'll create this form next
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render, redirect
from .models import ClubRegistration
from .forms import ClubRegistrationForm

from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from .forms import ClubForm, ClubRegistrationForm


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from .models import Club, ClubRegistration
from .forms import ClubForm, ClubRegistrationForm  # Make sure these forms exist and are imported
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from .models import Club, ClubRegistration
from .forms import ClubForm, ClubRegistrationForm

def edit_club(request, club_id):
    # 1. Make sure this ID refers to an actual approved club
    club = get_object_or_404(Club, id=club_id)

    # 2. Get matching ClubRegistration row (if any)
    registration = ClubRegistration.objects.filter(approved_club=club).first()

    # 3. POST handling
    if request.method == 'POST':
        form_club = ClubForm(request.POST, request.FILES, instance=club)
        form_registration = ClubRegistrationForm(request.POST, instance=registration)

        if form_club.is_valid() and form_registration.is_valid():
            form_club.save()

            # Save club registration but handle password hashing
            reg_obj = form_registration.save(commit=False)
            new_password = form_registration.cleaned_data.get('club_password')
            if new_password:
                reg_obj.club_password = make_password(new_password)
            reg_obj.approved_club = club  # Ensure correct FK
            reg_obj.save()

            return redirect('clubs:club_profile_view')  # ✅ Adjust to your actual URL name

    # 4. GET handling
    else:
        form_club = ClubForm(instance=club)
        form_registration = ClubRegistrationForm(instance=registration)

    context = {
        'form_club': form_club,
        'form_registration': form_registration,
    }
    return render(request, 'clubs/edit_club.html', context)


# ========== Public Views ==========

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import ClubRegistrationForm

def club_register(request):
    if request.method == "POST":
        form = ClubRegistrationForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            raw_password = form.cleaned_data["club_password"]
            club.club_password = make_password(raw_password)  # hash the password
            club.save()
            messages.success(request, "Registration successful! Please wait for admin approval.")
            return redirect("clubs:club_login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClubRegistrationForm()

    return render(request, "clubs/register.html", {"form": form})



from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ClubRegistration
from django.contrib.auth.models import User

def club_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            club = ClubRegistration.objects.get(club_username=username)
        except ClubRegistration.DoesNotExist:
            messages.error(request, "Club not found.")
            return redirect("clubs:club_login")

        if not club.is_approved:
            messages.warning(request, "Your club is not yet approved.")
            return redirect("clubs:club_login")

        # Check if club.club_password is hashed or plain text.
        # If it's hashed, use check_password.
        # Otherwise, compare directly (NOT recommended for production).
        if check_password(password, club.club_password):
            user, created = User.objects.get_or_create(username=club.club_username)
            if created:
                user.set_password(password)
                user.save()

            login(request, user)
            # Use a URL that definitely exists; if you have 'home', good, else use "/"
            return redirect("home")  # or redirect("/") if 'home' not defined
        else:
            messages.error(request, "Invalid password.")
            return redirect("clubs:club_login")

    return render(request, "clubs/login.html")


from django.contrib.auth import logout
from django.shortcuts import redirect



from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def club_logout(request):
    logout(request)
    return redirect("clubs:club_login")  # Or wherever you want to redirect after logout
