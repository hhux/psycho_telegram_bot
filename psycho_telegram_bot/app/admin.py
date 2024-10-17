from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('comment',)

admin.site.register(User, UserAdmin)
