from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Question

# Create your views here.
def index(request):
    lastQuestionList = Question.objects.order_by('-pubDate')[:10]
    context = {'lastQuestionList' : lastQuestionList, 
    }
    return render(request, 'polls/index.html', context)
    
def detail(request, questionId):
   
    question = get_object_or_404(Question, pk=questionId)
    return render(request, 'polls/detail.html', {'question' : question})

def results(request, questionId):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % questionId)

def vote(request, questionId):
    return HttpResponse("You're voting on question %s." % questionId)