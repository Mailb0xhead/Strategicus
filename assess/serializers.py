from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    ass_id = serializers.IntegerField()
    q_id = serializers.IntegerField()
    next_id = serializers.IntegerField()
    usr_id = serializers.IntegerField()
    answer = serializers.IntegerField()

