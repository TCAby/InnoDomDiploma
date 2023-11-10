from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SurveyUser
from .forms import SurveyUserRegistrationForm, SurveyUserProfileForm


class SurveyUserAdmin(UserAdmin):
    add_form = SurveyUserRegistrationForm
    form = SurveyUserProfileForm
    model = SurveyUser
    # list_display = ("first_name", "email", "is_staff", "is_active", "last_login", "date_joined", "role", )
    # list_filter = ("first_name", "email", "is_staff", "is_active", "last_login", "date_joined", "role", )
    list_display = ("email", "first_name", "is_active", "is_staff", "is_superuser")
    list_filter = ("email", "is_staff", "is_active", )
    '''
    fieldsets = (
        (None, {"fields": ("first_name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    '''
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    '''
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "email", "password", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    '''
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