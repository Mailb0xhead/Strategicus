from django.urls import path

from . import views, apiviews

urlpatterns = [
    path('', views.index, name='index'),
    path('results', views.results, name='results'),
    path('question', views.question, name='question'),
    path('subcomp', views.subcomp, name='subcomp'),
    path('question/', apiviews.question, name='question'),
    path('assessment/', views.assessment, name='assessment'),
    ]