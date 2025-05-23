from django import forms
from .models import ClubRegistration

class ClubRegistrationForm(forms.ModelForm):
    club_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ClubRegistration
        exclude = ['is_approved']
