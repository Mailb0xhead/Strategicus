from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from .models import Goals, Goal_Types
from .classes import goal
import os


def index(request):
    if request.user.is_authenticated:
        return redirect('/assessment')
    else:
        template = loader.get_template('assess/home.html')
        context = {'title': 'STRATEGICUS',
                }
        return HttpResponse(template.render(context, request))
    

def goals(request):
    print('in goals')
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
        template = loader.get_template('goals/goals_align.html')
    elif request.GET.get('stage') == 'p':
        context['goals']=goals
        template = loader.get_template('goals/goalsetter.html')
    elif request.GET.get('stage') == 'l':
        context['goals']=goals
        context['goal_types']=goal_types
        template = loader.get_template('goals/goals_list.html')
    else:
        context['goals']=goals
        template = loader.get_template('goals/goals.html')
    return HttpResponse(template.render(context, request))


'''
THIS IS A COMMENT
'''

