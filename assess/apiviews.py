
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
from .serializers import QuestionSerializer

@api_view(['GET','POST'])

def question(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented")
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            userid = User.objects.get(pk=serializer.data['usr_id'])
            try:
                # record then answer
                # fetch the next question
                # return the next question
                assess_id = Assessments.objects.get(ass_id=serializer.data['ass_id'])
                quest_id = Questions.objects.get(question_id=serializer.data['q_id'])

                # return Response('Your API is live mofo! You question was:'+quest_id.question, status=status.HTTP_400_BAD_REQUEST)                
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
