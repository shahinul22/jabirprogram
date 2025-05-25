from django.urls import path
from .views import (
    club_register, club_login, club_logout, club_detail,
    delete_club
)
urlpatterns = [
    path('register-club/', club_register, name='club-register'),
    path('register/', club_register, name='club_register'),
    path('login/', club_login, name='club_login'),
    path('details/<int:pk>/', club_detail, name='club_detail'), 
    path('club/<int:club_id>/delete/', delete_club, name='delete_club'),
    path('logout/', club_logout, name='club_logout')
]
