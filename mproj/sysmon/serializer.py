#!/usr/bin/env python3

from rest_framework import serializers
from .models import CpuUsageData, MemoryData, CpuData

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
