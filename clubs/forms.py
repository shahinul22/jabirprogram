
from django import forms
from .models import ClubRegistration


class ClubRegistrationForm(forms.ModelForm):
    club_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        required=False,
        help_text="Enter new password to change it, or leave blank to keep current."
    )

    class Meta:
        model = ClubRegistration
        exclude = ['is_approved']
        widgets = {
            'date_established': forms.DateInput(attrs={'type': 'date'}),
            'club_constitution': forms.Textarea(attrs={'rows': 4}),
            'mission_and_vision': forms.Textarea(attrs={'rows': 3}),
            'membership_rules': forms.Textarea(attrs={'rows': 3}),
            'other_executive_members': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club_password'].initial = ''


from django import forms
from .models import Club, ClubRegistration

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'category', 'date_established', 'constitution', 'mission_and_vision', 'membership_rules', 'description', 'logo', 'cover_photo']
        widgets = {
            'date_established': forms.DateInput(attrs={'type': 'date'}),
            'constitution': forms.Textarea(attrs={'rows': 4}),
            'mission_and_vision': forms.Textarea(attrs={'rows': 3}),
            'membership_rules': forms.Textarea(attrs={'rows': 3}),
            # description could be Textarea too, add if needed
        }
