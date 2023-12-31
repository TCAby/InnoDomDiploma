# Generated by Django 4.2.6 on 2023-11-01 08:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_alter_question_questionare_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='Correct?',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='Question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='Allow Multiple',
        ),
        migrations.RemoveField(
            model_name='question',
            name='Question',
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_text',
            field=models.TextField(default='new answer', verbose_name='Answer'),
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, help_text='Is the answer is correct', verbose_name='Correct?'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_allow_multiple_answers',
            field=models.BooleanField(default=False, help_text='Is more than one answer (correct or incorrect) allowed', verbose_name='Multiple answers?'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.TextField(default='new question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='questionare',
            name='date_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 2, 8, 36, 2, 488709, tzinfo=datetime.timezone.utc), help_text='Date, where the survey will be finished', verbose_name='Date finish'),
        ),
    ]
