from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, first_name, last_name, user_type, role, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, user_type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, first_name, last_name, user_type, extra_fields.pop('role', 'admin'), password, **extra_fields)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    MENTOR = 'mentor'
    MENTEE = 'mentee'
    WELLWISHER = 'wellwisher'
    ADMIN = 'admin'  

    USER_TYPE_CHOICES = [
        (MENTOR, _('Mentor')),
        (MENTEE, _('Mentee')),
        (WELLWISHER, _('Well-Wisher')),
        (ADMIN, _('Admin'))  
    ]
    role=models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
   
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) 
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["first_name", "last_name", "user_type"]
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"

    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
class OneTimePassword(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    code=models.CharField(max_length=6,unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"
class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    intro_as_mentor = models.TextField()
    mentoring_topics = models.TextField()
    area_of_expertise = models.TextField()
    linkedin = models.URLField(max_length=200)
    video_call_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.user.email
    
class MenteeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    intro_as_mentee = models.TextField()
    development_goal = models.TextField()
    linkedin = models.URLField(max_length=200)

    def __str__(self):
        return self.user.email

class WellWisherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    interests = models.TextField(blank=True, null=True)
    organization_affiliation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email
