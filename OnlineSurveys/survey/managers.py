from django.db.models.manager import Manager
from django.db import models
import datetime

class SurveyManager(models.Manager):
    def active(self) -> Manager:
        return self.filter(activity_status='active')

    def actual(self) -> Manager:
        date_today = datetime.date.today()
        return self.filter(
            activity_status='active',
            date_from__lte=date_today,
            date_upto__gte=date_today
        )

    def is_daterange_actual(self, id:int) -> bool:
        date_today = datetime.date.today()
        return self.filter(
            id=id,
            activity_status='active',
            date_from__lte=date_today,
            date_upto__gte=date_today
        ).exists()
