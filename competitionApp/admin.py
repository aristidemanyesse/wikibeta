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
    list_display = ['name', "flag", 'code']



@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['code', "name" ,"type","pays", "logo"]
    list_editable = ["name", "logo"]



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
    list_display = ['competition', 'edition',  'start_date', 'finish_date', "is_finished"]




@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'date'
    list_display = ['edition', "date", "created_at"]



@admin.register(LigneRanking)
class LigneRankingAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'ranking__date'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['ranking', "team", "level", "mj", "form", "created_at"]




@admin.register(CompetitionStat)
class CompetitionStatAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['edition', "avg_goals", "avg_fouls", "avg_corners", "avg_yellow_cards", "created_at"]
