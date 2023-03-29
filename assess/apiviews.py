
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
from .models import Components, Assessments, Scores, Questions
from .serializers import QuestionSerializer, ChatSerializer, ActionSerializer

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
            try:
                # record the answer
                # fetch the next question
                # return the next question
                assess_id = Assessments.objects.get(ass_id=serializer.data['ass_id'])
                quest_id = Questions.objects.get(question_id=serializer.data['q_id'])
            except:
                return Response('Request is invalid', status=status.HTTP_400_BAD_REQUEST)                
            new_score = serializer.data['answer']
            if new_score == 1:
                next_quest = quest_id.yes.question_id
                print('yes answer is: '+str(next_quest))
                queryset = Questions.objects.filter(question_id=next_quest)\
                    .annotate(yquest=F('yes_id__question'), nquest=F('no_id__question'), yid=F('yes_id__question_id'), nid=F('no_id__question_id'))\
                    .values('question_id','question','yquest','nquest','yid','nid')
            else:
                next_quest = quest_id.no.question_id
                print('no answer is: '+str(next_quest))
                queryset = Questions.objects.filter(question_id=next_quest)\
                    .annotate(yquest=F('yes_id__question'), nquest=F('no_id__question'), yid=F('yes_id__question_id'), nid=F('no_id__question_id'))\
                    .values('question_id','question','yquest','nquest','yid','nid')
            quest_data = json.dumps(list(queryset), cls=DjangoJSONEncoder)
            
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
def ai(request):
    ai_response = 'Unknown error'
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
                aiPrompt = serializer.data['prompt_1'] + serializer.data['prompt_2']
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No valid action requested", status=status.HTTP_400_BAD_REQUEST)
         
        openai.api_key = os.getenv("OPEN_AI_KEY")
        ai_response = openai.Completion.create(
        #   model="text-davinci-001", # Best ,most expensive model
        #   model="text-curie-001",  # Good, reasonably priced model
        #   model="text-babbage-001", # Stupid but cheap
            model="text-ada-001", # Stupid and fast but the cheapest model
            prompt=aiPrompt,
            temperature=0.6,
            max_tokens=1000,
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

