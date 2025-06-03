from django.db import models
from django.utils import timezone
from clubs.models import Club  # adjust import if Club is nested deeper


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('no_registration', 'No Registration Required'),
        ('registration_required', 'Registration Required'),
    )

    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('internal', 'Internal'),
    )

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer_name = models.CharField(max_length=255)
    organizer_contact = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.club.name})"

    def is_registration_open(self):
        return self.event_type == 'registration_required' and self.registration_deadline and timezone.now() < self.registration_deadline

    def is_full(self):
        if self.capacity:
            return self.registrations.filter(confirmed=True).count() >= self.capacity
        return False


class EventRegistrationQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registration_questions')
    question_text = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f"Q: {self.question_text} ({'Required' if self.is_required else 'Optional'})"


class EventRegistration(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    affiliation = models.CharField(max_length=100)  # e.g. Student, Staff, Guest
    custom_answers = models.JSONField(blank=True, null=True)  # Store answers to additional questions

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    confirmed = models.BooleanField(default=False)
    cancellation_requested = models.BooleanField(default=False)

    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} @ {self.event.title}"


class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
    registration = models.OneToOneField(EventRegistration, on_delete=models.CASCADE)
    checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.registration.full_name} checked in: {self.checked_in}"
