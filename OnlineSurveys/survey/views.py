""" Management of the heart of the project"""
import datetime
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import Questionare, Question, Answer, Response
from .forms import AddSurveyForm, AddQuestionForm, EditSurveyForm, EditQuestionForm, FillSurveyForm
from accounts.models import SurveySession, SurveyUser


def home(request) -> HttpResponse:
    """
    Outputs static introduction of the project
    :param request:
    :return:
    """
    context = {
        'title': 'Short introduction',
    }
    return render(request, 'survey/home.html', context)


def surveys(request) -> HttpResponse:
    """
    List of surveys, depends on user rights
    :param request:
    :return:
    """
    context = {
        'title': 'List of Surveys',
        'current_date': datetime.date.today(),
        'surveys': Questionare.objects.all() if request.user.is_staff else Questionare.objects.active(),
    }
    return render(request, 'survey/surveys.html', context)


@login_required
def edit_survey(request, id:int) -> HttpResponse:
    """

    :param request:
    :param id:
    :return:
    """
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
            return HttpResponseRedirect(reverse(surveys))
    else:
        form = EditSurveyForm(instance=questionare)
        context = {
            'title': 'Edit survey',
            'form': form,
        }
        return render(request, 'survey/edit_survey.html', context)


@login_required
def remove_survey(request, id:int) -> HttpResponse:
    """

    :param request:
    :param id:
    :return:
    """
    try:
        survey = Questionare.objects.get(id=id)
        # FixMe ToDo Add question-confirmation before delete
        survey.delete()
    except Questionare.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Survey (id={id}) not found</h2>")
    else:
        return HttpResponseRedirect(reverse(surveys))


@login_required
def add_survey(request) -> HttpResponse:
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AddSurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(surveys))
        return HttpResponse('We got your data', content_type='text/plain', status=201)

    form = AddSurveyForm(initial={'title': 'New survey', 'date_from': datetime.datetime.today(), 'date_upto': datetime.datetime.today() + datetime.timedelta(days=1)})
    context = {
        'title': 'Add new survey',
        'form': form,
    }
    return render(request, 'survey/add_survey.html', context)


def survey(request, id:int) -> HttpResponse:
    """

    :param request:
    :param id:
    :return:
    """
    if request.method == 'GET':
        try:
            questionare = Questionare.objects.get(id=id)
        except Questionare.DoesNotExist:
            return HttpResponseNotFound(
                f"<h2>The survey (id={id}) not found</h2> Check URL or <a href='/surveys'>Return back</a>")

        if not questionare.is_anonymous:
            if request.user.id is None:
                return redirect_to_login(request.get_full_path(), login_url='/accounts/login/')

        if not questionare.is_status_daterange_actual:
            return HttpResponseBadRequest(
                f"<h2>The survey (id={id}) inactive or the cut-off date is less than today's date </h2> " +
                f"Check URL or <a href='/surveys'>Return back</a>"
            )

        tmp_questions = Question.objects.filter(questionare=questionare).order_by('?')
        request.session['survey'] = id
        request.session['questions'] = [q.id for q in tmp_questions]
        request.session['questions_details'] = {'current_question': 0, 'questions_number': tmp_questions.count()}

        form = FillSurveyForm(initial={'questionare': questionare,})
        context = {
            'title': questionare.title,
            'form': form,
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

        current_user = request.user
        if current_user is None or current_user.id is None:
            current_user_id = None
        else:
            current_user_id = current_user.id

        session, created = SurveySession.objects.get_or_create(
            session_key=request.session.session_key,
            user_id=current_user_id
        )
        session.save()

        for answer_id in answer_ids:
            response = Response.objects.create(
                questionare=questionare,
                question=question,
                answer=Answer.objects.get(id=answer_id),
                survey_session=session
            )
            if current_user_id is not None:
                response.user=current_user
                response.save(update_fields=["user"])

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
            }
            return render(request, 'survey/survey.html', context)
        else:
            def calculate_result(survey_id: int, session_key: str) -> dict:
                """
                Creates a dictionary from the questions of the survey and correct answers received,
                like {'question': question.text, 'answer': answers}

                :param survey_id:
                :param session_key:
                :return: dictionary
                """
                survey_session = SurveySession.objects.get(session_key=session_key)
                survey_questions = Question.objects.filter(questionare_id=survey_id)
                user_answers = {}
                question_correct_answers = {}
                user_correct_answers_draft = {}
                for survey_question in survey_questions:
                    tmp = Response.objects.filter(survey_session_id=survey_session.id, questionare_id=survey_id,
                                                  question_id=survey_question.id)
                    user_answers[survey_question.id] = [value[0] for value in tmp.values_list('answer_id')]
                    question_correct_answers[survey_question.id] = [value[0] for value in Answer.objects.filter(
                        question_id=survey_question.id, is_correct=1).values_list('id')]

                    if survey_question.is_allow_multiple_answers:
                        if user_answers[survey_question.id] == question_correct_answers[survey_question.id]:
                            user_correct_answers_draft[survey_question.id] = user_answers[survey_question.id]
                    else:
                        user_answer = user_answers[survey_question.id][0]
                        if user_answer in question_correct_answers[survey_question.id]:
                            user_correct_answers_draft[survey_question.id] = user_answers[survey_question.id]

                user_correct_answers = {}
                for user_correct_answer_draft in user_correct_answers_draft:
                    question = Question.objects.get(id=user_correct_answer_draft)
                    answers = list()
                    for answer_id in user_correct_answers_draft.get(user_correct_answer_draft):
                        answer = Answer.objects.get(id=answer_id)
                        answers.append(answer.answer_text)
                    user_correct_answers[user_correct_answer_draft] = {'question': question.text, 'answer': answers}

                return user_correct_answers

            correct_answers = calculate_result(survey_id, request.session.session_key)
            context = {
                'title': questionare.title,
                'questions_number': questions_details['questions_number'],
                'number_correct_answers': len(correct_answers),
                'correct_answers': correct_answers,
            }
            return render(request, 'survey/survey_user_result.html', context)


