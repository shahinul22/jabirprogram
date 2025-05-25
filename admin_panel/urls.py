from django.urls import path
from .views import admin_login_view, admin_profile_view

urlpatterns = [
    path("login/", admin_login_view, name="admin_login"),  # ✅ Renamed
    path("profile/", admin_profile_view, name="profile"),   # ✅ Renamed
]
