from django import forms
from .models import Event, EventRegistration


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'club', 'title', 'description', 'date_time', 'location',
            'organizer_name', 'organizer_contact', 'capacity',
            'visibility', 'event_type', 'registration_deadline',
            'is_paid', 'poster'
        ]
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = [
            'full_name', 'email', 'phone', 'affiliation', 'custom_answers'
        ]
        widgets = {
            'custom_answers': forms.Textarea(attrs={'rows': 3}),
        }
