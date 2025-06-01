# views.py
from clubs.models import ClubRegistration
from user.views import home
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout
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
                return redirect('admin_panel:admin_profile_view')  # ✅ Correct usage
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_panel/login.html', {'form': form})


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from clubs.models import ClubRegistration

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


from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

# from .models import ClubRegistration


from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
# from .models import ClubRegistration 

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
# from .models import ClubRegistration
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from clubs.models import ClubRegistration, Club


@csrf_protect
def club_detail(request, pk):
    club = get_object_or_404(ClubRegistration, pk=pk)
    show_delete_form = False

    if request.method == "POST" and request.user.is_superuser:
        action = request.POST.get("action")

        if action == "approve":
            if club.is_approved:
                messages.warning(request, f"Club '{club.club_name}' has already been approved.")
                return redirect(request.path)

            if Club.objects.filter(name=club.club_name).exists():
                messages.error(request, f"Approval failed: Club '{club.club_name}' already exists!")
                return redirect(request.path)

            try:
                club.approve()

                subject = f"Your Club '{club.club_name}' Has Been Approved"
                message = f"""
Dear {club.president_name} and {club.secretary_name},

We are pleased to inform you that your club registration for "{club.club_name}" has been approved by the admin.

You can now log in using your username and password to manage your club activities.

Best regards,  
JU Club Management Team
"""
                recipient_list = list(filter(None, [club.president_email, club.secretary_email]))
                if recipient_list:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

                messages.success(request, f"{club.club_name} has been approved and notification email sent.")
                return redirect("admin_panel:admin_profile_view")

            except IntegrityError as e:
                messages.error(request, f"Approval failed: {str(e)}")
                return redirect(request.path)

        elif action == "initiate_delete":
            show_delete_form = True

        elif action == "confirm_delete":
            reason = request.POST.get("reason", "").strip()
            email = club.president_email or club.secretary_email

            if reason:
                if email:
                    try:
                        send_mail(
                            subject=f"Your club '{club.club_name}' registration was deleted",
                            message=f"Dear Club,\n\nYour club registration has been deleted by the admin.\n\nReason: {reason}\n\nRegards,\nAdmin Team",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email],
                            fail_silently=True,
                        )
                    except Exception:
                        messages.warning(request, "Failed to send deletion email.")

                # Delete approved club if exists
                if club.approved_club:
                    club.approved_club.delete()

                club.delete()
                messages.warning(request, f"{club.club_name} has been deleted.")
                return redirect("admin_panel:admin_profile_view")
            else:
                messages.error(request, "Please provide a reason for deletion.")

    return render(request, "admin_panel/detail.html", {
        "club": club,
        "show_delete_form": show_delete_form,
    })


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
        messages.success(request, f"Club '{club.club_name}' deleted and notification sent.")
        return redirect("admin_panel:admin_profile_view")  # ✅ Corrected

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
        return redirect("admin_panel:admin_profile_view")  # ✅ Corrected

    return render(request, "admin_panel/confirm_delete.html", {"club": club})


from django.contrib.auth import logout as auth_logout

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("admin_panel:admin_login_view")
