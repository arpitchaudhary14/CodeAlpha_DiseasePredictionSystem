from django.contrib import admin
from .models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'disease', 'prediction', 'label', 'probability', 'created_at')
    list_filter = ('disease', 'label', 'created_at')
    search_fields = ('user__username', 'disease', 'label')
    readonly_fields = ('created_at',)
    
    # Make the input_data field formatted nicely in the admin panel if desired
    # (Django 4.0+ displays JSONField pretty well by default)
