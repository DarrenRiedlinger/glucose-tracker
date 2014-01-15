from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from accounts.models import UserSettings


class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'is_superuser',
        'last_login',
        'date_joined',
    ]


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'time_zone',
        'modified',
        'created',
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)
