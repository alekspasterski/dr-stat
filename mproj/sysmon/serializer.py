#!/usr/bin/env python3

from rest_framework import serializers
from .models import CpuUsageData, MemoryData, CpuData, DiskData, DiskUsageData, PartitionData, FilesystemData, FilesystemUsageData, Settings

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryData
        fields = '__all__'

class CpuUsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuUsageData
        fields = '__all__'

class CpuDataSerializer(serializers.ModelSerializer):
    cpu_usage = CpuUsageDataSerializer(many=True, read_only=True)
    class Meta:
        model = CpuData
        fields = '__all__'

class SystemInfoSerializer(serializers.Serializer):
    uptime = serializers.DecimalField(decimal_places=2, max_digits=20)
    system_time = serializers.DateTimeField()
    system_time_zone = serializers.CharField()
    system_time_offset = serializers.CharField()
    cpu_model = serializers.CharField()
    hostname = serializers.CharField()
    task_interval = serializers.IntegerField()

class FilesystemUsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesystemUsageData
        fields = "__all__"

class FilesystemDataSerializer(serializers.ModelSerializer):
    filesystem_usage = FilesystemUsageDataSerializer(many=True, read_only=True)
    class Meta:
        model = FilesystemData
        fields = "__all__"

class DiskUsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskUsageData
        fields = "__all__"


class PartitionDataSerializer(serializers.ModelSerializer):
    filesystem_data = FilesystemDataSerializer(many=True, read_only=True)
    class Meta:
        model = PartitionData
        fields = "__all__"

class DiskDataSerializer(serializers.ModelSerializer):
    disk_usage = DiskUsageDataSerializer(many=True, read_only=True)
    partition_data = PartitionDataSerializer(many=True, read_only=True)
    filesystem_data = FilesystemDataSerializer(many=True,read_only=True)
    class Meta:
        model = DiskData
        fields = "__all__"

class SettingsSerializer(serializers.ModelSerializer):
    retention_period = serializers.SerializerMethodField()
    class Meta:
        model = Settings
        fields = "__all__"

    def get_retention_period(self, obj):
        if obj.retention_period:
            return int(obj.retention_period.total_seconds())
        return None
