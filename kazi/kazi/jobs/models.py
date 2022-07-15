
import email
from pyexpat import model
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
from django.db.models.deletion import CASCADE, SET_NULL
from  django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from sqlalchemy import true
from kazi.settings import AUTH_USER_MODEL
from django.conf import settings


class userManagement(BaseUserManager):
    def create_user(self,email,username,First_name,Last_name,phone_nember,password=None):
        if not email:
            raise ValueError('please enter a valid email')
        if not username:
            raise ValueError('please provide a username')
        if not First_name:
            raise ValueError("Please provide  your first name")
        if not Last_name:
            raise ValueError("please provide Last name")
        if not phone_nember:
            raise ValueError("Please provide the phone number")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            First_name = First_name,
            Last_name = Last_name,
            phone_nember = phone_nember,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,email,username,First_name,Last_name,phone_nember,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            First_name = First_name,
            Last_name = Last_name,
            phone_nember = phone_nember,
            password=password
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)
        return user


class User_profile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="enter email", unique=True)
    username = models.CharField(max_length=200,verbose_name="username", unique="True")
    First_name = models.CharField(max_length=200,verbose_name="first name")
    Last_name = models.CharField(max_length=200,verbose_name="first name")
    phone_number = models.CharField(max_length=12,verbose_name="enter phone number")
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default=False)
    is_superuser =models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username','First_name','Last_name','phone_number']

    objects=userManagement()

    def __str__(self):
        return self.First_name + " " + self.Last_name
    def has_perm(self, perm, obj=None) :
        return True
    def has_module_perms(self, app_label):
        return True

class jobCategory(models.Model):
    job_cat = (
        ('JOB','job'),
        ('JOB','job'),
        )

    name = models.CharField(max_length=200,choices=job_cat)
    def __str__(self):
        return self.name

class Jobs(models.Model):
    poster = models.ForeignKey(User_profile,on_delete=SET_NULL,null=True)
    Job_Title = models.CharField(max_length=200,verbose_name='enter Job title')
    Company_name = models.CharField(max_length=200,verbose_name='company name')
    Job_category = models. ForeignKey(jobCategory, on_delete= models.SET_NULL, null = True)
    short_description = models.TextField()
    job_description = RichTextField()
    date_added = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return self.Job_Title