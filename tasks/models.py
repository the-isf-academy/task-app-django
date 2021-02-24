import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now
# Create your models here.

class Task(models.Model):
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