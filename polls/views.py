from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .models import Choice, Question
from django.urls import reverse
from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latestQuestionList'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pubDate')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, questionId):
    question = get_object_or_404(Question, pk=questionId)
    try:
        selectedChoice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selectedChoice.votes += 1
        selectedChoice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



