# task_management/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    Provides helper methods to create regular users and superusers.
    """
    def create_user(self, email, password=None):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')  # Ensure email is provided
        
        email = self.normalize_email(email)  # Normalizes email (e.g., lowercasing domain part)
        user = self.model(email=email )  # Create a new user instance
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save user to the database
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)    #Determines whether a user’s account is active.or user wont be able to log
    is_staff = models.BooleanField(default=False)    #Defines whether a user has access to the Django admin panel.
    date_joined = models.DateTimeField(auto_now_add=True)#Automatically stores the timestamp when a user registers.

    objects = CustomUserManager()                    #logic for creating users (create_user) and superusers (create_superuser).

    USERNAME_FIELD = 'email'                         #Specifies that email will be used as the unique identifier
    REQUIRED_FIELDS = []                              #REQUIRED_FIELDS defines additional required fields when using createsuperuser.

    def __str__(self):
        return self.email                            #Returns the email as the string representation of the user.