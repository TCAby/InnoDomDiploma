from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
import datetime

from .models import Questionare, Question, Answer, Response
from .forms import AddSurveyForm, AddQuestionForm, EditSurveyForm, EditQuestionForm, FillSurveyForm
from accounts.models import SurveySession


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


@login_required
def edit_survey(request, id):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1

    try:
        questionare = Questionare.objects.get(id=id)
    except Questionare.DoesNotExist:
        return HttpResponseNotFound(f"<h2>The survey (id={id}) not found</h2> <a href='/surveys'>Return back</a>")

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
            return HttpResponse(f"<h2>Edit done!</h2> <a href='/surveys'>Return back</a>")
    else:
        form = EditSurveyForm(instance=questionare)
        context = {
            'title': 'Edit survey',
            'form': form,
            'num_visits': num_visits,
        }
        return render(request, 'survey/edit_survey.html', context)


@login_required
def remove_survey(request, id):
    try:
        survey = Questionare.objects.get(id=id)
        # FixMe ToDo Add question-confirmation before delete
        survey.delete()
    except Questionare.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Survey (id={id}) not found</h2>")
    else:
        return HttpResponseRedirect(reverse(surveys))


@login_required
def add_survey(request):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    if request.method == 'POST':
        form = AddSurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(surveys))
        else:
            form.full_clean()
            form_clean_data = form.cleaned_data
            return HttpResponse('We got your data', content_type='text/plain', status=201)
    else:
        form = AddSurveyForm(initial={'title': 'New survey', 'date_from': datetime.datetime.today(), 'date_upto': datetime.datetime.today() + datetime.timedelta(days=1)})
        context = {
            'title': 'Add new survey',
            'form': form,
            'num_visits': num_visits,
        }
        return render(request, 'survey/add_survey.html', context)    


def survey(request, id):
    num_visits = request.session.get('num_visits', 0)
    if request.method == 'GET':
        try:
            questionare = Questionare.objects.get(id=id)
        except Questionare.DoesNotExist:
            return HttpResponseNotFound(f"<h2>The survey (id={id}) not found</h2> Check URL or <a href='/surveys'>Return back</a>")

        if not questionare.is_anonymous:
            pass    # ToDo Authorization form

        questions = Question.objects.filter(questionare=questionare).order_by('?')
        numb_questions = questions.count()
        request.session['survey'] = id
        request.session['questions'] = [q.id for q in questions]
        request.session['questions_details'] = {'current_question': 0, 'questions_number': numb_questions}

        form = FillSurveyForm(initial={'questionare': questionare,})
        context = {
            'title': questionare.title,
            'form': form,
            'num_visits': num_visits,
        }
        return render(request, 'survey/survey.html', context)
    else:
        survey_id = request.session.get('survey')
        question_ids = request.session.get('questions')

        if not survey_id or not question_ids or survey_id != id:
            return HttpResponseBadRequest("Incorrect request: Survey and/or questions not found in session")

        questions_details = request.session.get('questions_details')
        answer_ids = request.POST.getlist('answer[]')
        questionare = Questionare.objects.get(id=id)
        question = Question.objects.get(id=question_ids[questions_details['current_question'] - 1])

        # ToDo
        #if type(request.user) == 'django.utils.functional.SimpleLazyObject':
        current_user = request.user
        if current_user is None:
            c_id = None
        else:
            c_id = current_user.id
        #else:
        #    current_user = None

        session, created = SurveySession.objects.get_or_create(
            session_key=request.session.session_key,
            user_id=c_id
        )
        session.save()

        for answer_id in answer_ids:
            if c_id is None:
                response = Response.objects.create(
                    questionare=questionare,
                    question=question,
                    answer=Answer.objects.get(id=answer_id),
                    survey_session=session
                )
            else:
                response = Response.objects.create(
                    user=current_user,
                    questionare=questionare,
                    question=question,
                    answer=Answer.objects.get(id=answer_id),
                    survey_session=session
                )
            response.save()

        if questionare.must_answers:
            if questions_details['current_question'] >= 0:
                if len(answer_ids) > 0:
                    request.session['questions_details'] = {'current_question': questions_details['current_question'] + 1, 'questions_number': questions_details['questions_number']}
                    questions_details = request.session.get('questions_details')
        else:
            request.session['questions_details'] = {'current_question': questions_details['current_question'] + 1,
                                                    'questions_number': questions_details['questions_number']}
            questions_details = request.session.get('questions_details')

        if questions_details['current_question'] < questions_details['questions_number']:
            question = Question.objects.get(id=question_ids[questions_details['current_question']-1])
            answers = Answer.objects.filter(question=question).order_by('?')
            form = FillSurveyForm(initial={'questionare': questionare, })
            context = {
                'question': question,
                'answers': answers,
                'question_details': questions_details,
                'progress': (int)((questions_details['current_question']+1) / questions_details['questions_number'] * 100),
                'title': questionare.title,
                'form': form,
                'num_visits': num_visits,
            }
        else:  # ToDo Generate result form of the survey
            context = {

            }

        return render(request, 'survey/survey.html', context)

