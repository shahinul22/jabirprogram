from django.urls import path
from .views import home, user_profile_view
app_name = "user"  # ✅ Add this line

urlpatterns = [
    # path("", home, name="home"),
    # path("profile/", user_profile_view, name="user_profile"),
    # path("logout/user/", user_logout_view, name="user_logout"),
    
]
