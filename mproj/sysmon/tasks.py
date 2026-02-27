#!/usr/bin/env python3
from celery import shared_task
from .utils import get_memory_info, get_cpu_info
from .models import MemoryData, CpuData, CpuUsageData
from django.utils import timezone


@shared_task
def check_memory_and_cpu():
    stats: dict[str, str | float | dict[str, str]] = get_memory_info()
    s: MemoryData = MemoryData(timestamp=timezone.now(), free=stats['free_memory'], total=stats["total_memory"])
    s.save()
    statsCpu: dict[str, str | list[float]] = get_cpu_info()
    time = timezone.now()
    sCpu = CpuData(timestamp=time, avg_load=statsCpu["avg_load"])
    sCpu.save()
    s2 = []
    all_zeroes = True
    for i, v in enumerate(statsCpu['cpu_usage']):
        s2.append(CpuUsageData(cpu_data=sCpu, cpu_usage=v, cpu_number=i))
        if v != 0.00:
            all_zeroes = False
    if not all_zeroes:
        CpuUsageData.objects.bulk_create(s2)
