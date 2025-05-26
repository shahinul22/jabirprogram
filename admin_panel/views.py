# views.py
from clubs.models import ClubRegistration
from user.views import home
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                auth_login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_panel/login.html', {'form': form})

    
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_profile_view(request):
    approved_clubs = ClubRegistration.objects.filter(is_approved=True)
    pending_clubs = ClubRegistration.objects.filter(is_approved=False)
    context = {
        'approved_clubs': approved_clubs,
        'pending_clubs': pending_clubs
    }
    return render(request, 'admin_panel/profile.html', context)


@csrf_exempt
def club_detail(request, pk):
    club = get_object_or_404(ClubRegistration, pk=pk)
    show_delete_form = False

    if request.method == "POST" and request.user.is_superuser:
        action = request.POST.get("action")

        if action == "approve":
            club.is_approved = True
            club.save()

            subject = f"Your Club '{club.club_name}' Has Been Approved"
            message = f"""
Dear {club.president_name} and {club.secretary_name},

We are pleased to inform you that your club registration for \"{club.club_name}\" has been approved by the admin.

You can now log in using your username and password to manage your club activities.

Best regards,  
JU Club Management Team
"""
            recipient_list = list(filter(None, [club.president_email, club.secretary_email]))
            if recipient_list:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

            messages.success(request, f"{club.club_name} has been approved and email sent.")
            return redirect("club_detail", pk=pk)

        elif action == "initiate_delete":
            show_delete_form = True

        elif action == "confirm_delete":
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

    return render(request, "admin_panel/detail.html", {"club": club, "show_delete_form": show_delete_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_club(request, club_id):
    club = get_object_or_404(ClubRegistration, id=club_id)

    if request.method == "POST":
        reason = request.POST.get("reason", "No reason provided.")
        subject = f"Your Club '{club.club_name}' Registration Was Rejected"
        message = f"""
Dear {club.president_name} and {club.secretary_name},

We regret to inform you that your club registration for \"{club.club_name}\" has been declined.

Reason: {reason}

If you have any questions, feel free to contact the admin office.

Best regards,
JU Club Management Admin
"""
        recipient_list = [club.president_email, club.secretary_email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        club.delete()
        messages.success(
            request, f"Club '{club.club_name}' deleted and notification sent."
        )
        return redirect("home")

    return render(request, "admin_panel/confirm_delete.html", {"club": club})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def confirm_delete_view(request, pk):
    club = get_object_or_404(ClubRegistration, pk=pk)

    if request.method == "POST":
        reason = request.POST.get("reason", "No reason provided.")
        subject = f"Club '{club.club_name}' Registration Rejected"
        message = f"""
Dear {club.president_name} and {club.secretary_name},

We regret to inform you that your club registration for \"{club.club_name}\" has been declined.

Reason: {reason}

Regards,  
JU Club Management Admin
"""
        recipient_list = list(filter(None, [club.president_email, club.secretary_email]))
        if recipient_list:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        club.delete()
        messages.warning(request, f"{club.club_name} has been deleted and notification sent.")
        return redirect("home")

    return render(request, "admin_panel/confirm_delete.html", {"club": club})
