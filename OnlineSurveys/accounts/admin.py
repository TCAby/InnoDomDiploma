from django.contrib import admin
from .models import SurveyUser
from django.contrib.auth.admin import UserAdmin
from .forms import SurveyUserRegistrationForm, SurveyUserProfileForm

admin.site.register(SurveyUser)


class SurveyUserAdmin(UserAdmin):
    add_form = SurveyUserRegistrationForm
    form = SurveyUserProfileForm
    model = SurveyUser
    list_display = ("first_name", "email", "is_staff", "is_active", "last_login", "date_joined", "role", )
    list_filter = ("first_name", "email", "is_staff", "is_active", "last_login", "date_joined", "role", )
    fieldsets = (
        (None, {"fields": ("username", "first_name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "first_name", "email", "password", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)