from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.db import transaction
import datetime

from .models import Questionare, Question, Answer
from .forms import AddSurveyForm, AddQuestionForm, EditSurveyForm, EditQuestionForm


def home(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits']=num_visits+1
    context = {
        'title': 'Short introduction',
        'num_visits': num_visits
    }
    return render(request, 'survey/home.html', context)


def surveys(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    context = {
        'title': 'List of Surveys',
        'surveys': Questionare.objects.all(),
        'num_visits': num_visits
    }
    return render(request, 'survey/surveys.html', context)


def edit_survey(request, id):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1

    try:
        questionare = Questionare.objects.get(id=id)
        form = EditSurveyForm(instance=questionare)
        if request.method == "POST":
            form = EditSurveyForm(request.POST, instance=questionare)
            if form.is_valid():
                form.save()
                selected_questions = form.cleaned_data['new_questions']
                for question in selected_questions:
                    question.questionare = questionare
                    question.save()
                selected_questions = form.cleaned_data['exist_questions']
                for question in selected_questions:
                    question.questionare = None
                    question.save()
                return HttpResponseNotFound(f"<h2>Edit done!</h2> <a href='/surveys'>Return back</a>")
        else:
            context = {
                'title': 'Edit survey',
                'form': form,
                'num_visits': num_visits,
            }
            return render(request, 'survey/edit_survey.html', context)
    except Questionare.DoesNotExist:
        return HttpResponseNotFound(f"<h2>The survey (id={id}) not found</h2> <a href='/surveys'>Return back</a>")
    #except:
    #    return HttpResponseNotFound(f"<h2>Anything go wrong for the survey (id={id})!</h2> <a href='/surveys'>Return back</a>")


def remove_survey(request, id):
    try:
        survey = Questionare.objects.get(id=id)
        # FixMe ToDo Add question-confirmation before delete
        survey.delete()
    except Questionare.DoesNotExist:
        return HttpResponseNotFound("<h2>Survey not found</h2>")
    else:
        return HttpResponseRedirect(reverse(surveys))


def add_survey(request):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    if request.method == 'POST':
        form = AddSurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(surveys))
        else:
            print(form.data)
            form.full_clean()
            form_clean_data = form.cleaned_data
            print(form_clean_data)
            return HttpResponse('We got your data', content_type='text/plain', status=201)
    else:
        form = AddSurveyForm(initial={'title': 'New survey', 'date_from': datetime.datetime.today(), 'date_upto': datetime.datetime.today() + datetime.timedelta(days=1)})
        context = {
            'title': 'Add new survey',
            'form': form,
            'num_visits': num_visits,
        }
        return render(request, 'survey/add_survey.html', context)    


def questions(request):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    context = {
        'title': 'List of Questions',
        'questions': Question.objects.all(),
        'num_visits': num_visits
    }
    return render(request, 'survey/questions.html', context)


def add_question(request):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            form_data = form.data
            answers = [(x, False) for x in request.POST.getlist('answer[]')]
            i = 0
            for is_correct in enumerate(request.POST.getlist('is_correct_answer[]')):
                print(i, is_correct, is_correct[1] == 'on')
                if is_correct[1] == 'on':
                    if i == 0:
                        answers[i] = (answers[i][0], True)
                    else:
                        answers[i-1] = (answers[i-1][0], True)
                else:
                    i += 1

            if 'is_allow_multiple_answers' in form_data:
                is_mult = True
            else:
                is_mult = False

            with transaction.atomic():
                qid = transaction.savepoint()
                try:
                    question = Question.objects.create(
                        text=form_data['text'],
                        is_allow_multiple_answers=is_mult,
                    )
                except Exception:
                    print (f"Exception on Question save: ", Exception.__name__)
                    transaction.savepoint_rollback(qid)
                else:
                    question.save()
                    aid = transaction.savepoint()
                    try:
                        for ans in answers:
                            print(ans)
                            answer = Answer.objects.create(
                                question=question,
                                answer_text=ans[0],
                                is_correct=ans[1],
                            )
                            answer.save()
                    except Exception:
                        print(f"Exception on Answer save: ", Exception)
                        transaction.savepoint_rollback(qid)
                finally:
                    return HttpResponseRedirect(reverse(questions))
        else:
            print(form.data)
            form.full_clean()
            form_clean_data = form.cleaned_data
            print(form_clean_data)
            return HttpResponse('We got your data', content_type='text/plain', status=201)
    else:
        form = AddQuestionForm(initial={'question': 'New question',})
        context = {
            'title': 'Add new question',
            'form': form,
            'num_visits': num_visits,
        }
        return render(request, 'survey/add_question.html', context)


def edit_question(request, id):
    pass


def remove_question(request, id):
    pass


def answer(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits']=num_visits+1
    return HttpResponse('<h1>Answer</h1>')


