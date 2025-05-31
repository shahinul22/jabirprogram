# clubs/urls.py
from django.urls import path
from .views import (
    club_register,
    club_login,
    club_logout,
    club_profile_view,
    edit_club,
    club_profile_tab_view
)

app_name = "clubs"

urlpatterns = [
    path("register/", club_register, name="club_register"),
    path("login/", club_login, name="club_login"),
    path("profile/", club_profile_tab_view,  {'tab': 'about'}, name="club_profile_about"),
    path('edit/<int:club_id>/', edit_club, name='edit_club'),
    path("logout/", club_logout, name="club_logout"),
    
    # Tab-specific URLs
    path("profile/about/", club_profile_tab_view, {'tab': 'about'}, name='club_profile_about'),
    path("profile/members/", club_profile_tab_view, {'tab': 'members'}, name='club_profile_members'),
    path("profile/events/", club_profile_tab_view, {'tab': 'events'}, name='club_profile_events'),
    path("profile/gallery/", club_profile_tab_view, {'tab': 'gallery'}, name='club_profile_gallery'),
    path("profile/resources/", club_profile_tab_view, {'tab': 'resources'}, name='club_profile_resources'),
]