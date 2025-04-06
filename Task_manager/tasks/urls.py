from django.urls import path
from .views import register, login_view, logout_view,home_view
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView
from .views import task_list, task_create, task_detail, task_update, task_delete

urlpatterns = [
    path('home/', home_view, name='home'), 
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #tasks views
     # Normal task views
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('<int:pk>/edit/', task_update, name='task_update'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    #api views 
    # API views
    path('api/tasks/', TaskListView.as_view(), name='api_task_list'),
    path('api/tasks/create/', TaskCreateView.as_view(), name='api_task_create'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='api_task_details'),
    path('api/tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='api_task_update'),
    path('api/tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='api_task_delete'),
    

]