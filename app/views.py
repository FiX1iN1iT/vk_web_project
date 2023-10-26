from django.shortcuts import render


# Create your views here.
def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'Long lorem ipsum {i}'
        } for i in range(20)
    ]

    return render(request, 'index.html', {'questions': questions})


def question(request):
    return render(request, 'question.html')
