from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    """
    Custom authentication backend that allows users to log in using their email 
    """
    def authenticate(self, request, email=None, password=None):
        """
        Authenticate a user based on email and password.
        """
        User = get_user_model()  # Get the custom user model
        try:
            user = User.objects.get(email=email)  # Retrieve user by email
            if user.check_password(password):  # Verify the provided password
                return user  # Return the authenticated user
        except User.DoesNotExist:
            return None  # Return None if the user does not exist or login  fails

    def get_user(self, user_id):
        """
        Retrieve a user by their primary key (ID).
        Used for session authentication.
        """
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)  # Retrieve user by ID
        except User.DoesNotExist:
            return None  # Return None if the user is not found

