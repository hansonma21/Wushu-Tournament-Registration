from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
admin.site.unregister(User)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'birth_date', 'sex', 'skill_level', 
              'school_or_club', 'is_judge')

class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]

admin.site.register(User, ProfileAdmin)