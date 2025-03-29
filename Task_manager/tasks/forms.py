from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Import the custom user model

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    """
    A form for user registration using email 
    - Extends Django's built-in UserCreationForm.
    - Requires email, password1 (new password), and password2 (password confirmation).
    """
    class Meta:
        model = CustomUser                            # Use the custom user model
        fields = ['email', 'password1', 'password2']  # Fields included in the form

    def clean_email(self):
        """
        Validates the email field:
        - Ensures that the email is unique.
        - Raises a validation error if the email is already in use.
        """
        email = self.cleaned_data.get("email")               # Get the email from form data
        if CustomUser.objects.filter(email=email).exists():  # Check if email already exists
            raise forms.ValidationError("A user with this email already exists.")  # Raise error if duplicate
        return email  # Return the validated email


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
        model = CustomUser  # Use the custom user model
        fields = ['username', 'password']  # Fields required for login
