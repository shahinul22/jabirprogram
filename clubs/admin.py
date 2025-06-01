# clubs/admin.py
from django.contrib import admin
from .models import Club, ClubRegistration, ClubMember, ClubAdvisor, ClubSocialLink

from django.contrib import admin
from .models import ClubRegistration

@admin.register(ClubRegistration)
class ClubRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'club_name',
        'club_category',
        'status',
        'submitted_at',
        'reviewed_at'
    ]
    list_filter = [
        'club_category',
        'submitted_at',
        'is_approved'
    ]
    search_fields = ['club_name', 'club_username']
    readonly_fields = ['submitted_at', 'reviewed_at']
    actions = ['approve_registrations']

    def approve_registrations(self, request, queryset):
        approved_count = 0
        for registration in queryset:
            if not registration.is_approved:
                try:
                    registration.approve()
                    approved_count += 1
                except Exception as e:
                    self.message_user(request, f"Failed to approve {registration.club_name}: {e}", level='error')
        self.message_user(request, f"Successfully approved {approved_count} registrations")
    approve_registrations.short_description = "Approve selected registrations"

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'date_established']
    list_filter = ['is_active', 'category']
    search_fields = ['name']
    # readonly_fields = ['created_at', 'updated_at']
    readonly_fields = ()


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'club', 'role', 'is_active']
    list_filter = ['club', 'role', 'is_active']
    search_fields = ['name', 'student_id']
    raw_id_fields = ['club']

@admin.register(ClubAdvisor)
class ClubAdvisorAdmin(admin.ModelAdmin):
    list_display = ['name', 'club', 'is_primary']
    list_filter = ['is_primary', 'club']
    search_fields = ['name']

@admin.register(ClubSocialLink)
class ClubSocialLinkAdmin(admin.ModelAdmin):
    list_display = ['club', 'website']
    search_fields = ['club__name']