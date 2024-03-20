from django.urls import path

from . import views, apiviews

urlpatterns = [
    path('', views.index, name='index'),
    path('question', views.question, name='question'),
    path('question/', apiviews.question, name='question'),
    path('profile',views.profile, name='profile' ),
    path('ai_old/', views.ai, name='ai'),
    path('engagement/', views.engagement, name='engagement'),
    path('ai2/', apiviews.ai, name='ai'),
    path('assessment/', views.assessment, name='assessment'),
    ]