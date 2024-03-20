
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

from todoist_api_python.api import TodoistAPI

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

@api_view(['GET'])
def get_todoist(request):
    # api = TodoistAPI("f33e38b843a30cdd91e534313f8cbec8969a3c22")
    # mydb = mysql.connector.connect(
    # host=os.getenv('HOSTNAME'),
    # user=os.getenv('USER'),
    # password=os.getenv('PASSWORD'), 
    # database="strategicus"
    # )

    # mycursor = mydb.cursor()
    # tables = []
    # mycursor.execute("SHOW TABLES")
    # tables = [i[0] for i in mycursor.fetchall()]

    # if "goals_projects" not in tables:
    #     mycursor.execute("CREATE TABLE goals_projects (pid BIGINT PRIMARY KEY, name VARCHAR(255))")

    # if "goals_sections" not in tables:
    #     mycursor.execute("CREATE TABLE goals_sections (sid BIGINT PRIMARY KEY, name VARCHAR(255), pid BIGINT, FOREIGN KEY (pid) REFERENCES goals_projects(pid))")

    # if "goals_tasks" not in tables:
    #     mycursor.execute("""CREATE TABLE goals_tasks (
    #                     tid BIGINT PRIMARY KEY, 
    #                     content VARCHAR(255), 
    #                     priority INT, 
    #                     due_date DATE, 
    #                     pid BIGINT, 
    #                     sid BIGINT, 
    #                     parent_id BIGINT, 
    #                     FOREIGN KEY (pid) REFERENCES goals_projects(pid), 
    #                     FOREIGN KEY (sid) REFERENCES goals_sections(sid), 
    #                     FOREIGN KEY (parent_id) REFERENCES goals_tasks(tid))
    #                     """)



    # allProjects = []
    # allSections = []
    # allTasks = []

    # class Project:
    #     def __init__(self, id, name):
    #         self.id = id
    #         self.name = name
    #         self.sections = []
    #         self.tasks = []

    #     def __str__(self):
    #         sSections = ''
    #         sTasks = ''
    #         for i in self.sections:
    #             sSections += i.name + ', '
    #         for i in self.tasks:
    #             sTasks += i.content + ', '
    #         return f'Project: {self.name}; Sections: [{sSections}]; Tasks: [{sTasks}]'

    # class Section:
    #     def __init__(self, id, name, project_id):
    #         self.id = id
    #         self.name = name
    #         self.tasks = []
    #         self.project_id = project_id
    #         for i in allProjects:
    #             if i.id == project_id:
    #                 i.sections.append(self)
        
    #     def __str__(self):
    #         sTasks = ''
    #         for i in self.tasks:
    #             sTasks += i.content + ', '
    #         return f'Section: {self.name}; Tasks: [{sTasks}]'

    # class Task:
    #     def __init__(self, id, content, priority, labels, due_date, project_id, section_id, parent_id):
    #         self.id = id
    #         self.content = content
    #         self.priority = priority
    #         self.labels = labels
    #         self.due_date = due_date
    #         self.project_id = project_id
    #         self.section_id = section_id
    #         self.parent_id = parent_id
    #         self.subtasks = []
    #         for i in allProjects:
    #             if i.id == project_id:
    #                 i.tasks.append(self)
    #         for i in allSections:
    #             if i.id == section_id:
    #                 i.tasks.append(self)
    #         for i in allTasks:
    #             if i.id == parent_id:
    #                 i.subtasks.append(i)

    #     def __str__(self):
    #         return f'Task: {self.content}, Priority: {self.priority}, Labels: {self.labels}, Due Date: {self.due_date}'


    # def dlProjects():
    #     try :
    #         projects = api.get_projects()
    #         for project in projects:
    #             allProjects.append(Project(project.id, project.name))
    #         return projects
    #     except Exception as error:
    #         print(error)
    #         return None
        
    # def dlSections():
    #     try:
    #         sections = api.get_sections()
    #         for section in sections:
    #             allSections.append(Section(section.id, section.name, section.project_id))
    #         return sections
    #     except Exception as error:
    #         print(error)
    #         return None

    # def dlTasks():
    #     try:
    #         tasks = api.get_tasks()
    #         for task in tasks:
    #             if task.due is None:
    #                 allTasks.append(Task(task.id, task.content, task.priority, task.labels, task.due, task.project_id, task.section_id, task.parent_id)) #getting task.due.date causes errors and prevents subtasks from being gathered, since some tasks don't have a due date
    #             else:
    #                 allTasks.append(Task(task.id, task.content, task.priority, task.labels, task.due.date, task.project_id, task.section_id, task.parent_id))
    #         return tasks
    #     except Exception as error:
    #         print(error)
    #         return None 
    # dlProjects()
    # dlSections()
    # dlTasks()
    # sql = "INSERT INTO goals_projects (pid, name) VALUES (%s, %s)"
    # val = []
    # pInserted = []
    # mycursor.execute("SELECT pid FROM goals_projects")
    # pInserted = [i[0] for i in mycursor.fetchall()]
    # for i in allProjects:
    #     # print(i)
    #     if int(i.id) not in pInserted:
    #         pInserted.append(i.id)
    #         val.append((int(i.id), i.name))
    # mycursor.executemany(sql, val)
    # mydb.commit()
    # print(mycursor.rowcount, "was inserted.")  

    # sql = "INSERT INTO goals_sections (sid, name, pid) VALUES (%s, %s, %s)"
    # val = []
    # sInserted = []
    # mycursor.execute("SELECT sid FROM goals_sections")
    # sInserted = [i[0] for i in mycursor.fetchall()]
    # for i in allSections:
    #     if int(i.id) not in sInserted:
    #         sInserted.append(i.id)
    #         val.append((int(i.id), i.name, int(i.project_id)))
    # mycursor.executemany(sql, val)
    # mydb.commit()
    # print(mycursor.rowcount, "was inserted.")


    # sql = "INSERT INTO goals_tasks (tid, content, priority, due_date, pid, sid, parent_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = []
    # tInserted = []
    # mycursor.execute("SELECT tid FROM goals_tasks")
    # tInserted = [i[0] for i in mycursor.fetchall()]
    # for i in allTasks:
    #     if int(i.id) not in tInserted:
    #         tInserted.append(i.id)
    #         val.append((int(i.id), i.content, i.priority, i.due_date, i.project_id, i.section_id, i.parent_id))
    # mycursor.executemany(sql, val)
    # mydb.commit()
    # print(mycursor.rowcount, "was inserted.")
    return Response('OK', status=status.HTTP_200_OK)
