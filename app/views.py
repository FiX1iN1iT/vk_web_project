from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

from app.models import Question, Answer, Profile, Tag, Vote

QUESTION = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(40)
]

ANSWER = [
    {
        'id': i,
        'title': f'Answer {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(40)
]

TAG = [
    {
        'id': i,
        'name': f'Tag {i}',
    } for i in range(10)
]


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
    context = {
        'page_obj': paginate(QUESTION, request),
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def ask(request):
    return render(request, 'ask.html')


def signup(request):
    return render(request, 'signup.html')


def hot(request):
    context = {
        'page_obj': paginate(QUESTION, request),
    }
    return render(request, 'hot.html', context)


def tag(request, tag_name):
    questions = Question.objects.tagged(tag_name)
    context = {
        'tag': tag_name,
        'page_obj': paginate(questions, request),
    }
    return render(request, 'tag.html', context)


def question(request, question_id):
    if question_id >= len(QUESTION):
        raise Http404("Question does not exist")
    context = {
        'question': QUESTION[question_id],
        'page_obj': paginate(ANSWER, request),
    }
    return render(request, 'question.html', context)
