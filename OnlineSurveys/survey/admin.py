from django.contrib import admin
from .models import Questionare, Question, Answer, Response

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


