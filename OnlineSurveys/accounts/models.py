from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
# from survey.models import Response


class SurveyUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('registered', 'Registered User'),
        ('anonymous', 'Anonymous'),
    )

    role = models.CharField(max_length=20, choices=ROLES, default='anonymous')
    survey_data = models.TextField(blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='surveyuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='surveyuser_set',
        related_query_name='user',
    )


class UserProfile(models.Model):
    user = models.OneToOneField(SurveyUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)


class SurveySession(models.Model):
    user = models.ForeignKey(SurveyUser, on_delete=models.CASCADE)
    responses = models.ManyToManyField('survey.Response')
    session_key = models.CharField(max_length=100)
