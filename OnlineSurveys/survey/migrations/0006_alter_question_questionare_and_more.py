# Generated by Django 4.2.6 on 2023-11-01 08:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_alter_questionare_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionare',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.questionare'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 2, 8, 19, 50, 543427, tzinfo=datetime.timezone.utc), help_text='Date, where the survey will be finished', verbose_name='Date finish'),
        ),
    ]
