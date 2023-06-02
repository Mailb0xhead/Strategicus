
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime

import json
from django.contrib.auth.models import User 
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from .models import Components, Assessments, Scores, Questions, Sections, Goals
from .serializers import QuestionSerializer, ChatSerializer, ActionSerializer, GoalSerializer

import os
import openai


@api_view(['GET','POST'])

def question(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            userid = User.objects.get(pk=serializer.data['usr_id'])
            print(userid,serializer.data['ass_id'],serializer.data['q_id'],serializer.data['answer'])
            assess_id = Assessments.objects.get(ass_id=serializer.data['ass_id'])
            quest_id = Questions.objects.get(question_id=serializer.data['q_id'])
            try:
                # record the answer
                # fetch the next question
                # return the next question
                assess_id = Assessments.objects.get(ass_id=serializer.data['ass_id'])
                quest_id = Questions.objects.get(question_id=serializer.data['q_id'])
            except:
                return Response('Request is invalid', status=status.HTTP_400_BAD_REQUEST)    
            print('The next question is:', quest_id.next.question_id)            
            if quest_id.next.question_id == 999999:
                next_up = quest_id.section.next_section.first_question
                print('next section',next_up)
                # this_section = Sections.objects.filter(section_id = quest_id.section_id).values('next_section')
                # first_quest = Sections.objects.filter(section_id=this_section).values('first_question')
                quest_id = Questions.objects.get(question_id=next_up)
                next_quest = quest_id.question_id
            else:    
                next_quest = quest_id.next.question_id

            queryset = Questions.objects.filter(question_id=next_quest)\
                .annotate(yquest=F('yes_id__question'), nquest=F('no_id__question'), yid=F('yes_id__question_id'), nid=F('no_id__question_id'))\
                .values('question_id','question','yquest','nquest','yid','nid','type','level','section__name')
            quest_data = json.dumps(list(queryset), cls=DjangoJSONEncoder)
            
            new_score = serializer.data['answer']

            try:
                curr_score = Scores.objects.get(ass_id=assess_id, question_id=quest_id, user_id=userid)
                curr_score.score = new_score
                # print(quest_id, new_score)
                curr_score.save()
                return Response(quest_data, status=status.HTTP_201_CREATED)
            except:
                 curr_score = Scores.objects.create(ass_id=assess_id, question_id=quest_id, score=new_score, create_date=datetime.date.today(), user_id=userid)
                 curr_score.save()
                 return Response(quest_data, status=status.HTTP_201_CREATED)

            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
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
                    Goals.objects.create(user=request.user, goal=g, duration=times['data'][index], create_date=datetime.date.today(), update_date=datetime.date.today())



                
            return Response('OK', status=status.HTTP_200_OK)
        else:
            print('did not make it')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    



@api_view(['GET','POST'])
def ai(request):
    ai_response = 'Unknown error'
    Client = 'This is for an IT leader at a mid size business with revenue between $50m and $1B.  '
    Tone = 'Keep a professional tone like you are a consultant.  '
    Instructions = 'Please give a few options and preface it with a short summary paragraph that paraphrases the question and talks about the importance of doing this work.  Do not reiterate their business details.  Do not list the answers in numerical format. Include hyperlinks to resources if applicable.'
    if request.method == 'GET':
        return HttpResponse("This type of request is not valid")
    if request.method=='POST':
        if request.data['type'] == 'chat':
            serializer = ChatSerializer(data=request.data)
            if serializer.is_valid():
                aiPrompt = serializer.data['chat_prompt']
                aiHistory = serializer.data['chat_history']
        elif request.data['type'] == 'action':
            serializer = ActionSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data['prompt_1'],serializer.data['prompt_2'])
                aiPrompt = serializer.data['prompt_1'] + serializer.data['prompt_2'] + Client + Tone + Instructions
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No valid action requested", status=status.HTTP_400_BAD_REQUEST)
         
        openai.api_key = os.getenv("OPEN_AI_KEY")
        ai_response = openai.Completion.create(
           model="text-davinci-001", # Best ,most expensive model
        #   model="text-curie-001",  # Good, reasonably priced model
        #   model="text-babbage-001", # Stupid but cheap
            # model="text-ada-001", # Stupid and fast but the cheapest model
            prompt=aiPrompt,
            temperature=0.7,
            max_tokens=450,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print('AI Response: ',ai_response)
    else:
        ai_response = 'unknown post error'
    return Response(ai_response, status=status.HTTP_200_OK)




@api_view(['GET','POST'])
def dalle(request):
    ai_response = 'Unknown error'
    if request.method == 'GET':
        return HttpResponse("This type of request is not valid")
    if request.method=='POST':
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            aiPrompt = serializer.data['chat_prompt']
            print('aiPrompt:',aiPrompt)
            aiHistory = serializer.data['chat_history']
            openai.api_key = os.getenv("OPEN_AI_KEY")

            ai_response = openai.Image.create(
            #   model="text-davinci-001", # Best ,most expensive model
            #   model="text-curie-001",  # Good, reasonably priced model
            #   model="text-babbage-001", # Stupid but cheap
                # model="text-ada-001", # Stupid and fast but the cheapest model
                prompt=aiPrompt,
                size="1024x1024",
                n=1,
                # temperature=0.6,
                # max_tokens=1000,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0
            )

            # The response is in the url:  image_url = response['data'][0]['url']
            
            print('AI Response: ',ai_response)
        else:
            print('no post prompt')
    else:
        ai_response = 'unknown post error'
    return Response(ai_response, status=status.HTTP_200_OK)

