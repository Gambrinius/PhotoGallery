from django.contrib import admin
from users.models import UserProfile
# Register your models here.


class AdminProfile(admin.ModelAdmin):
    fields = ['user', 'first_name', 'last_name', 'birthday', 'avatar', 'about_user']

admin.site.register(UserProfile, AdminProfile)
