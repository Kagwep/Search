from django.contrib import admin
from .models import User_profile,jobCategory,Jobs

# Register your models here.

admin.site.register(User_profile)
admin.site.register(jobCategory)
admin.site.register(Jobs)