@login_required
def questions(request):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    context = {
        'title': 'List of Questions',
        'questions': Question.objects.all(),
        'num_visits': num_visits
    }
    return render(request, 'survey/questions.html', context)


@login_required
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
            form.full_clean()
            form_clean_data = form.cleaned_data
            return HttpResponse('We got your data', content_type='text/plain', status=201)
    else:
        form = AddQuestionForm(initial={'question': 'New question',})
        context = {
            'title': 'Add new question',
            'form': form,
            'num_visits': num_visits,
        }
        return render(request, 'survey/add_question.html', context)


@login_required
def edit_question(request, id):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return HttpResponseNotFound(
            f"<h2>Question (id={id}) not found</h2> <a href='/surveys/questions/'>Return back</a>")

    if request.method == 'POST':
        form = EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            existed_answers = Answer.objects.filter(question=question)
            answers = [(x, False) for x in request.POST.getlist('answer[]')]
            answers_ids = request.POST.getlist('answer_id[]')
            for ex_ans in existed_answers:
                if str(ex_ans.id) not in answers_ids:
                    ex_ans.delete()
            i = 0
            for is_correct in enumerate(request.POST.getlist('is_correct_answer[]')):
                if is_correct[1] == 'on':
                    if i == 0:
                        answers[i] = (answers[i][0], True)
                    else:
                        answers[i-1] = (answers[i-1][0], True)
                else:
                    i += 1

            i = 0
            for ans in answers:
                if answers_ids[i] == '0':
                    answer = Answer.objects.create(
                        question=question,
                        answer_text=ans[0],
                        is_correct=ans[1],
                    )
                    answer.save()
                else:
                    answer = Answer.objects.get(id=answers_ids[i])
                    answer.answer_text = ans[0]
                    answer.is_correct = ans[1]
                    answer.save(update_fields=['answer_text', 'is_correct'])
                i += 1

            return HttpResponseRedirect(reverse(questions))
        else:
            form.full_clean()
            form_clean_data = form.cleaned_data
            return HttpResponse('We got your data', content_type='text/plain', status=201)
    else:
        form = EditQuestionForm(instance=question)
        answers = Answer.objects.filter(question=question)
        context = {
            'title': 'Edit the question',
            'form': form,
            'answers': answers,
            'num_visits': num_visits,
        }
        return render(request, 'survey/edit_question.html', context)


@login_required
def remove_question(request, id):
    try:
        question = Question.objects.get(id=id)
        # FixMe ToDo Add question-confirmation before delete
        question.delete()
    except Question.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Question (id={id}) not found</h2>")
    else:
        return HttpResponseRedirect(reverse(questions))


@login_required
def answer(request):
    num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits']=num_visits+1
    return HttpResponse('<h1>Answer</h1>')


