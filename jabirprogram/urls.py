from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from user.views import home
# jabirprogram/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('clubs/', include('clubs.urls', namespace='clubs')),
    path('user/', include('user.urls', namespace='user')),
 
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)