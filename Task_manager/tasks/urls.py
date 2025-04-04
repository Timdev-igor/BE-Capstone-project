from django.urls import path
from .views import register, login_view, logout_view,home_view
from . import views

urlpatterns = [
    path('home/', home_view, name='home'), 
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    #tasks views
    path('create/', views.task_create, name='task_create'),
    path('', views.task_list, name='task_list'),
    # Task Detail for specific task
    path('<int:pk>/', views.task_detail, name='task_detail'),
    # Task Update 
    path('<int:pk>/edit/', views.task_update, name='task_update'),
    # Task Delete 
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),

]