from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from accounts.models import UserSettings


class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'settings_time_zone',
        'last_login',
        'date_joined',
    ]

    def settings_time_zone(self, instance):
        """
        This method allows us to access the time_zone attribute of Settings
        to display in the Django Admin.
        """
        return instance.settings.time_zone


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
