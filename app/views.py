from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializer import *
from .services import *

# Create your views here.
class ProjectView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response({"data": serializer.data})

class TaskView(APIView):
    def get(self, request):
        project_id = request.query_params.get('project_id', None)

        try:
            project = Project.objects.get(id = project_id)
        except Project.DoesNotExist:
            return Response({"data": "Project not found."})

        tasks = Task.objects.filter(project = project)
        serializer = TaskSerializer(tasks, many=True)

        if not serializer.data:
            return Response({"data": "No tasks found for this project."})
        return Response({"data": serializer.data})

class TaskDetailsView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id = task_id)
        except Task.DoesNotExist:
            return Response({"data": "Task does not exists"})

        serializer = TaskSerializer(task)
        return Response({"data": serializer.data})

    def post(self, request, task_id):
        try:
            task = Task.objects.get(id = task_id)
        except Task.DoesNotExist:
            return Response({"data": "Task does not exists"})

        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Task has been closed"})
        return Response({"data": "Failed to close task"})

class AssignTaskView(APIView):
    def post(self, request, task_id):
        resource_id = request.data.get('resource_id')

        if not task_id or not resource_id:
            return Response({"data": "Task or Resource id's are missing"})

        try:
            task = assign_resource_to_task(task_id=task_id, resource_id=resource_id)
            serializer = TaskSerializer(task)
            return Response({"data": serializer.data})
        except Exception as e:
            return Response({'data': e.detail[0]})

class MatchedResourceView(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')

        if not task_id:
            return Response({"error": "Missing task_id parameter."}, status=400)

        try:
            task = Task.objects.select_related('skill').get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=404)

        required_skill = task.skill

        # Find all resources that have this skill and resource avaliblity
        matched_resources = Resource.objects.filter(skills=required_skill, current_status='avalible')

        data = [
            {
                "id": res.id,
                "name": res.name,
                "short_description": res.short_description,
                "status": res.current_status,
                "skills": [skill.name for skill in res.skills.all()]
            }
            for res in matched_resources
        ]

        return Response({"data": data}, status=200)

class SkillsView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"data": serializer.data})

class ResourceBasedOnSkill(APIView):
    def get(self, request):
        requested_skill = request.query_params.get('skill')

        if not requested_skill:
            return Response({"error": "Missing skill parameter."}, status=400)

        try:
            if requested_skill == 'all':
                resources = Resource.objects.all()
            else:
                resources = Resource.objects.filter(skills__name__iexact=requested_skill)

            serializer = ResourceSerializer(resources, many=True)
            return Response({"data": serializer.data})
        except:
            return Response({"data": []})
