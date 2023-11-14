import datetime

from django.db import models
from django.urls import reverse


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
    introduction_text = models.TextField(verbose_name='Introduction text', blank=True)
    activity_status = models.CharField(max_length=10, choices=ACTIVITY_STATUS, default='draft', db_index=True, verbose_name="Survey's Activity Status")
    date_from = models.DateField(default=datetime.date.today(), db_index=True, verbose_name="Date start", help_text="Date, where the survey will be started")
    date_upto = models.DateField(default=datetime.date.today() + datetime.timedelta(days=1), verbose_name="Date finish", help_text="Date, where the survey will be finished")
    is_anonymous = models.BooleanField(verbose_name='Allow Anonymous', default=True)
    must_answers = models.BooleanField(verbose_name='Is all answers mandatory', default=True)

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
        Returns the url to access a particular instance of Questionare.
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


class Response(models.Model):
    # Fields
    user = models.ForeignKey('accounts.SurveyUser', on_delete=models.CASCADE, blank=True, null=True)
    questionare = models.ForeignKey(Questionare, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    survey_session = models.ForeignKey('accounts.SurveySession', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
