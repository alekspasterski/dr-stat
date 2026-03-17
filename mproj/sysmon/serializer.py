#!/usr/bin/env python3

from diskinfo import FileSystem
from rest_framework import serializers
from .models import CpuUsageData, MemoryData, CpuData, DiskData, DiskUsageData, PartitionData, FilesystemData, FilesystemUsageData

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
    filesystem_data = FilesystemDataSerializer(read_only=True)
    class Meta:
        model = PartitionData
        fields = "__all__"

class DiskDataSerializer(serializers.ModelSerializer):
    disk_usage = DiskUsageDataSerializer(many=True, read_only=True)
    partition_data = PartitionDataSerializer(many=True, read_only=True)
    filesystem_data = FilesystemDataSerializer(read_only=True)
    class Meta:
        model = DiskData
        fields = "__all__"
