from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from .models import Components, Assessments, Questions, Scores
from .classes import assess



def index(request):
    if request.user.is_authenticated:
        template = loader.get_template('assess/assessment.html')
        component_list = Components.objects.values('comp_id','name','desc','icon')
        question_list = Questions.objects.values('question','subcomp__name','yes','no','outcome__outcome')
        request.session['ass_id'] = 1    #setting the default assessment value before the assessments logic is built
        context = {'title': 'STRATEGICUS',
                'quest':question_list,
                'comp': component_list
                }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('assess/home.html')
        context = {'title': 'STRATEGICUS',
                }
        return HttpResponse(template.render(context, request))

def assessment(request):
    template = loader.get_template('assess/assessment.html')
    if request.user.is_authenticated:
        resp_text = "Hello, world. You're at the polls index.  You are logged in as: "+request.user.username
        component_list = Components.objects.values('comp_id','name','desc','icon')
        question_list = Questions.objects.values('question','subcomp__name','yes','no','outcome__outcome')
        request.session['ass_id'] = 1    #setting the default assessment value before the assessments logic is built
    else:
        resp_text = "Hello, world. You're not logged in!"
        return redirect('/accounts/login')
    context = {'title': 'STRATEGICUS',
                'quest':question_list,
                'comp': component_list
                }
    return HttpResponse(template.render(context, request))

def subcomp(request):
    template = loader.get_template('assess/subcomp.html')
    if request.GET.get('scid') == None:
        print(request.GET)
        return redirect('/')
    else:
        scid = request.GET.get('scid')    #  Get the sub component we are working with
        assid = request.session.get('ass_id')    #  Get the assessment id

    if request.user.is_authenticated:
        question_list = assess('Test Assessment')  # Need to replace with database data when assessment logic is built
        question_list.add_questions(Questions.objects.values('question_id','question','subcomp__name','yes','no','outcome__outcome').filter(subcomp__comp_id=scid))
        question_list.add_scores(Scores.objects.values('question_id','score').filter(ass_id=assid, question_id__in=question_list.quest_ids))
    else:
        resp_text = "No Subcomp Id"
        return redirect('accounts/login')
    context = {'title': 'STRATEGICUS',
                'quest':question_list,
                }
    return HttpResponse(template.render(context, request))    

def question(request):
    template = loader.get_template('assess/question.html')
    if request.GET.get('scid') == None:
        print(request.GET)
        return redirect('/')
    else:
        scid = request.GET.get('scid')    #  Get the sub component we are working with
        assid = request.session.get('ass_id')    #  Get the assessment id

    if request.user.is_authenticated:
        question_list = assess('Test Assessment')  # Need to replace with database data when assessment logic is built
        question_list.add_questions(Questions.objects.values('question_id','question','subcomp__name','yes','no','outcome__outcome').filter(subcomp__comp_id=scid))
        question_list.add_scores(Scores.objects.values('question_id','score').filter(ass_id=assid, question_id__in=question_list.quest_ids))
    else:
        resp_text = "No Subcomp Id"
        return redirect('accounts/login')
    context = {'title': 'STRATEGICUS',
                'quest':question_list,
                }
    return HttpResponse(template.render(context, request))    
    
def results(request):
    template = loader.get_template('assess/results.html')
    if request.GET.get('scid') == None:
        print(request.GET)
        return redirect('/')
    else:
        scid = request.GET.get('scid')    #  Get the sub component we are working with
        assid = request.session.get('ass_id')    #  Get the assessment id

    if request.user.is_authenticated:
        question_list = assess('Test Assessment')  # Need to replace with database data when assessment logic is built
        question_list.add_questions(Questions.objects.values('question_id','question','subcomp__name','yes','no','outcome__outcome').filter(subcomp__comp_id=scid))
        question_list.add_scores(Scores.objects.values('question_id','score').filter(ass_id=assid, question_id__in=question_list.quest_ids))
    else:
        resp_text = "No Subcomp Id"
        return redirect('accounts/login')
    context = {'title': 'STRATEGICUS',
                'quest':question_list,
                }
    return HttpResponse(template.render(context, request))    
