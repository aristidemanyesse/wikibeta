from django.contrib import admin
from .models import*
from django.contrib.admin import DateFieldListFilter
# Register your models here.



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['name', 'code', "pays", "logo"]


@admin.register(EditionTeam)
class EditionTeamAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['team', 'edition']

