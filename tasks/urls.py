from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('register/', views.CreateAccountView.as_view(), name='register'),
    path('home/', views.AllTasks.as_view(), name='all-tasks'),

    path('newtask/', views.TaskForm.as_view(), name='new-task'),
    path('updatetask/<int:pk>/', views.EditTask.as_view(), name='update-task'),
    path('archivedTasks/', views.ArchivedTaskList.as_view(), name='archived-task'),


]