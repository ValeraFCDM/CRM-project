from django.contrib import admin
from .models import Supply, SupplyProduct

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'delivery_date')
    list_display_links = ('supplier', )
