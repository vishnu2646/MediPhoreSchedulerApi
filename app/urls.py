from django.urls import path
from .views import *

urlpatterns = [
    path('projects', ProjectView.as_view(), name='projetcs'),
    path('tasks', TaskView.as_view(), name='tasks'),
    path('tasks/<int:task_id>', TaskDetailsView.as_view(), name='task-details'),
    path('resources', ResourceBasedOnSkill.as_view(), name='resource_based_on_skill'),
    path('resources/search', MatchedResourceView.as_view(), name='resource_search'),
    path('skills', SkillsView.as_view(), name="skills"),
]