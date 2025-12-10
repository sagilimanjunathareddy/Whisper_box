from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:story_id>/', views.add_comment, name='add_comment'),
]
