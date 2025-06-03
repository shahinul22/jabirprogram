from django.urls import path
from . import views

app_name = 'events'  # 🔥 This is what was missing

urlpatterns = [
    path('list/', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('create/', views.create_event, name='create_event'),
]
