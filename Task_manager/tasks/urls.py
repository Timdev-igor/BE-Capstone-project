from django.urls import path
from .views import register, login_view, logout_view,home_view

urlpatterns = [
    path('home/', home_view, name='home'), 
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #tasks
    path('task/create/', views.task_create, name='task_create'),

]