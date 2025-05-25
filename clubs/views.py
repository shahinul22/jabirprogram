from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import ClubRegistration
from user.views import home
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt  # Optional: if CSRF issues

from django.core.mail import send_mail



def club_register(request):
    if request.method == "POST":
        club_username = request.POST["club_username"]
        raw_password = request.POST["password"]
        hashed_password = make_password(raw_password)

        club = ClubRegistration(
            club_username=club_username,
            club_password=hashed_password,
            club_name=request.POST["club_name"],
            club_category=request.POST.get("club_category", ""),
            date_established=request.POST.get("date_established", None),
            president_name=request.POST.get("president_name", ""),
            president_student_id=request.POST.get("president_student_id", ""),
            president_email=request.POST.get("president_email", ""),
            president_phone=request.POST.get("president_phone", ""),
            president_department_year=request.POST.get("president_department_year", ""),
            secretary_name=request.POST.get("secretary_name", ""),
            secretary_student_id=request.POST.get("secretary_student_id", ""),
            secretary_email=request.POST.get("secretary_email", ""),
            secretary_phone=request.POST.get("secretary_phone", ""),
            secretary_department_year=request.POST.get("secretary_department_year", ""),
            treasurer_name=request.POST.get("treasurer_name", ""),
            treasurer_student_id=request.POST.get("treasurer_student_id", ""),
            treasurer_email=request.POST.get("treasurer_email", ""),
            treasurer_phone=request.POST.get("treasurer_phone", ""),
            treasurer_department_year=request.POST.get("treasurer_department_year", ""),
            other_executive_members=request.POST.get("other_executive_members", ""),
            club_constitution=request.POST.get("club_constitution", ""),
            mission_and_vision=request.POST.get("mission_and_vision", ""),
            membership_rules=request.POST.get("membership_rules", ""),
            advisor_name=request.POST.get("advisor_name", ""),
            advisor_contact=request.POST.get("advisor_contact", ""),
            facebook_link=request.POST.get("facebook_link", ""),
            instagram_link=request.POST.get("instagram_link", ""),
            linkedin_link=request.POST.get("linkedin_link", ""),
            youtube_link=request.POST.get("youtube_link", ""),
            website_link=request.POST.get("website_link", ""),
        )
        club.save()
        messages.success(request, "Registration successful! Please wait for approval.")
        return redirect("club_login")

    return render(request, "clubs/register.html")


def club_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            club = ClubRegistration.objects.get(club_username=username)
        except ClubRegistration.DoesNotExist:
            messages.error(request, "Club not found.")
            return redirect("club_login")

        if not club.is_approved:
            messages.warning(request, "Your club is not yet approved.")
            return redirect("club_login")

        # Check hashed password from club_password field
        if check_password(password, club.club_password):
            # Create Django user on first login after approval
            user, created = User.objects.get_or_create(username=club.club_username)
            if created:
                user.set_password(password)
                user.save()
            login(request, user)
            return redirect("home")  # redirect to your dashboard or homepage
        else:
            messages.error(request, "Invalid password.")
            return redirect("club_login")

    return render(request, "clubs/login.html")

@csrf_exempt
def club_detail(request, pk):
    club = get_object_or_404(ClubRegistration, pk=pk)

    if request.method == "POST" and request.user.is_superuser:
        action = request.POST.get("action")

        if action == "approve":
            club.is_approved = True
            club.save()

            # Email notification after approval
            subject = f"Your Club '{club.club_name}' Has Been Approved"
            message = f"""
Dear {club.president_name} and {club.secretary_name},

We are pleased to inform you that your club registration for "{club.club_name}" has been approved by the admin.

You can now log in using your username and password to manage your club activities.

Best regards,  
JU Club Management Team
"""
            recipient_list = []
            if club.president_email:
                recipient_list.append(club.president_email)
            if club.secretary_email:
                recipient_list.append(club.secretary_email)

            if recipient_list:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

            messages.success(request, f"{club.club_name} has been approved and email sent.")
            return redirect("club_detail", pk=pk)

        elif action == "delete":
            reason = request.POST.get("reason")
            email = club.president_email or club.secretary_email

            if email and reason:
                send_mail(
                    subject=f"Your club '{club.club_name}' registration was deleted",
                    message=f"Dear Club,\n\nYour club registration has been deleted by the admin.\n\nReason: {reason}\n\nRegards,\nAdmin Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )

            club.delete()
            messages.warning(request, f"{club.club_name} has been deleted.")
            return redirect("admin_profile")

    return render(request, "clubs/detail.html", {"club": club})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ClubRegistration
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_club(request, club_id):
    club = get_object_or_404(ClubRegistration, id=club_id)

    if request.method == "POST":
        reason = request.POST.get("reason", "No reason provided.")
        subject = f"Your Club '{club.club_name}' Registration Was Rejected"
        message = f"""
Dear {club.president_name} and {club.secretary_name},

We regret to inform you that your club registration for "{club.club_name}" has been declined.

Reason: {reason}

If you have any questions, feel free to contact the admin office.

Best regards,
JU Club Management Admin
"""
        recipient_list = [club.president_email, club.secretary_email]
        send_mail(subject, message, None, recipient_list)

        club.delete()
        messages.success(
            request, f"Club '{club.club_name}' deleted and notification sent."
        )
        return redirect("home")

    return render(request, "clubs/confirm_delete.html", {"club": club})

def club_logout(request):
    logout(request)
    return redirect("home")  # or wherever you want user to land