@login_required
def questions(request):
    context = {
        'title': 'List of Questions',
        'questions': Question.objects.all(),
    }
    return render(request, 'survey/questions.html', context)


@login_required
def add_question(request):
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
            return HttpResponse('We got your data', content_type='text/plain', status=201)
    else:
        form = AddQuestionForm(initial={'question': 'New question',})
        context = {
            'title': 'Add new question',
            'form': form,
        }
        return render(request, 'survey/add_question.html', context)


@login_required
def edit_question(request, id:int):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return HttpResponseNotFound(
            f"<h2>Question (id={id}) not found</h2> <a href='/surveys/questions/'>Return back</a>")

    def verify_existed_answers_list(existed_answers:dict, new_answers_ids:list):
        """Compares the list of saved responses to the list of response IDs in the new list.
        If this answer is no longer in the new list, it is deleted.

        Keyword arguments:
            existed_answers:QuerySet    - items of the Answer Model
            new_answers_ids:list        - list of ids from the form (elements with name="answer_id[]")

        """
        for answer in existed_answers:
            if str(answer.id) not in new_answers_ids:
                answer.delete()

    def mark_correct_answers(answers:dict, list_correct_answers:list) -> dict:
        """Combines a list of answers and a list of marks for correct answers.

        Keyword arguments:
            answers:dict                - result of request.POST.getlist
            list_correct_answers:list   - result of request.POST.getlist
        """
        i = 0
        for is_correct in enumerate(list_correct_answers):
            if is_correct[1] == 'on':
                if i == 0:
                    answers[i] = (answers[i][0], True)
                else:
                    answers[i - 1] = (answers[i - 1][0], True)
            else:
                i += 1

        return answers

    if request.method == 'POST':
        form = EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            existed_answers = Answer.objects.filter(question=question)
            answers_ids = request.POST.getlist('answer_id[]')
            verify_existed_answers_list(existed_answers, answers_ids)

            answers = [(x, False) for x in request.POST.getlist('answer[]')]
            answers = mark_correct_answers(answers,request.POST.getlist('is_correct_answer[]'))

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
        }
        return render(request, 'survey/edit_question.html', context)


@login_required
def remove_question(request, id:int) -> HttpResponse:
    try:
        question = Question.objects.get(id=id)
        # FixMe ToDo Add question-confirmation before delete
        question.delete()
    except Question.DoesNotExist:
        return HttpResponseNotFound(f"<h2>Question (id={id}) not found</h2>")
    else:
        return HttpResponseRedirect(reverse(questions))

