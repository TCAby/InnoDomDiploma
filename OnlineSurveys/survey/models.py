import datetime

from django.utils import timezone
from django.db import models
from datetime import timedelta
from django.urls import reverse

# Create your models here.


class Questionare(models.Model):
    """Class represent top level of Survey

    Args:
        models.Model (_type_): _description_
        
    Return:
        __str__ returns <type 'str'> title of the Survey
    """
    ACTIVITY_STATUS = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspend', 'Suspended'),
    )

    # Fields
    title = models.CharField(max_length=100, verbose_name='Survey Name', blank=False, default="New survey")
    activity_status = models.CharField(max_length=10, choices=ACTIVITY_STATUS, default='draft', db_index=True, verbose_name="Survey's Activity Status")
    date_from = models.DateField(default=datetime.date.today(), db_index=True, verbose_name="Date start", help_text="Date, where the survey will be started")
    date_upto = models.DateField(default=datetime.date.today() + datetime.timedelta(days=1), verbose_name="Date finish", help_text="Date, where the survey will be finished")
    is_anonymous = models.BooleanField(verbose_name='Allow Annonimouse', default=True)
    
    # Metadata
    class Meta:
        ordering = ("-date_from", "activity_status")

    # Methods
    def __str__(self) -> str:
        """
        String for representing the Questionare object (in Admin site etc.)
        """
        return str(self.title)
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Questionaire.
        """
        return reverse('model-detail-view', args=[str(self.title)])


class Question(models.Model):
    # Fields
    questionare = models.ForeignKey(Questionare, on_delete=models.SET_NULL, null=True)
    text = models.TextField(name="text", verbose_name="Question", blank=False, default="new question")
    is_allow_multiple_answers = models.BooleanField(name='is_allow_multiple_answers', verbose_name='Multiple answers?', help_text='Is more than one answer (correct or incorrect) allowed', default=False)

    # Methods
    def __str__(self) -> str:
        """
        String for representing the Question object (in Admin site etc.)
        """
        return str(self.text)


class Answer(models.Model):
    # Fields
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(name="answer_text", verbose_name="Answer", blank=False, default="new answer")
    is_correct = models.BooleanField(name='is_correct', verbose_name='Correct?', help_text='Is the answer is correct', default=False)

        