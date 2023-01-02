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

class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500, blank=True, null=True)
    subcomp = models.ForeignKey('Subcomps', on_delete=models.CASCADE)
    yes = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    no = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='f_yes')
    outcome = models.ForeignKey('Outcomes', on_delete=models.CASCADE)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.question

class Outcomes(models.Model):
    outcome_id = models.AutoField(primary_key=True)
    outcome = models.CharField(max_length=500, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.outcome

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


