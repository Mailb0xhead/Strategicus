from django.urls import path

from . import views, apiviews

urlpatterns = [
    path('', views.index, name='index'),
    path('question', views.question, name='question'),
    path('subcomp', views.subcomp, name='subcomp'),
    path('question/', apiviews.question, name='question'),
    path('ai_old/', views.ai, name='ai'),
    path('engagement/', views.engagement, name='engagement'),
    path('ai/', apiviews.ai, name='ai'),
    path('assessment/', views.assessment, name='assessment'),
    ]