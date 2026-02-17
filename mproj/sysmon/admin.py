from django.contrib import admin
from .models import CpuData, MemoryData

@admin.register(CpuData)
class CpuDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'avg_load')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(MemoryData)
class MemoryDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'free', 'total')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
