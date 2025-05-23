from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ClubRegistration
from user.views import home

def club_register(request):
    if request.method == 'POST':
        club_username = request.POST['club_username']
        raw_password = request.POST['password']
        hashed_password = make_password(raw_password)

        club = ClubRegistration(
            club_username=club_username,
            club_password=hashed_password,

            club_name=request.POST['club_name'],
            club_category=request.POST.get('club_category', ''),
            date_established=request.POST.get('date_established', None),

            president_name=request.POST.get('president_name', ''),
            president_student_id=request.POST.get('president_student_id', ''),
            president_email=request.POST.get('president_email', ''),
            president_phone=request.POST.get('president_phone', ''),
            president_department_year=request.POST.get('president_department_year', ''),

            secretary_name=request.POST.get('secretary_name', ''),
            secretary_student_id=request.POST.get('secretary_student_id', ''),
            secretary_email=request.POST.get('secretary_email', ''),
            secretary_phone=request.POST.get('secretary_phone', ''),
            secretary_department_year=request.POST.get('secretary_department_year', ''),

            treasurer_name=request.POST.get('treasurer_name', ''),
            treasurer_student_id=request.POST.get('treasurer_student_id', ''),
            treasurer_email=request.POST.get('treasurer_email', ''),
            treasurer_phone=request.POST.get('treasurer_phone', ''),
            treasurer_department_year=request.POST.get('treasurer_department_year', ''),

            other_executive_members=request.POST.get('other_executive_members', ''),
            club_constitution=request.POST.get('club_constitution', ''),
            mission_and_vision=request.POST.get('mission_and_vision', ''),
            membership_rules=request.POST.get('membership_rules', ''),

            advisor_name=request.POST.get('advisor_name', ''),
            advisor_contact=request.POST.get('advisor_contact', ''),

            facebook_link=request.POST.get('facebook_link', ''),
            instagram_link=request.POST.get('instagram_link', ''),
            linkedin_link=request.POST.get('linkedin_link', ''),
            youtube_link=request.POST.get('youtube_link', ''),
            website_link=request.POST.get('website_link', '')
        )
        club.save()
        messages.success(request, "Registration successful! Please wait for approval.")
        return redirect('club_login')

    return render(request, 'clubs/register.html')


def club_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            club = ClubRegistration.objects.get(club_username=username)
        except ClubRegistration.DoesNotExist:
            messages.error(request, 'Club not found.')
            return redirect('club_login')

        if not club.is_approved:
            messages.warning(request, 'Your club is not yet approved.')
            return redirect('club_login')

        # Check hashed password from club_password field
        if check_password(password, club.club_password):
            # Create Django user on first login after approval
            user, created = User.objects.get_or_create(username=club.club_username)
            if created:
                user.set_password(password)
                user.save()
            login(request, user)
            return redirect('home')  # redirect to your dashboard or homepage
        else:
            messages.error(request, 'Invalid password.')
            return redirect('club_login')

    return render(request, 'clubs/login.html')
