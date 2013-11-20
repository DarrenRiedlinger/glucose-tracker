from django.contrib import admin

from .models import UserSettings


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'time_zone',
    ]


admin.site.register(UserSettings, UserSettingsAdmin)
