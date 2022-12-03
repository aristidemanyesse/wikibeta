from django.contrib import admin
from .models import*
from django.contrib.admin import DateFieldListFilter
# Register your models here.

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['name', 'code']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['name', 'code',"pays"]



@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_display = ['name']


@admin.register(EditionCompetition)
class EditionCompetitionAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'start_date'
    list_filter = (
        ('start_date', DateFieldListFilter),
    )
    list_display = ['competition', 'edition',  'start_date', 'finish_date']



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



@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'date'
    list_filter = (
        ('date', DateFieldListFilter),
    )
    list_display = ['date', 'home', "away", "result", "edition"]


@admin.register(ExtraInfosMatch)
class ExtraInfosMatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['match', 'home_shots', "away_shots", "home_corners", "away_corners"]



@admin.register(BeforeMatchStat)
class BeforeMatchStatAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['match', 'team', "ppg", "goals_scored", "goals_conceded"]




@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['match', 'team', "minute", "is_penalty"]

