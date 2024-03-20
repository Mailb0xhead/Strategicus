from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.template import loader
from django.db.models import F

# Create your views here.
from django.http import HttpResponse
from .models import Components, Subcomps, Assessments, Questions, Scores, Resources, Outcomes, Engagements
from .classes import assess, engage, ll_goal, goal
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
    
def profile(request):
    template = loader.get_template('assess/profile.html')
    context = {}
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
        test = (Scores.objects.annotate(actions=F('question_id__outcome_id__outcome'),
                                                          priority=F('question_id__outcome_id__priority'),
                                                          benefit=F('question_id__outcome_id__benefit'))\
                                  .values('actions','priority','benefit','question_id__outcome_id')
                                  .filter(question_id__subcomp_id=scid, score=0).distinct())
        print(test.query)
        question_list.add_actions(Scores.objects.annotate(actions=F('question_id__outcome_id__outcome'),
                                                          priority=F('question_id__outcome_id__priority'),
                                                          benefit=F('question_id__outcome_id__benefit'))\
                                  .values('actions','priority','benefit','question_id__outcome_id')
                                  .filter(question_id__subcomp_id=scid, score=0).order_by('priority').distinct())
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
    goals = Goals.objects.values('goal_id','goal','goal_type_id','goal_type_id__goal_abbv','goal_type_id__goal_name','priority','roll_up_id', 'roll_up_id__goal').filter(user=request.user).order_by('priority')
    goal_types = Goal_Types.objects.values('goal_type_id', 'goal_abbv', 'goal_name','goal_timeframe','goal_type_desc')
    # print(goals.query)
    # print(len(goals))
    
    if request.GET.get('stage') == 'd' and len(goals) > 0:
        template = loader.get_template('assess/drill_goals.html')
        # goals = Goals.objects.values('goal_id','goal','duration','priority','roll_up_id').filter(user=request.user)
        thisGoal = goal(goals.filter(goal_type_id__goal_abbv='LL'))
        for ll in thisGoal.ll_goals:
            if ll.id == -1:
                ll.add_lt_goal(goals.filter(goal_type_id__goal_abbv='LT'))
            else:    
                ll.add_lt_goal(goals.filter(goal_type_id__goal_abbv='LT', roll_up_id=ll.id))
            for lt in ll.lt_goals:
                if lt.id == -1:
                    lt.add_mt_goal(goals.filter(goal_type_id__goal_abbv='MT'))
                else:
                    lt.add_mt_goal(goals.filter(roll_up_id=lt.id, goal_type_id__goal_abbv='MT'))
                for mt in lt.mt_goals:
                    if mt.id == -1:
                        mt.add_st_goal(goals.filter(goal_type_id__goal_abbv='ST'))    
                    else:
                        mt.add_st_goal(goals.filter(roll_up_id=mt.id, goal_type_id__goal_abbv='ST'))
                    for st in mt.st_goals:  
                        if st.id == -1:
                            st.add_tk_goal(goals.filter(goal_type_id__goal_abbv='TK'))
                        else:
                            st.add_task(goals.filter(roll_up_id=st.id, goal_type_id__goal_abbv='TK'))
        context['goals']=thisGoal
    elif request.GET.get('stage') == 'a' and len(goals) > 0:
        # print(goals)
        if request.GET.get('goal_id') == None:          # Set the default goal to the first goal priority in the list
            curr_goal = goals.first()
        else:
            curr_goal = goals.filter(goal_id=request.GET.get('goal_id'))[0]
        h_goal = curr_goal['roll_up_id']
        lower_goal = goals.filter(roll_up_id=curr_goal['goal_id'])
        higher_duration, lower_duration  = calc_duration(curr_goal['goal_type_id__goal_abbv'])
        if lower_goal:
            other_l_goals = goals.filter(goal_type_id__goal_abbv=lower_duration, roll_up_id=None).exclude(roll_up_id = curr_goal['goal_id'])
        else:
            other_l_goals = goals.filter(goal_type_id__goal_abbv=lower_duration, roll_up_id=None)
        print('other l_goals',other_l_goals, lower_goal)
        if not other_l_goals.exists() and not lower_goal.exists():
            lower_goal = 'None'
            
        # print(other_l_goals, lower_goal)
        if h_goal == None:
            print('no higher goal')
            higher_goal = 'None'
        else:
            higher_goal = goals.filter(goal_id=h_goal)[0]
        other_h_goals = goals.filter(goal_type_id__goal_abbv=higher_duration, roll_up_id=None).exclude(goal_id = h_goal)
        # print(other_h_goals)
        # higher_goal = goals.get(goal_id=h_goal)
        # print('curr:',curr_goal,'low:', lower_goal,'high:', higher_goal)
        context['curr_goal']=curr_goal
        context['other_goals']=other_l_goals
        context['higher_goal'] = higher_goal
        context['other_h_goals'] = other_h_goals
        context['lower_goal'] = lower_goal
        context['goal_types']=goal_types
        context['goals']=goals
        template = loader.get_template('assess/goals_align.html')
    elif request.GET.get('stage') == 'p':
        context['goals']=goals
        template = loader.get_template('assess/goalsetter.html')
    elif request.GET.get('stage') == 'l':
        context['goals']=goals
        context['goal_types']=goal_types
        template = loader.get_template('assess/goals_list.html')
    else:
        context['goals']=goals
        template = loader.get_template('assess/goals.html')
    return HttpResponse(template.render(context, request))


'''
THIS IS A COMMENT
'''

