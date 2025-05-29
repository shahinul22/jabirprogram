from django.contrib import admin
from .models import Club, ClubMember, ClubAdvisor, ClubSocialLink, ClubRegistration

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date_established', 'is_active')

@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'club')

@admin.register(ClubAdvisor)
class ClubAdvisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'club')

@admin.register(ClubSocialLink)
class ClubSocialLinkAdmin(admin.ModelAdmin):
    list_display = ('club',)

@admin.register(ClubRegistration)
class ClubRegistrationAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'club_username', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('club_name', 'club_username')

    actions = ['approve_clubs']

    def approve_clubs(self, request, queryset):
        for registration in queryset.filter(is_approved=False):
            registration.approve()
        self.message_user(request, "Selected clubs have been approved.")
    approve_clubs.short_description = "Approve selected club registrations"
