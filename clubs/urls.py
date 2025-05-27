from django.urls import path
from .views import ( 
            club_register, 
            club_login,
            club_profile_view,
            club_logout_view,
)

app_name = "clubs"  # ✅ Add this line

urlpatterns = [
    path("register/", club_register, name="club_register"),
    path("login/", club_login, name="club_login"),
    path('profile/', club_profile_view, name='club_profile'),
    path("logout/club/", club_logout_view, name="club_logout"),
]
