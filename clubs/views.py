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


# clubs/views.py
def club_profile_tab_view(request, tab):
    # Get the club registration for the current user
    try:
        club_reg = ClubRegistration.objects.get(club_username=request.user.username)
    except ClubRegistration.DoesNotExist:
        messages.error(request, "Club registration not found.")
        return redirect('clubs:club_profile')
    
    if not club_reg.is_approved or not club_reg.approved_club:
        messages.warning(request, "Your club is not approved yet.")
        return redirect('clubs:club_profile')
    
    club = club_reg.approved_club
    context = {
        'club': club,
        'active_tab': tab,
        'status': 'approved',
        'club_registration': club_reg
    }
    
    return render(request, 'clubs/profile.html', context)

    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Club, ClubRegistration
from .forms import ClubForm, ClubRegistrationForm

@login_required
def edit_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    registration = ClubRegistration.objects.filter(approved_club=club).first()

    if request.method == 'POST':
        form_club = ClubForm(request.POST, request.FILES, instance=club)
        form_registration = ClubRegistrationForm(request.POST, instance=registration)

        if form_club.is_valid() and form_registration.is_valid():
            form_club.save()
            reg_obj = form_registration.save(commit=False)

            # Handle password update
            new_password = form_registration.cleaned_data.get('club_password')
            if new_password:
                reg_obj.club_password = make_password(new_password)

            # Handle username change and prevent duplicates
            old_username = request.user.username
            new_username = form_registration.cleaned_data.get('club_username')

            if old_username != new_username:
                if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                    form_registration.add_error('club_username', "This username is already taken.")
                    context = {
                        'form_club': form_club,
                        'form_registration': form_registration,
                        'club': club,
                        'registration': registration,
                    }
                    return render(request, 'clubs/edit_club.html', context)

                # Update the request.user.username
                request.user.username = new_username
                request.user.save()

            reg_obj.approved_club = club
            reg_obj.save()

            messages.success(request, "Club information updated successfully.")
            return redirect('clubs:club_profile_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form_club = ClubForm(instance=club)
        form_registration = ClubRegistrationForm(instance=registration)

    context = {
        'form_club': form_club,
        'form_registration': form_registration,
        'club': club,
        'registration': registration,
    }
    return render(request, 'clubs/edit_club.html', context)

# ========== Public Views ==========

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import ClubRegistrationForm

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import ClubRegistrationForm

def club_register(request):
    if request.method == "POST":
        form = ClubRegistrationForm(request.POST)
        if form.is_valid():
            try:
                club = form.save(commit=False)
                raw_password = form.cleaned_data["club_password"]
                club.club_password = make_password(raw_password)
                club.save()
                messages.success(request, "✅ Registration successful! Await admin approval.")
                return redirect("clubs:club_login")
            except Exception as e:
                messages.error(request, f"Error saving form: {e}")
        else:
            # Log form errors for debugging
            print("Form errors:", form.errors)
            messages.error(request, "❌ Please fix the errors below.")
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

# clubs/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Club, ClubMember

@login_required
def club_members_view(request):
    # Get the club registration for the current user
    try:
        club_reg = ClubRegistration.objects.get(club_username=request.user.username)
    except ClubRegistration.DoesNotExist:
        messages.error(request, "Club registration not found.")
        return redirect('clubs:club_profile_view')
    
    # Redirect if club not approved
    if not club_reg.is_approved or not club_reg.approved_club:
        messages.warning(request, "Your club is not approved yet.")
        return redirect('clubs:club_profile_view')
    
    club = club_reg.approved_club
    members = ClubMember.objects.filter(club=club)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(members, 10)  # Show 10 members per page
    
    try:
        members_page = paginator.page(page)
    except PageNotAnInteger:
        members_page = paginator.page(1)
    except EmptyPage:
        members_page = paginator.page(paginator.num_pages)

    context = {
        'club': club,
        'members_page': members_page,
    }
    return render(request, 'clubs/members.html', context)

from .forms import ClubMemberForm


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

def add_member(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    
    if request.method == 'POST':
        form = ClubMemberForm(request.POST, request.FILES)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            
            # Check if student_id already exists in this club
            if club.members.filter(student_id=student_id).exists():
                messages.error(request, "A member with this student ID already exists in the club.")
            else:
                member = form.save(commit=False)
                member.club = club
                member.save()
                
                messages.success(request, "New member added successfully!")
                return redirect('clubs:club_profile_members')

    else:
        form = ClubMemberForm()

    return render(request, 'clubs/add_member.html', {
        'form': form,
        'club': club,
    })

def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    # Render the detail template or redirect as needed
    return render(request, 'clubs/club_detail.html', {'club': club})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def club_logout(request):
    logout(request)
    return redirect("clubs:club_login")  # Or wherever you want to redirect after logout


