from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from .models import Choice, Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))

def detail(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk= question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/details.html', {'question': question})


def results(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk= question_id)
    return render(request= request, template_name= 'polls/results.html', context= {'question' : question})


def vote(request: HttpRequest, question_id):
    question : Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk= request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request= request, 
            template_name= 'polls/details.html',
            context={
                'question': question, 
                'error_message': "You didn't select a choice",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    
    return HttpResponseRedirect(redirect_to= reverse('polls:results', args= (question.id,)))