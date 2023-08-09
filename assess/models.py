from django.db import models

# Create your models here.
class Assessments(models.Model):
    ass_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Components(models.Model):
    comp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Engagements(models.Model):
    eng_id = models.AutoField(primary_key=True)
    resource_id = models.ForeignKey('Resources', db_column='resource_id', on_delete=models.CASCADE)
    outcome_id = models.ForeignKey('Outcomes', db_column='outcome_id', on_delete=models.CASCADE)
    eng_name = models.CharField(max_length=45, blank=True, null=True)
    eng_desc = models.CharField(max_length=500, blank=True, null=True)
    eng_type = models.CharField(max_length=20, blank=True, null=True)
    eng_cost = models.IntegerField(blank=True, null=True)
    eng_level = models.CharField(max_length=45, blank=True, null=True)
    eng_complexity = models.CharField(max_length=45, blank=True, null=True)
    eng_duration = models.IntegerField(blank=True, null=True)
    eng_duration_units = models.CharField(max_length=45, blank=True, null=True)
    eng_link = models.CharField(max_length=500, blank=True, null=True)
    eng_rating = models.FloatField(blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Goals(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    goal = models.CharField(max_length=500, blank=True, null=True)
    duration = models.CharField(max_length=2, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    roll_up = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='f_rollup')
    break_down = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='f_breakdown')
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500, blank=True, null=True)
    subcomp = models.ForeignKey('Subcomps', on_delete=models.CASCADE)
    section = models.ForeignKey('Sections', on_delete=models.CASCADE)
    exit_on_no = models.CharField(max_length=1, blank=True, null=True)
    next = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='f_nxt')
    level = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    outcome = models.ForeignKey('Outcomes', on_delete=models.CASCADE)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    yes = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    no = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='f_yes')

    def __str__(self):
        return self.question
    
class Sections(models.Model):
    section_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    next_section = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    first_question = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Outcomes(models.Model):
    outcome_id = models.AutoField(primary_key=True)
    outcome = models.CharField(max_length=500, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.outcome

class Resources(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    resource_link = models.CharField(max_length=500, blank=True, null=True)
    resource_type = models.CharField(max_length=45, blank=True, null=True)
    resource_rating = models.FloatField(blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.resource

class Scores(models.Model):
    score_id = models.AutoField(primary_key=True)
    ass_id = models.ForeignKey('Assessments', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Questions', on_delete=models.CASCADE)
    score = models.IntegerField()
    create_date = models.DateField(blank=True, null=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.ass_id.user_id.username + ': '+ self.ass_id.name + ' - '+ self.question_id.question + ' [' + str(self.score) + ']'

class Subcomps(models.Model):
    subcomp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    comp = models.ForeignKey('Components', on_delete=models.CASCADE)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.comp.name
