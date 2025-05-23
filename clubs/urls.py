from django.urls import path
from .views import club_register, club_login, club_logout

urlpatterns = [
    path('register-club/', club_register, name='club-register'),
    path('register/', club_register, name='club_register'),
    path('login/', club_login, name='club_login'),
    path('logout/', club_logout, name='club_logout')
]
