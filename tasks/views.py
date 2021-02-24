from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *
from .forms import TaskForm

class WelcomeView(TemplateView):
    template_name = 'task/welcomeView.html'

# class CreateAccount(FormView):
#     template_name = 'task/createAccount.html'
#     success_url = '/home'


#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.save()
#         username = form.cleaned_data.get('username')
#         raw_password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=raw_password)
#         login(request, user)
#         return redirect('home')

class TaskList(ListView):

    template_name = 'task/taskList.html'
    model = Task
    paginate_by = 3
    context_object_name = 'tasks'

    def get_queryset(self):
        #Filters archived tasks out of main list 
        return self.model.objects.filter(archive=False).filter(task_user=self.request.user).order_by('-due_date')


class TaskForm(LoginRequiredMixin,FormView):
    template_name = 'task/TaskForm.html'
    form_class = TaskForm
    success_url = '/home'


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.task_user = self.request.user
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
    success_url = '/home'
    
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
        return self.model.objects.filter(archive=True).filter(task_user=self.request.user)