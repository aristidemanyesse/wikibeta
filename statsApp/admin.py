from django.contrib import admin
from .models import*
from django.contrib.admin import DateFieldListFilter
# Register your models here.



@admin.register(ExtraInfosMatch)
class ExtraInfosMatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['match', 'home_shots', "away_shots", "home_corners", "away_corners"]



@admin.register(ResultMatch)
class ResultMatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['match', "home_score", "away_score",  "result"]





@admin.register(BeforeMatchStat)
class BeforeMatchStatAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['match', 'team', "ppg", "goals_scored", "goals_conceded"]


