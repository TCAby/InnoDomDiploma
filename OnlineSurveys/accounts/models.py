from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# from survey.models import Response

from .managers import SurveyUserManager


class SurveyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, verbose_name='First name')
    last_name = models.CharField(max_length=50, verbose_name='Last name')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='surveyuser_set',
        related_query_name='surveyuser',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = SurveyUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(SurveyUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)


class SurveySession(models.Model):
    user = models.ForeignKey(SurveyUser, on_delete=models.CASCADE, null=True, blank=True)
    responses = models.ManyToManyField('survey.Response')
    session_key = models.CharField(max_length=100)
