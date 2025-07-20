from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Task, Resource

def assign_resource_to_task(task_id, resource_id):
    with transaction.atomic():
        try:
            task = Task.objects.get(id=task_id)
            resource = Resource.objects.get(id=resource_id)
        except Task.DoesNotExist:
            raise ValidationError("Task not Found")
        except Resource.DoesNotExist:
            raise ValidationError("Resource not Found")

        if resource.current_status != 'avalible':
            raise ValidationError("Resource is not available to assign the Task.")

        if not resource.skills.filter(id=task.skill.id).exists():
            raise ValidationError("Resource does not have enough required skills.")

        task.assigned_resource = resource
        task.save()

        resource.current_status = 'busy'
        resource.save()

        return task