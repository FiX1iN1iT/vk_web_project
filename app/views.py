from django.shortcuts import render
from django.core.paginator import Paginator

QUESTION = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(20)
]


def paginate(objects, page, per_page=15):
    paginator = Paginator(objects, per_page)

    return paginator.page(page)


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html', {'questions': paginate(QUESTION, page)})


def question(request, question_id):
    item = QUESTION[question_id]
    return render(request, 'question.html', {'question': item})
