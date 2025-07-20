from django.db import models

# Create your models here.

STATUS_CHOICES = [
    ('not started', 'Not Started'),
    ('in progress', 'In Progress'),
    ('completed', 'Completed'),
]

RESOURCE_STATUS = [
    ('avalible', 'Avalible'),
    ('unavailable', 'Unavailable'),
    ('busy', 'Busy'),
]

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Skill(BaseModel):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Resource(BaseModel):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, null=True, blank=True)
    skills = models.ManyToManyField(Skill,related_name="resource_skills")
    current_status = models.CharField(max_length=50, choices=RESOURCE_STATUS, default='avalible')

    def __str__(self):
        return self.name

class Project(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duedate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not started')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    def __str__(self):
        return self.name

class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not started')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(Project, related_name='project_skills', on_delete=models.CASCADE)
    assigned_resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return self.title

    def can_be_assigned_to(self, resource):
        return self.skill in resource.skills.all()