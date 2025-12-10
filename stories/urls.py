from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('submit/', views.submit_story, name='submit_story'),
    path('<int:pk>/', views.story_detail, name='story_detail'),
]
