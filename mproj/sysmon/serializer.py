#!/usr/bin/env python3

from rest_framework import serializers
from .models import CpuUsageData, MemoryData, CpuData, DiskData, DiskUsageData, PartitionData, PartitionUsageData

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

class DiskUsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskUsageData
        fields = "__all__"

class PartitionUsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartitionUsageData
        fields = "__all__"

class PartitionDataSerializer(serializers.ModelSerializer):
    partition_usage = PartitionUsageDataSerializer(many=True, read_only=False)
    class Meta:
        model = PartitionData
        fields = "__all__"

class DiskDataSerializer(serializers.ModelSerializer):
    disk_usage = DiskUsageDataSerializer(many=True, read_only=True)
    partition_data = PartitionDataSerializer(many=True, read_only=True)
    class Meta:
        model = DiskData
        fields = "__all__"
