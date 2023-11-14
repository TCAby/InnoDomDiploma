from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SurveyUser
from .forms import SurveyUserRegistrationForm, SurveyUserProfileForm


class SurveyUserAdmin(UserAdmin):
    add_form = SurveyUserRegistrationForm
    form = SurveyUserProfileForm
    model = SurveyUser
    list_display = ("email", "first_name", "is_active", "is_staff", "is_superuser")
    list_filter = ("email", "is_staff", "is_active", )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password", "password2", "is_staff", "is_active"
            )}
         ),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(SurveyUser, SurveyUserAdmin)