from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, FormView, UpdateView
from django.views.generic.detail import DetailView

from .models import *
from .forms import TaskForm


class TaskList(ListView):

    template_name = 'task/taskList.html'
    model = Task
    paginate_by = 3
    context_object_name = 'tasks'

    def get_queryset(self):
        #Filters archived tasks out of main list 
        return self.model.objects.filter(archive=False).order_by('-due_date')


class TaskForm(FormView):
    template_name = 'task/TaskForm.html'
    form_class = TaskForm
    success_url = '/'


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)


class DetailTask(DetailView):

    template_name = 'task/detailTask.html' 
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EditTask(UpdateView):
    model = Task
    template_name = 'task/updateTask.html'    
    success_url = '/'
    
    fields = [
        "title",
        "label",
        "notes",
        "archive",
        "due_date"
    ]

class ArchivedTaskList(ListView):

    template_name = 'task/archivedTaskList.html' 
    model = Task
    # paginate_by = 12
    context_object_name = 'tasks'

    def get_queryset(self):
        #Filters archived tasks out of main list 
        return self.model.objects.filter(archive=True)