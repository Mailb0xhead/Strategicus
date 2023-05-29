from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    ass_id = serializers.IntegerField()
    q_id = serializers.IntegerField()
    next_id = serializers.IntegerField()
    usr_id = serializers.IntegerField()
    answer = serializers.IntegerField()

class ChatSerializer(serializers.Serializer):
    chat_prompt = serializers.CharField(max_length=500)
    chat_history = serializers.CharField(max_length=2000)
    action = serializers.CharField(max_length=50)

class GoalSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    goals = serializers.ListField(child=serializers.CharField())
    goalTimes = serializers.ListField(child=serializers.CharField())


class ActionSerializer(serializers.Serializer):
    prompt_1 = serializers.CharField(max_length=500)
    prompt_2 = serializers.CharField(max_length=500)
    type= serializers.CharField(max_length=50)

    