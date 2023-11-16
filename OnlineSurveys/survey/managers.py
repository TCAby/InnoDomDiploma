from django.db import models
import datetime

class SurveyManager(models.Manager):
    def active(self):
        return self.filter(activity_status='active')

    def actual(self):
        date_today = datetime.date.today()
        return self.filter(
            activity_status='active',
            date_from__lte=date_today,
            date_upto__gte=date_today
        )
