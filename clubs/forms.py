from django import forms
from django.contrib.auth.hashers import make_password
from .models import ClubRegistration, Club

class ClubRegistrationForm(forms.ModelForm):
    club_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        required=False,
        help_text="Leave blank to keep the current password."
    )

    class Meta:
        model = ClubRegistration
        exclude = ['is_approved', 'approved_club']
        widgets = {
            'date_established': forms.DateInput(attrs={'type': 'date'}),
            'club_constitution': forms.Textarea(attrs={'rows': 4}),
            'mission_and_vision': forms.Textarea(attrs={'rows': 3}),
            'membership_rules': forms.Textarea(attrs={'rows': 3}),
            'other_executive_members': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club_password'].initial = ''  # never prefill password

    def clean_club_password(self):
        password = self.cleaned_data.get('club_password')

        # If user left the password blank on update, return old one
        if not password and self.instance.pk:
            return self.instance.club_password
        
        return password  # Raw password will be hashed in model


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            'name', 'category', 'date_established', 'constitution',
            'mission_and_vision', 'membership_rules', 'description',
            'logo', 'cover_photo'
        ]
        widgets = {
            'date_established': forms.DateInput(attrs={'type': 'date'}),
            'constitution': forms.Textarea(attrs={'rows': 4}),
            'mission_and_vision': forms.Textarea(attrs={'rows': 3}),
            'membership_rules': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }




from django import forms
from .models import ClubMember

class ClubMemberForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        fields = ['name', 'student_id', 'email', 'phone', 'session', 'department', 'role', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'student_id': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'session': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'department': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'role': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
        }
