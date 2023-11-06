from django.contrib import admin
from django.urls import path
from .models import Questionare, Question, Answer, Response
from .views import home

@admin.register(Questionare)
class QuestionareAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


#@admin.register(Answer)
#class AnswerAdmin(admin.ModelAdmin):
#    pass


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    pass


