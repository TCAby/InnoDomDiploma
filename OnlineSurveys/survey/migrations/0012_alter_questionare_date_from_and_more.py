# Generated by Django 4.2.6 on 2023-11-05 13:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0011_questionare_introduction_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionare',
            name='date_from',
            field=models.DateField(db_index=True, default=datetime.date(2023, 11, 5), help_text='Date, where the survey will be started', verbose_name='Date start'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_upto',
            field=models.DateField(default=datetime.date(2023, 11, 6), help_text='Date, where the survey will be finished', verbose_name='Date finish'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.question')),
                ('questionare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.questionare')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
