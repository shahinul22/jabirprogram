from django.db import models
from django.contrib.auth.models import User

class ClubRegistration(models.Model):
    
    # Auth Info
    club_username = models.CharField(max_length=150, unique=True)
    club_password = models.CharField(max_length=128)  # Will be hashed

    # Club Info
    club_name = models.CharField(max_length=255)
    club_category = models.CharField(max_length=255)
    date_established = models.DateField()

    # President Info
    president_name = models.CharField(max_length=255)
    president_student_id = models.CharField(max_length=50)
    president_email = models.EmailField()
    president_phone = models.CharField(max_length=20)
    president_department_year = models.CharField(max_length=255)

    # Secretary Info
    secretary_name = models.CharField(max_length=255)
    secretary_student_id = models.CharField(max_length=50)
    secretary_email = models.EmailField()
    secretary_phone = models.CharField(max_length=20)
    secretary_department_year = models.CharField(max_length=255)

    # Treasurer Info
    treasurer_name = models.CharField(max_length=255, blank=True)
    treasurer_student_id = models.CharField(max_length=50, blank=True)
    treasurer_email = models.EmailField(blank=True)
    treasurer_phone = models.CharField(max_length=20, blank=True)
    treasurer_department_year = models.CharField(max_length=255, blank=True)

    # Others
    other_executive_members = models.TextField(blank=True)
    club_constitution = models.TextField(blank=True)
    mission_and_vision = models.TextField(blank=True)
    membership_rules = models.TextField(blank=True)

    # Advisor
    advisor_name = models.CharField(max_length=255, blank=True)
    advisor_contact = models.CharField(max_length=255, blank=True)

    # Social Media
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    # Status
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.club_name


