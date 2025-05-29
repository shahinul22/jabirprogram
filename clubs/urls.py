from django.urls import path
from .views import (
    club_register,
    club_login,
    club_logout,
    club_profile_view,
    edit_club,
)

app_name = "clubs"  # ✅ Add this line

urlpatterns = [
    path("register/", club_register, name="club_register"),
    path("login/", club_login, name="club_login"),
    path("profile/", club_profile_view, name="club_profile_view"),
    path('edit/<int:club_id>/', edit_club, name='edit_club'),

    # clubs/urls.py
    path("logout/", club_logout, name="club_logout"),


]
