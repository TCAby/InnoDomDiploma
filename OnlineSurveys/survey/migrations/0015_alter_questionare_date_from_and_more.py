# Generated by Django 4.2.6 on 2023-11-07 10:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_userprofiles_userprofile'),
        ('survey', '0014_alter_response_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionare',
            name='date_from',
            field=models.DateField(db_index=True, default=datetime.date(2023, 11, 7), help_text='Date, where the survey will be started', verbose_name='Date start'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_upto',
            field=models.DateField(default=datetime.date(2023, 11, 8), help_text='Date, where the survey will be finished', verbose_name='Date finish'),
        ),
        migrations.AlterField(
            model_name='response',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.surveyuser'),
        ),
    ]
