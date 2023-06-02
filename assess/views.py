from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.template import loader
from django.db.models import F

# Create your views here.
from django.http import HttpResponse
from .models import Components, Subcomps, Assessments, Questions, Scores, Resources, Outcomes, Engagements
from .classes import assess, engage
import os
import openai



def index(request):
    if request.user.is_authenticated:
        return redirect('/assessment')
    else:
        template = loader.get_template('assess/home.html')
        context = {'title': 'STRATEGICUS',
                }
        return HttpResponse(template.render(context, request))

def ai(request):
    template = loader.get_template('assess/ai.html')
    if request.user.is_authenticated:
        ai_response = 'error'
        if request.method=='POST':
            aiPrompt = request.POST['aiprompt']
            openai.api_key = os.getenv("OPEN_AI_KEY")

            ai_response = openai.Completion.create(
            #   model="text-davinci-001", # Best ,most expensive model
            #   model="text-curie-001",  # Good, reasonably priced model
            #   model="text-babbage-001", # Stupid but cheap
              model="text-ada-001", # Stupid and fast but the cheapest model
              prompt=aiPrompt,
              temperature=0.4,
              max_tokens=64,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )
        else:
            print('no post prompt')
    else:
        ai_response = 'not logged in'
    context = {'title': 'STRATEGIC.ai',
                'airesponse': ai_response,
            }
    return HttpResponse(template.render(context, request))

def assessment(request):
    if request.user.is_authenticated:
        template = loader.get_template('assess/assessment.html')
        if request.GET.get('scid')== None:
            type = 'comp'
            # resp_text = "Hello, world. You're at the polls index.  You are logged in as: "+request.user.username
            component_list = Components.objects.values('comp_id','name','desc','icon')
            # question_list = Questions.objects.values('question','subcomp__name','yes','no','outcome__outcome')
            request.session['ass_id'] = 1    #setting the default assessment value before the assessments logic is built
        else:
            type = 'subcomp'
            scid = request.GET.get('scid')    #  Get the sub component we are working with
            assid = request.session.get('ass_id')    #  Get the assessment id
            component_list = Subcomps.objects.values('subcomp_id','name','desc','icon').filter(comp_id=scid)
    else:
            resp_text = "Hello, world. You're not logged in!"
            return redirect('/accounts/login')
    context = {'title': 'STRATEGICUS',
                # 'quest':question_list,
                'type':type,
                'comp': component_list
                }
    return HttpResponse(template.render(context, request))

# def subcomp(request):
#     template = loader.get_template('assess/subcomp.html')
#     if request.GET.get('scid') == None:
#         print(request.GET)
#         return redirect('/')
#     else:
#         scid = request.GET.get('scid')    #  Get the sub component we are working with
#         assid = request.session.get('ass_id')    #  Get the assessment id

#     if request.user.is_authenticated:
#         subcomponent_list = Subcomps.objects.values('subcomp_id','name','desc','icon').filter(comp_id=scid)
#     else:
#         resp_text = "No Subcomp Id"
#         return redirect('accounts/login')
#     context = {'title': 'STRATEGICUS',
#                 'subcomp':subcomponent_list,
#                 }
#     return HttpResponse(template.render(context, request))    

def question(request):
    if request.GET.get('section') == 'q':
        template = loader.get_template('assess/question.html')
    elif request.GET.get('section') == 'r':
        template = loader.get_template('assess/results.html')
    elif request.GET.get('section') == 'a':
        template = loader.get_template('assess/actions.html')
    elif request.GET.get('section') == 's':
        template = loader.get_template('assess/setup.html')
    else:
        return redirect('/')
    if request.GET.get('scid') == None:
        print(request.GET)
        return redirect('/')
    else:
        scid = request.GET.get('scid')    #  Get the sub component we are working with
        assid = request.session.get('ass_id')    #  Get the assessment id
    
    if request.user.is_authenticated:
        question_list = assess('Test Assessment')  # Need to replace with database data when assessment logic is built
        question_list.id = scid
        question_list.add_questions(Questions.objects\
                                    .values('question_id','section_id','section_id__name','level', 'type','question','subcomp__name','yes','no','outcome__outcome')\
                                    .filter(subcomp_id=scid)\
                                    .order_by('section_id','level','type'))
        question_list.add_scores(Scores.objects.values('question_id','score').filter(ass_id=assid, question_id__in=question_list.quest_ids))
        question_list.add_actions(Scores.objects.annotate(actions=F('question_id__outcome_id__outcome')).values('actions','question_id__outcome_id')\
                                  .filter(question_id__subcomp_id=scid, score=0))
    else:
        resp_text = "No Subcomp Id"
        return redirect('accounts/login')


    context = {'title': 'STRATEGICUS',
                'quest':question_list,
                }
    return HttpResponse(template.render(context, request))   

def engagement(request):
    template = loader.get_template('assess/engagement.html')
    print(request.GET)
    try:
        actionid = request.GET.get('actionid')
    except:
        print("No action id")
        return redirect('/')
    if actionid == None:
        print("No action id")
        return redirect('/')
    action = Outcomes.objects.values('outcome').filter(outcome_id=actionid)
    print('action:', action)
    data = Engagements.objects.values('eng_name','eng_desc','eng_type','eng_cost','eng_level','eng_complexity','eng_duration','eng_duration_units','eng_link','eng_rating', 'resource_id__resource_type').filter(outcome_id__outcome_id=actionid)
    # print(Engagements.objects.values('eng_name','eng_desc','eng_cost','eng_level','eng_complexit','eng_duration','eng_duration_units','eng_link','eng_rating').filter(outcome_id__outcome_id=actionid).query)
    action_list = []
    for item in data:
        action_list.append(engage(item))

    context = {'title': 'STRATEGICUS',
                'action': action,
                'engagement':action_list,
                }
    return HttpResponse(template.render(context, request))

def goals(request):
    apiserver = os.environ['API_SERVER']
    context = {'title': 'STRATEGICUS',
               'apiserver': apiserver,}
    if request.GET.get('stage') == 'd':
        template = loader.get_template('assess/drill_goals.html')
    else:
        template = loader.get_template('assess/goals.html')
    return HttpResponse(template.render(context, request))