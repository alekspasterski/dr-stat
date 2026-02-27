#!/usr/bin/env python3

from rest_framework import serializers
from .models import CpuUsageData, MemoryData, CpuData

class MemorySerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    free = serializers.DecimalField(decimal_places=0, max_digits=100)
    total = serializers.DecimalField(decimal_places=0, max_digits=100)

    def create(self, validated_data):
        return MemoryData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp = validated_data.get("timestamp", instance.timestamp)
        instance.free = validated_data.get("free", instance.free)
        instance.total = validated_data.get("total", instance.total)
        instance.save()
        return instance


class CpuUsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuUsageData
        fields = '__all__'

class CpuDataSerializer(serializers.ModelSerializer):
    cpu_usage = CpuUsageDataSerializer(many=True, read_only=True)
    class Meta:
        model = CpuData
        fields = '__all__'
