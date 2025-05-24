from django.urls import path
from . import views 
from user.views import profile, admin_login 

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", admin_login, name="admin_login"),
    path("profile/", profile, name="profile"),
    # path("profile/<int:user_id>/", profile, name="profile_detail"),
]
