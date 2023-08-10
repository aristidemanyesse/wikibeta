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




@admin.register(TypeFact)
class TypeFactAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['name', 'description']



@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['match', 'type', "all_matches", "full_time", "team", "total", "success", "pct"]


@admin.register(TeamProfileMatch)
class TeamProfileMatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ["date", 'match', 'team', "dynamic", "attack", "defense", "pression", "clean"]