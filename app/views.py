from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

from app.models import Question
from django.db.models import Sum


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        raise Http404("Page not found")
    return page_obj


# Create your views here.
def index(request):
    # questions = Question.objects.all()
    questions = Question.objects.annotate(totaly_votes=Sum('vote__value'))

    context = {
        'page_obj': paginate(questions, request),
        # 'question_votes': {question.id: Question.objects.count_total_votes(question.id) for question in questions},
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    # questions = Question.objects.all()
    questions = Question.objects.get_hot_questions().annotate(totaly_votes=Sum('vote__value'))

    context = {
        'page_obj': paginate(questions, request),
    }
    return render(request, 'hot.html', context)


def top(request):
    questions = Question.objects.get_top_questions().annotate(totaly_votes=Sum('vote__value'))

    context = {
        'page_obj': paginate(questions, request, 10),
    }
    return render(request, 'top.html', context)


def tag(request, tag_name):
    questions = Question.objects.tagged(tag_name).annotate(totaly_votes=Sum('vote__value'))
    context = {
        'tag': tag_name,
        'page_obj': paginate(questions, request),
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    if question_id > len(Question.objects.all()):
        raise Http404("Question does not exist")
    my_question = Question.objects.filter(pk=question_id).annotate(totaly_votes=Sum('vote__value')).first()
    context = {
        'question': my_question,
        'page_obj': paginate(my_question.answers.all(), request),
    }
    return render(request, 'question.html', context)
