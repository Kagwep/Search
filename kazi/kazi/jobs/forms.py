from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import User_profile,Jobs
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User_profile
        fields = ['username','email','First_name','Last_name','phone_number','password1','password2']
class CreateJob(ModelForm):
    class Meta:
        model =Jobs
        fields = '__all__'
        exclude = ['poster']
