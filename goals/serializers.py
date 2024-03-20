from rest_framework import serializers


class GoalSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    goals = serializers.ListField(child=serializers.CharField())
    goalTimes = serializers.ListField(child=serializers.CharField())

class DrilldownSerializer(serializers.Serializer):
    drillGoal = serializers.IntegerField()
    currGoal = serializers.IntegerField()
    type = serializers.CharField()
    userId = serializers.IntegerField()
    action = serializers.CharField()

class GoalEditSerializer(serializers.Serializer):
    editGoalName = serializers.CharField(max_length=500)
    editGoalPriority = serializers.IntegerField(default=99)
    editGoalType = serializers.IntegerField()
    editGoalRollUp = serializers.IntegerField(default=None)
    goalId = serializers.IntegerField(default=None)
    userId = serializers.IntegerField()
    action = serializers.CharField(max_length=50, default="none")


    