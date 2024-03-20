from django.db import models

    
class Goal_Types(models.Model):
    goal_type_id = models.AutoField(primary_key=True)
    goal_abbv = models.CharField(max_length=2, blank=True, null=True)
    goal_name = models.CharField(max_length=45, blank=True, null=True)
    goal_timeframe = models.CharField(max_length=45, blank=True, null=True)
    goal_type_desc = models.CharField(max_length=250, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.goal_name
    
class Goals(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    goal = models.CharField(max_length=500, blank=True, null=True)
    goal_type_id = models.ForeignKey('Goal_Types', on_delete=models.CASCADE, db_column='goal_type_id')
    priority = models.IntegerField(blank=True, null=True)
    roll_up = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='f_rollup')
    break_down = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='f_breakdown')
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

class Project(models.Model):
    pid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sid = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='f_sid')

class Section(models.Model):
    sid = models.IntegerField(primary_key=True)
    section_name = models.CharField(max_length=45, blank=True, null=True)
    pid = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='f_pid')
    tid = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='f_tid')    
    
    
class Task(models.Model):
    tid = models.IntegerField(primary_key=True)
    task_name = models.CharField(max_length=45, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    sid = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='f2_sid')
    pid = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='f2_pid')
    parent_id = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='f2_tid')

