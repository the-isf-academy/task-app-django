import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User # new
# Create your models here.

class Task(models.Model):
    task_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    task_assigned_to = models.CharField(max_length=30,default="",blank=True)
    task_assigned_by = models.CharField(max_length=30,default="", editable=False)

    title =  models.CharField(max_length=30)
    label =  models.CharField(max_length=8)
    notes = models.TextField(editable=True)

    due_date = models.DateField('Date Due', editable=True)    
    pub_date = models.DateTimeField('Date Created',default=now, editable=False)    
    archive = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def date_created(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)