from django.contrib import admin
from .models import Event, EventRegistration, EventRegistrationQuestion, EventAttendance

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'event_type', 'date_time', 'visibility', 'is_paid')
    list_filter = ('event_type', 'visibility', 'club', 'is_paid')
    search_fields = ('title', 'description', 'organizer_name')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'email', 'payment_status', 'confirmed', 'registered_at')
    list_filter = ('event', 'payment_status', 'confirmed')
    search_fields = ('full_name', 'email')


@admin.register(EventRegistrationQuestion)
class EventRegistrationQuestionAdmin(admin.ModelAdmin):
    list_display = ('event', 'question_text', 'is_required')
    list_filter = ('event',)


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ('registration', 'event', 'checked_in', 'check_in_time')
    list_filter = ('checked_in',)
