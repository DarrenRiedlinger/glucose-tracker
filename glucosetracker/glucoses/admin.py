from django.contrib import admin

from .models import Glucose, Category


class GlucoseAdmin(admin.ModelAdmin):
    list_display = [
        'value',
        'category',
        'record_date',
        'record_time',
        'notes',
        'user',
        'created',
        'modified',
    ]

    list_filter = [
        'user',
        'category',
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]


admin.site.register(Glucose, GlucoseAdmin)
admin.site.register(Category, CategoryAdmin)
