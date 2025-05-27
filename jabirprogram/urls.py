from django.contrib import admin
from django.urls import path, include
from core.views import profile_redirect_view  # assuming it's in main app
from user.views import home
# jabirprogram/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('clubs/', include('clubs.urls', namespace='clubs')),
    path('user/', include('user.urls', namespace='user')),
    path('profile/', profile_redirect_view, name='profile')
 
]
