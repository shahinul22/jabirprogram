from django.urls import path
from . import views 
from user.views import profile, admin_login 
from .views import home
urlpatterns = [
    path("", home, name="home"),
    path("superAdmin/login/", admin_login, name="admin_login"),
    path("profile/", profile, name="profile"),
    # path("profile/<int:user_id>/", profile, name="profile_detail"),
]
