# Generated by Django 4.2.6 on 2023-11-09 10:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0003_surveysession'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveyuser',
            options={},
        ),
        migrations.AlterModelManagers(
            name='surveyuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='surveyuser',
            name='role',
        ),
        migrations.RemoveField(
            model_name='surveyuser',
            name='survey_data',
        ),
        migrations.RemoveField(
            model_name='surveyuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]