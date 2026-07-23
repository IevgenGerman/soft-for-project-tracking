from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from monitor.models import Language, Location, Project, Team, TeamMember


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "country")
    search_fields = ("city", "country")
    exclude = ("slug",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    exclude = ("slug",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "team",
        "start_date",
        "progress_percent",
        "payment_percent",
    )
    list_filter = ("team", "location")
    search_fields = ("name",)
    exclude = ("slug",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TeamMember)
class TeamMemberAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "team",
        "role",
        "years_of_experience",
        "license_number",
    )
    list_filter = UserAdmin.list_filter + ("team", "role")
    filter_horizontal = UserAdmin.filter_horizontal + ("languages",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Team info",
            {
                "fields": (
                    "team",
                    "role",
                    "years_of_experience",
                    "license_number",
                    "languages",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "Team info",
            {
                "fields": (
                    "team",
                    "role",
                    "years_of_experience",
                    "license_number",
                    "languages",
                )
            },
        ),
    )
