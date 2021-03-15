from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.db.models import Q


from .models import *
from .forms import TaskForm, CreateAccountForm

class WelcomeView(TemplateView):
    template_name = 'task/welcomeView.html'

class CreateAccountView(FormView):
    template_name = 'task/createAccount.html'
    form_class = CreateAccountForm

    success_url = '/dashboard'


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)


class TaskForm(LoginRequiredMixin,FormView):
    template_name = 'task/TaskForm.html'
    form_class = TaskForm
    success_url = '/dashboard'


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        if form.instance.task_assigned_to != "":
            form.instance.task_assigned_by = self.request.user.username
        
        form.instance.task_user = self.request.user
        form.save()
        return super().form_valid(form)


class AllUserAssignedTasks(ListView):

    template_name = 'task/all-tasks-for-user.html' 
    model = Task
    paginate_by = 5
    context_object_name = 'tasks'


    def get_queryset(self):
        #Filters archived tasks out of main list 
        data = self.model.objects.all().filter(archive=False)
        user_created_tasks = data.filter(task_user=self.request.user).filter(~Q(task_assigned_by=self.request.user.username))
        user_assigned_tasks = data.filter(task_assigned_to=self.request.user.username)
        tasks = user_created_tasks | user_assigned_tasks
        return tasks.distinct().order_by('-due_date') 

class AllTasksUserAssigned(ListView):

    template_name = 'task/all-tasks-assigned-by-user.html' 
    model = Task
    paginate_by = 5
    context_object_name = 'tasks'


    def get_queryset(self):
        #Filters archived tasks out of main list 
        data = self.model.objects.all().filter(archive=False)
        user_created_tasks = data.filter(task_user=self.request.user).filter(task_assigned_by=self.request.user.username)
        return user_created_tasks.distinct().order_by('-due_date') 


class TaskDashboard(ListView):
    template_name = 'task/dashboard.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.model.objects.all().filter(archive=False)

        # filter tasks for user
        user_created_tasks = data.filter(task_user=self.request.user).filter(~Q(task_assigned_by=self.request.user.username))
        user_assigned_tasks = data.filter(task_assigned_to=self.request.user.username)
        tasks = user_created_tasks | user_assigned_tasks
        context['user_tasks'] = tasks.distinct().order_by('-due_date')[0:3]

        # filter tasks user assigned to other users 
        user_created_tasks = data.filter(task_user=self.request.user).filter(task_assigned_by=self.request.user.username)
        context['user_created_tasks'] = user_created_tasks.distinct().order_by('-due_date')[0:3]

        return context

class EditTask(UpdateView):
    model = Task
    template_name = 'task/updateTask.html'    
    success_url = '/dashboard'
    
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

    # def get_queryset(self):
    #     #Filters archived tasks out of main list 
    #     return self.model.objects.filter(archive=True).filter(task_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_created_tasks = Task.objects.filter(archive=True).filter(task_user=self.request.user)
        user_assigned_tasks = Task.objects.filter(archive=True).filter(task_assigned_to=self.request.user.username)
        tasks = user_created_tasks | user_assigned_tasks
        context['archived_tasks'] = tasks.distinct().order_by('-due_date') 

        return context
