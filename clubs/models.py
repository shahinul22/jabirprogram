from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# === Approved Clubs ===
class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    date_established = models.DateField()
    constitution = models.TextField(blank=True)
    mission_and_vision = models.TextField(blank=True)
    membership_rules = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='club_covers/', blank=True, null=True)

    def __str__(self):
        return self.name





class ClubMember(models.Model):
    ROLE_CHOICES = (
        # Core Executive Team
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('secretary', 'Secretary'),
        ('joint_secretary', 'Joint Secretary'),
        ('assistant_secretary', 'Assistant Secretary'),
        ('organizing_secretary', 'Organizing Secretary'),    
        ('treasurer', 'Treasurer'),
        ('financial_controller', 'Financial Controller'),

        # Operational Roles
        ('event_manager', 'Event Manager'),
        ('event_coordinator', 'Event Coordinator'),
        ('logistics_head', 'Logistics Head'),
        ('operations_manager', 'Operations Manager'),

        # Communications
        ('pr_officer', 'Public Relations Officer'),
        ('communications_officer', 'Communications Officer'),
        ('media_coordinator', 'Media Coordinator'),
        ('social_media_manager', 'Social Media Manager'),

        # Creative & Technical
        ('creative_director', 'Creative Director'),
        ('design_head', 'Design Head'),
        ('technical_head', 'Technical Head'),
        ('content_creator', 'Content Creator'),
        ('graphic_designer', 'Graphic Designer'),
        ('webmaster', 'Webmaster'),
        ('photographer', 'Photographer'),
        ('videographer', 'Videographer'),

        # Membership & Outreach
        ('membership_coordinator', 'Membership Coordinator'),
        ('outreach_coordinator', 'Outreach Coordinator'),
        ('partnership_coordinator', 'Partnership Coordinator'),
        ('fundraising_officer', 'Fundraising Officer'),
        ('alumni_relations', 'Alumni Relations Officer'),

        # Specialized Departments
        ('cultural_secretary', 'Cultural Secretary'),
        ('sports_secretary', 'Sports Secretary'),
        ('academic_head', 'Academic Head'),
        ('research_head', 'Research Head'),
        ('training_head', 'Training Head'),
        ('welfare_officer', 'Welfare Officer'),
        ('equity_officer', 'Equity Officer'),

        # Advisory & Support
        ('faculty_advisor', 'Faculty Advisor'),
        ('mentor', 'Mentor'),
        ('legal_advisor', 'Legal Advisor'),
        ('auditor', 'Auditor'),

        # General Roles
        ('project_manager', 'Project Manager'),
        ('volunteer_coordinator', 'Volunteer Coordinator'),
        ('general_member', 'General Member'),
        ('executive_member', 'Executive Member'),
    )
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    session = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=255, default='Not Specified')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(default=timezone.now)

    # ✅ Leave date for inactive members
    leave_date = models.DateField(blank=True, null=True)

    # ✅ Photo field
    photo = models.ImageField(upload_to='member_photos/', blank=True, null=True)

    class Meta:
        unique_together = ('club', 'student_id')

    def save(self, *args, **kwargs):
        if not self.is_active and self.leave_date is None:
            self.leave_date = timezone.now().date()
        elif self.is_active:
            self.leave_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.role} - {self.club.name})"


class ClubAdvisor(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='advisors')
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Advisor - {self.club.name})"


class ClubSocialLink(models.Model):
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name='social_links')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return f"Social links for {self.club.name}"


# === Pending Registration ===
from django.db import models
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import is_password_usable
from django.db import models, IntegrityError
from django.contrib.auth.hashers import make_password
from django.utils import timezone



