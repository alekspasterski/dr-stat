from django.contrib import admin
from .models import CpuData, CpuUsageData, MemoryData, DiskData, DiskUsageData, FilesystemData, FilesystemUsageData, PartitionData, Settings

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


@admin.register(CpuUsageData)
class CpuUsageDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpu_usage', 'cpu_number')
    list_filter = ('id',)
    ordering = ('-id',)

@admin.register(DiskData)
class DiskDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'hw_id', 'device')
    list_filter = ('id',)
    ordering = ('-id',)

@admin.register(DiskUsageData)
class DiskUsageDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'total')
    list_filter = ('id',)
    ordering = ('-id',)

@admin.register(PartitionData)
class PartitionDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'device', 'uuid', 'active', 'total')
    list_filter = ('active', 'device')

@admin.register(FilesystemData)
class FilesystemDataAdmin(admin.ModelAdmin):
    list_display = ('mount_point', 'label', 'filesystem_type', 'active')
    list_filter = ('filesystem_type', 'active')

@admin.register(FilesystemUsageData)
class FilesystemUsageDataAdmin(admin.ModelAdmin):
    list_display = ('filesystem', 'timestamp', 'size', 'free')
    list_filter = ('timestamp', 'filesystem')
    ordering = ('-timestamp',)

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('retention_period',)
