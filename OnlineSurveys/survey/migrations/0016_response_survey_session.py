# Generated by Django 4.2.6 on 2023-11-07 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_surveysession'),
        ('survey', '0015_alter_questionare_date_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='survey_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.surveysession'),
        ),
    ]
