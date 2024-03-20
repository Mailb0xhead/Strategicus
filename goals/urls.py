from django.urls import path

from . import views, apiviews

urlpatterns = [
    path('', views.index, name='index'),
    path('goal/', views.goals, name='goals'),
    path('goalapi/', apiviews.goals_api, name='goals'),
    path('goal_drilldown/', apiviews.goal_drilldown, name='drilldown'),
    path('goaledit/', apiviews.goaledit, name='goaledit'),
    ]