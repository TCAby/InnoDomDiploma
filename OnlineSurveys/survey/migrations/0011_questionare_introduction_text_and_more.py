# Generated by Django 4.2.6 on 2023-11-04 18:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_rename_question_text_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionare',
            name='introduction_text',
            field=models.TextField(blank=True, verbose_name='Introduction text'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_from',
            field=models.DateField(db_index=True, default=datetime.date(2023, 11, 4), help_text='Date, where the survey will be started', verbose_name='Date start'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_upto',
            field=models.DateField(default=datetime.date(2023, 11, 5), help_text='Date, where the survey will be finished', verbose_name='Date finish'),
        ),
    ]