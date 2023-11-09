# Generated by Django 4.2.6 on 2023-11-09 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0016_response_survey_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionare',
            name='date_from',
            field=models.DateField(db_index=True, default=datetime.date(2023, 11, 9), help_text='Date, where the survey will be started', verbose_name='Date start'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_upto',
            field=models.DateField(default=datetime.date(2023, 11, 10), help_text='Date, where the survey will be finished', verbose_name='Date finish'),
        ),
    ]
