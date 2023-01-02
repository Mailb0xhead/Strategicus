from django.contrib import admin
from .models import Assessments, Components, Scores, Questions, Subcomps, Outcomes

# Register your models here.
admin.site.register(Assessments)
admin.site.register(Components)
admin.site.register(Scores)
admin.site.register(Questions)
admin.site.register(Subcomps)
admin.site.register(Outcomes)