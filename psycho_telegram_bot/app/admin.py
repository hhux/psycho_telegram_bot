from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'comment', 'is_active')
    search_fields = ('comment',)
    readonly_fields = ('comment',)

admin.site.register(User, UserAdmin)
