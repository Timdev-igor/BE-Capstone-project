from django.shortcuts import render, get_object_or_404,redirect
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm ,TaskForm 
from django.contrib.auth.decorators import  login_required
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now


# User Registration View
def register(request):
   
   # Handles user registration.
   # - If the request is POST, it processes the submitted form.
   #- If valid, saves the user, logs them in, and redirects to home.
   #- Otherwise, renders the registration form again.
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Bind form with POST data
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the user automatically after registration
            return redirect('home')  # Redirect to home page after successful registration
    else:
        form = CustomUserCreationForm()  # Create a blank form for GET request
    return render(request, 'tasks/registration.html', {'form': form})  # Render the registration template

# User Login View
def login_view(request):
    """
    Handles user login.
    - If  successful, logs in the user and redirects to home.
    - Otherwise, displays an error message.
    """
    if request.method == 'POST':
        email = request.POST['email']  # Get email from POST data
        password = request.POST['password']  # Get password from POST data
        user = authenticate(request, email=email, password=password)  # Authenticate user using custom backend
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('home')  # Redirect to the home page after login
        else:
            return render(request, 'tasks/login.html', {'error': 'Invalid email or password'})  # Show error message
    return render(request, 'tasks/login.html')  # Render the login page for GET requests

# User Logout View
def logout_view(request):
    """
    Logs out the user and redirects them to the login page.
    """
    logout(request)           # Log out the user
    return redirect('login')  # Redirect to the login page

# Home View (Requires  user Login)
@login_required
def home_view(request):
    """
    Displays the home page but only for logged-in users.
    - The @login_required decorator ensures only authenticated users can access this view.
    """
    return render(request, 'tasks/home.html')  # Render the home page

#task normal views

@login_required
def task_list(request):                           #list all created tasks
    tasks = Task.objects.filter(user=request.user)# Filter tasks for the logged-in user
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})

#tasks API VIEWS
# Task List View with Filtering, Searching, Ordering
# Task List View
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'due_date', 'created_at']

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        # Filtering
        priority = self.request.query_params.get('priority')
        if priority is not None:
            queryset = queryset.filter(priority=priority)

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        due_date = self.request.query_params.get('due_date')
        if due_date is not None:
            queryset = queryset.filter(due_date=due_date)

        return queryset


# Task Detail View
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# Task Create View
class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Task Update View

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()  # Queryset for all tasks
    serializer_class = TaskSerializer  # The serializer class for validating input data
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Permissions




# Task Delete View
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# Toggle Task Status
class TaskToggleStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        task.status = not task.status  # Toggle the status
        task.completed_at = now() if task.status else None
        task.save()

        return Response({
            'detail': f'Task marked as {"complete" if task.status else "incomplete"}',
            'status': task.status
        })