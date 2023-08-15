from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from uuid import uuid4
import json

class AppUserManager(BaseUserManager):

    def create_user(self, email, password, **fields):
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("email is required")

        user_email = self.normalize_email(email=email)
        user:AppUser = self.model(email=user_email, **fields)
        user.set_password(raw_password=password)
        return user
    

    def create_superuser(self, email, password, **fields,):
        user: AppUser = self.create_user( email=email,password=password, **fields)
        user.is_staff = True
        user.is_superuser =  True
        user.is_verified = True
        user.save()
        return user




class AppUser(AbstractUser):
    
    def profile_directory(instance, filename):
        return '/'.join(['images',str(instance.email),filename])

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(blank=False, null=False)
    is_verified = models.BooleanField(blank=False, default=False)
    verification_token = models.CharField(max_length=30, null=True)
    profile_pic = models.ImageField(upload_to=profile_directory, null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = AppUserManager() 







@receiver(post_save,sender=AppUser)
def send_mail_for_verification(sender, instance:AppUser , created, **kwargs):
        
    print(kwargs)    
    if created:
        token = uuid4()
        instance.verification_token = token
        
        subject = "email verification"
        message = f'click this link to verify your email http://52.66.71.251:8000/foodapp/auth/verify/{instance.verification_token}'
        receipent_list = [instance.email]
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,receipent_list)
        except Exception as e:
            print(e)    
