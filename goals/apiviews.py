
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime

import json
from django.contrib.auth.models import User 
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .models import Goals, Goal_Types
from .serializers import GoalSerializer, DrilldownSerializer, GoalEditSerializer

import os

### STRATEGICUS GOALS API PROCESSOR ####

######### GOAL PRIORITY API SET    
@api_view(['GET','POST'])
def goals_api(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        print(request.data)
        serializer = GoalSerializer(data=request.data)
        print('starting')
        if serializer.is_valid():
            values = json.loads(serializer.data['goals'][0])
            times = json.loads(serializer.data['goalTimes'][0])
            print('whole values: ', values, 'whole times: ', times)
            Goals.objects.filter(user=request.user).delete()
            for index, g in enumerate(values['data']):
                if g != '':
                    print('goal: ',g)
                    print('timing: ',times['data'][index])
                    print('user: ',serializer.data['userId'])
                    print('priority: ',index)
                    Goals.objects.create(user=request.user, goal=g, duration=times['data'][index], priority=index, create_date=datetime.date.today(), update_date=datetime.date.today())
            return Response('OK', status=status.HTTP_200_OK)
        else:
            print('did not make it')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
### GOAL  DRILL DOWN API SET
@api_view(['GET','POST'])
def goal_drilldown(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = DrilldownSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data['action'], serializer.data['currGoal'], serializer.data['drillGoal'])
            drillgoal = get_object_or_404(Goals, pk=serializer.data['drillGoal'])
            currgoal = get_object_or_404(Goals, pk=serializer.data['currGoal'])
            if serializer.data['action'] == 'add':
                print(drillgoal.goal)
                if serializer.data['type'] == 'low':
                    drillgoal.roll_up = currgoal
                    drillgoal.save()
                elif serializer.data['type'] == 'high':
                    print('high')
                    currgoal.roll_up = drillgoal
                    currgoal.save()
                else:
                    return Response('Invalid type', status=status.HTTP_400_BAD_REQUEST)

                return Response(currgoal.goal + ' hass been linked to ' + drillgoal.goal, status=status.HTTP_200_OK)
            elif serializer.data['action'] == 'remove':
                if serializer.data['type'] == 'low':
                    drillgoal.roll_up = None
                    drillgoal.save()
                elif serializer.data['type'] == 'high':
                    currgoal.roll_up = None
                    currgoal.save()
                return Response(drillgoal.goal + ' has been removed from goal ' + currgoal.goal, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
### GOAL:  ADD / EDIT GOALS
@api_view(['POST'])
def goaledit(request):
    if request.method == 'POST':
        print(request.data)
        serializer = GoalEditSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            if serializer.data['action'] == 'add':
                print('adding', serializer.data['editGoalName'])
                try:
                    goal_rollup_obj = Goals.objects.get(pk=serializer.data['editGoalRollUp'])
                except ObjectDoesNotExist:
                    # Handle the "not found" situation here
                    goal_rollup_obj = None
                goal_type_obj = get_object_or_404(Goal_Types, pk=serializer.data['editGoalType'])
                # goal_rollup_obj = get_object_or_404(Goals, pk=serializer.data['editGoalRollUp'])
                goal_user_obj = get_object_or_404(User, pk=serializer.data['userId'])
                new_goal = Goals(goal=serializer.data['editGoalName'], priority=serializer.data['editGoalPriority'], goal_type_id=goal_type_obj, update_date=datetime.date.today(), roll_up=goal_rollup_obj, user=goal_user_obj)
                new_goal.save()
            elif serializer.data['action'] == 'edit':
                print('editing', serializer.data['editGoalName'], serializer.data['goalId'])
                goal_id = serializer.data['goalId']
                goal = serializer.data['editGoalName']
                goal_obj = get_object_or_404(Goals, pk=goal_id)
                goal_type_obj = get_object_or_404(Goal_Types, pk=serializer.data['editGoalType'])
                goal_rollup_obj = get_object_or_404(Goals, pk=serializer.data['editGoalRollUp'])
                goal_obj.goal = goal
                goal_obj.priority = serializer.data['editGoalPriority']
                goal_obj.goal_type_id = goal_type_obj
                goal_obj.update_date = datetime.date.today()
                goal_obj.roll_up = goal_rollup_obj
                goal_obj.save()
            elif serializer.data['action'] == 'delete':
                print('deleting', serializer.data['editGoalName'], serializer.data['goalId'])
                goal_id = serializer.data['goalId']
                goal_obj = get_object_or_404(Goals, pk=goal_id)
                goal_obj.delete()  # Delete the goal object from the database

            else:
                return Response('Invalid action', status=status.HTTP_400_BAD_REQUEST)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data['editGoalName'] + ' has been ' + serializer.data['action'] +'ed. TEST', status=status.HTTP_200_OK)


