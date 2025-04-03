# task_management/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    Provides helper methods to create regular users and superusers.
    """
    def create_user(self, email, username,password=None):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')  # Ensure email is provided
        if not username:
            raise ValueError('The username must be provided')#ensure username is provided
        
        
        email = self.normalize_email(email)  # Normalizes email (e.g., lowercasing domain part)
        user = self.model(email=email, username=username )  # Create a new user instance
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save user to the database
        return user
    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField( max_length=150, null=True, blank=True ,default='username') #username
    is_active = models.BooleanField(default=True)    #Determines whether a user’s account is active.or user wont be able to log
    is_staff = models.BooleanField(default=False)    #Defines whether a user has access to the Django admin panel.
    date_joined = models.DateTimeField(auto_now_add=True)#Automatically stores the timestamp when a user registers.

    objects = CustomUserManager()                    #logic for creating users (create_user) and superusers (create_superuser).

    USERNAME_FIELD = 'email'                         #Specifies that email will be used as the unique identifier
    REQUIRED_FIELDS = []                              #REQUIRED_FIELDS defines additional required fields when using createsuperuser.

    def __str__(self):
        return self.email                            #Returns the email as the string representation of the user.
    
#creating task models
class Task(models.Model):
    # Category choices
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    STATUS_CHOICES = [
        ('COMPLETE', 'Complete'),
        ('INCOMPLETE', 'Incomplete'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(  choices= STATUS_CHOICES ,default='INCOMPLETE')  # False=Incomplete, True=Complete
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='MEDIUM')
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']  #tasks first by date due


    def __str__(self):
        return f"{self.title} - {self.status_display()}"

    def status_display(self):
        return "Complete" if self.status else "Incomplete"