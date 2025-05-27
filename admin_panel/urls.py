# urls.py
from django.urls import path
from .views import (
    admin_login_view,
    admin_profile_view,
    club_detail,
    confirm_delete_view,
    admin_logout_view
)

app_name = "admin_panel"  # ✅ Namespace for URLs

urlpatterns = [
    path("login/", admin_login_view, name="admin_login_view"),
    path("profile/", admin_profile_view, name="admin_profile_view"),
    path("club/<int:pk>/", club_detail, name="club_detail"),
    path("club/<int:pk>/delete/", confirm_delete_view, name="confirm_delete"),
    path("logout/", admin_logout_view, name="admin_logout_view"),
]
