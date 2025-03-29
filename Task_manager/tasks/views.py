from django.shortcuts import render,redirect
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import  login_required

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
    - If authentication is successful, logs in the user and redirects to home.
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
