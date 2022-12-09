from django.contrib import admin
from .models import*
from django.contrib.admin import DateFieldListFilter
# Register your models here.

@admin.register(ModePrediction)
class ModePredictionAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['name', 'description']


@admin.register(TypePrediction)
class TypePredictionhAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )
    list_display = ['name', 'description']



@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    date_hierarchy = 'match__date'
    list_filter = (
        ('match__date', DateFieldListFilter),
    )
    list_display = ['mode', 'type', 'pct', 'is_checked']
