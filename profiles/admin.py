from django.contrib import admin
from .models import UserProfile, Role, Institution

admin.site.register(Institution)
admin.site.register(UserProfile)
admin.site.register(Role)
