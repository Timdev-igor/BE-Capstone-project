from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Task  # Import the custom user model

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    """
    A form for user registration using email 
    - Extends Django's built-in UserCreationForm.
    - Requires email, password1 (new password), and password2 (password confirmation).
    """
    class Meta:
        model = CustomUser                            # Use the custom user model
        fields = ['email',  'username', 'password1', 'password2']  # Fields included in the form

    def clean_email(self):
        email = self.data.get('email')  # Directly access form data
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.data.get('username')  # Directly access form data
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is taken.")
        return username                                   


# Custom User Login Form
class CustomUserLoginForm(AuthenticationForm):
    """
    A login form that allows authentication using email instead of a username.
    - Replaces the username field with an email field.
    """
    username = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={"autofocus": True})  
    )
    class Meta:
        model = CustomUser                 # Use the custom user model
        fields = ['username', 'password']  # Fields required for login

#task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'priority']

    due_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        
    }))
