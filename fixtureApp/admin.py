from django.contrib import admin
from .models import*
from django.contrib.admin import DateFieldListFilter
# Register your models here.





@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'date'
    list_filter = (
        ('date', DateFieldListFilter),
    )
    list_display = ['date', 'home', "away", "is_finished", "edition"]



@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['match', 'team', "minute", "is_penalty"]