class ClubRegistration(models.Model):
    # Auth Info
    club_username = models.CharField(max_length=150, unique=True)
    club_password = models.CharField(max_length=128)

    # Club Info
    club_name = models.CharField(max_length=255)
    club_category = models.CharField(max_length=255)
    date_established = models.DateField()

    # President Info
    president_name = models.CharField(max_length=255)
    president_student_id = models.CharField(max_length=50)
    president_email = models.EmailField()
    president_phone = models.CharField(max_length=20)
    president_session = models.CharField(max_length=20)
    president_department = models.CharField(max_length=255)

    # Secretary Info
    secretary_name = models.CharField(max_length=255)
    secretary_student_id = models.CharField(max_length=50)
    secretary_email = models.EmailField()
    secretary_phone = models.CharField(max_length=20)
    secretary_session = models.CharField(max_length=20)
    secretary_department = models.CharField(max_length=255)

    # Organizing Secretary
    organizing_secretary_name = models.CharField(max_length=255)
    organizing_secretary_student_id = models.CharField(max_length=50)
    organizing_secretary_email = models.EmailField()
    organizing_secretary_phone = models.CharField(max_length=20)
    organizing_secretary_session = models.CharField(max_length=20)
    organizing_secretary_department = models.CharField(max_length=255)

    # Other Details
    other_executive_members = models.TextField(blank=True)
    club_constitution = models.TextField(blank=True)
    mission_and_vision = models.TextField(blank=True)
    membership_rules = models.TextField(blank=True)

    # Advisor
    advisor_name = models.CharField(max_length=255, blank=True)
    advisor_contact = models.CharField(max_length=255, blank=True)
    advisor_email = models.EmailField(blank=True, default='')
    advisor_department = models.CharField(max_length=255, blank=True, default='')

    # Social Media
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    # Approval Info
    is_approved = models.BooleanField(default=False)
    approved_club = models.OneToOneField('Club', null=True, blank=True, on_delete=models.SET_NULL)

    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.club_password.startswith('pbkdf2_'):
            self.club_password = make_password(self.club_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.club_name} ({'Approved' if self.is_approved else 'Pending'})"

    @property
    def status(self):
        return "Approved" if self.is_approved else "Pending"

    def approve(self):
        from .models import Club, ClubMember, ClubAdvisor, ClubSocialLink

        club = Club.objects.create(
            name=self.club_name,
            category=self.club_category,
            date_established=self.date_established,
            constitution=self.club_constitution,
            mission_and_vision=self.mission_and_vision,
            membership_rules=self.membership_rules,
            description=self.other_executive_members,
            is_active=True
        )

        executive_members = [
            {
                'name': self.president_name,
                'student_id': self.president_student_id,
                'email': self.president_email,
                'phone': self.president_phone,
                'session': self.president_session,
                'department': self.president_department,
                'role': 'president'
            },
            {
                'name': self.secretary_name,
                'student_id': self.secretary_student_id,
                'email': self.secretary_email,
                'phone': self.secretary_phone,
                'session': self.secretary_session,
                'department': self.secretary_department,
                'role': 'secretary'
            },
            {
                'name': self.organizing_secretary_name,
                'student_id': self.organizing_secretary_student_id,
                'email': self.organizing_secretary_email,
                'phone': self.organizing_secretary_phone,
                'session': self.organizing_secretary_session,
                'department': self.organizing_secretary_department,
                'role': 'organizing_secretary'
            }
        ]

        for member in executive_members:
            if member['name'] and member['student_id']:
                exists = ClubMember.objects.filter(club=club, student_id=member['student_id']).exists()
                if not exists:
                    ClubMember.objects.create(club=club, **member)

        if self.advisor_name:
            ClubAdvisor.objects.create(
                club=club,
                name=self.advisor_name,
                contact=self.advisor_contact,
                email=self.advisor_email,
                department=self.advisor_department
            )

        ClubSocialLink.objects.create(
            club=club,
            facebook=self.facebook_link,
            instagram=self.instagram_link,
            linkedin=self.linkedin_link,
            youtube=self.youtube_link,
            website=self.website_link
        )

        self.is_approved = True
        self.approved_club = club
        self.reviewed_at = timezone.now()
        self.save()


#  for event 
