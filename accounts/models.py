from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        # Ensure email and username are provided
        if not email:
            raise ValueError('Email must be provided')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):  
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email']),  
        ]
        index_together = [
            ('email',),
        ]
    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='userprofile_user')
    address = models.TextField('User Address',blank=True,max_length=255,null=True)
    zipcode = models.CharField('User Zipcode',max_length=16,blank=True,null=True)
    phone_number = models.CharField('User Contact Number', max_length=20, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return str(self.user)
    

class BlacklistedToken(models.Model):
    token = models.TextField()  # Store the entire JWT token
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted Token created at {self.created_at}"