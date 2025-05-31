from django.db import models


# === Approved Clubs ===

class Club(models.Model):
    name = models.CharField(max_length=255)
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
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department_year = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.role}"


class ClubAdvisor(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='advisors')
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (Advisor - {self.club.name})"


class ClubSocialLink(models.Model):
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name='social_links')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Social links for {self.club.name}"


# === Pending Registration ===

class ClubRegistration(models.Model):
    # Auth Info
    club_username = models.CharField(max_length=150, unique=True)
    club_password = models.CharField(max_length=128)  # Hashed password should be handled properly

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

    # Treasurer Info (optional)
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

    # Approval Status
    is_approved = models.BooleanField(default=False)
    approved_club = models.OneToOneField('Club', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.club_name} (Pending)"

    def approve(self):
        """Approve the registration and create the linked Club and related data."""

        # Create the Club instance
        club = Club.objects.create(
            name=self.club_name,
            category=self.club_category,
            date_established=self.date_established,
            constitution=self.club_constitution,
            mission_and_vision=self.mission_and_vision,
            membership_rules=self.membership_rules,
            description=self.other_executive_members,
            is_active=True,
            logo=None,
            cover_photo=None,
        )

        # Link this ClubRegistration to the new Club
        self.approved_club = club

        # Create members: president and secretary
        ClubMember.objects.bulk_create([
            ClubMember(
                club=club,
                name=self.president_name,
                student_id=self.president_student_id,
                email=self.president_email,
                phone=self.president_phone,
                department_year=self.president_department_year,
                role='president'
            ),
            ClubMember(
                club=club,
                name=self.secretary_name,
                student_id=self.secretary_student_id,
                email=self.secretary_email,
                phone=self.secretary_phone,
                department_year=self.secretary_department_year,
                role='secretary'
            ),
        ])

        # Optional treasurer
        if self.treasurer_name:
            ClubMember.objects.create(
                club=club,
                name=self.treasurer_name,
                student_id=self.treasurer_student_id,
                email=self.treasurer_email,
                phone=self.treasurer_phone,
                department_year=self.treasurer_department_year,
                role='treasurer'
            )

        # Optional advisor
        if self.advisor_name:
            ClubAdvisor.objects.create(
                club=club,
                name=self.advisor_name,
                contact=self.advisor_contact
            )

        # Social media links
        ClubSocialLink.objects.create(
            club=club,
            facebook=self.facebook_link,
            instagram=self.instagram_link,
            linkedin=self.linkedin_link,
            youtube=self.youtube_link,
            website=self.website_link
        )

        # Mark registration as approved
        self.is_approved = True
        self.save()

        return club
