from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('register/', views.CreateAccountView.as_view(), name='register'),

    path('dashboard/', views.TaskDashboard.as_view(), name='dashboard'),

    path('all-tasks-for-user/', views.AllUserAssignedTasks.as_view(), name='all-tasks-for-user'),
    path('all-tasks-assigned-by-user', views.AllTasksUserAssigned.as_view(), name='all-tasks-assigned-by-user'),
    path('archivedTasks/', views.ArchivedTaskList.as_view(), name='archived-task'),

    path('newtask/', views.TaskForm.as_view(), name='new-task'),
    path('updatetask/<int:pk>/', views.EditTask.as_view(), name='update-task'),


]