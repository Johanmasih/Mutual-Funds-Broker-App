from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Custom Manager for the User model
class UserManager(BaseUserManager):
    """
    Custom manager for User model to handle user creation
    and superuser creation with email as the unique identifier.
    """
    
    # Method to create a regular user
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        Ensures that the email is normalized and that the user has a password.
        """
        # Ensure email is provided
        if not email:
            raise ValueError('Email must be provided')
        
        # Normalize the email (e.g., convert to lowercase)
        email = self.normalize_email(email)
        
        # Create the user instance
        user = self.model(email=email, username=username, **extra_fields)
        
        # Set the user's password (hashing it)
        user.set_password(password)
        
        # Save the user to the database
        user.save()
        return user

    # Method to create a superuser (admin user)
    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser (admin) with elevated privileges.
        """
        # Ensure superuser has both 'is_staff' and 'is_superuser' flags set to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Use the create_user method to actually create the superuser
        return self.create_user(email, username, password, **extra_fields)


# Custom User model that uses email as the unique identifier
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that inherits from AbstractBaseUser and PermissionsMixin.
    It uses email as the unique identifier for authentication (instead of the default username).
    """
    
    email = models.EmailField(unique=True)  # Unique email field
    username = models.CharField(max_length=150, null=True, blank=True)  # Username is optional
    is_active = models.BooleanField(default=True)  # User's active status
    is_staff = models.BooleanField(default=False)  # Staff flag, determines if the user can access the admin site

    # Set the email field as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    
    # No required fields other than email for this custom user model
    REQUIRED_FIELDS = []

    # Attach the custom user manager
    objects = UserManager()

    class Meta:
        # Add an index on the 'email' field for faster lookups
        indexes = [
            models.Index(fields=['email']),  
        ]
        # Define the set of fields that should be used for a multi-field index
        index_together = [
            ('email',),
        ]

    def __str__(self):
        """Return the user's email when the user is printed"""
        return self.email
    

# Profile model to store additional user-related information
class UserProfile(models.Model):
    """
    A model that stores additional user information such as address,
    phone number, and other profile details. Each User has a one-to-one
    relationship with the UserProfile.
    """
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='userprofile_user')  # Each user has one profile
    address = models.TextField('User Address', blank=True, max_length=255, null=True)  # User's address (optional)
    zipcode = models.CharField('User Zipcode', max_length=16, blank=True, null=True)  # User's zipcode (optional)
    phone_number = models.CharField('User Contact Number', max_length=20, blank=True, null=True)  # User's contact number (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the profile was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last time the profile was updated

    def __str__(self):
        """Return a string representation of the user profile (linked to the user)"""
        return str(self.user)
    

# BlacklistedToken model to store blacklisted JWT tokens
class BlacklistedToken(models.Model):
    """
    A model to store JWT tokens that are blacklisted, to ensure that
    those tokens cannot be used again for authentication.
    """
    token = models.TextField()  # Store the entire JWT token as text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the token was blacklisted

    def __str__(self):
        """Return a string representation of the blacklisted token, showing its creation time"""
        return f"Blacklisted Token created at {self.created_at}"
